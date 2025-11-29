import torch
import torch.nn as nn
import torch.optim as optim
import pandas as pd
import numpy as np
from db import SessionLocal, engine
import sqlite3

class NeutritionPlanner(nn.Module):
    def __init__(self, num_foods, num_nutrients=4, hidden_dim=128):
        super(NeutritionPlanner, self).__init__()
        
        self.num_foods = num_foods
        self.num_nutrients = num_nutrients
        
        # Embedding layer for food features
        self.food_encoder = nn.Sequential(
            nn.Linear(num_nutrients + 10, hidden_dim),  # nutrients + category features
            nn.ReLU(),
            nn.Dropout(0.2),
            nn.Linear(hidden_dim, hidden_dim),
            nn.ReLU(),
            nn.Dropout(0.2)
        )
        
        # Context encoder for goals and current state
        self.context_encoder = nn.Sequential(
            nn.Linear(num_nutrients * 2, hidden_dim),  # goals + current state
            nn.ReLU(),
            nn.Linear(hidden_dim, hidden_dim),
            nn.ReLU()
        )
        
        # Attention mechanism to select foods based on context
        self.attention = nn.MultiheadAttention(hidden_dim, num_heads=4, batch_first=True)
        
        # Serving size predictor (outputs servings for each food)
        self.serving_predictor = nn.Sequential(
            nn.Linear(hidden_dim, hidden_dim // 2),
            nn.ReLU(),
            nn.Linear(hidden_dim // 2, 1),
            nn.Sigmoid()  # Output between 0-1, will scale to 0-2 servings
        )
        
    def forward(self, food_features, context):
        """
        Args:
            food_features: [batch_size, num_foods, num_features] - nutritional info + categories
            context: [batch_size, num_nutrients * 2] - goals + current state
        Returns:
            servings: [batch_size, num_foods] - predicted servings for each food
        """
        batch_size = food_features.shape[0]
        
        # Encode each food
        food_encoded = self.food_encoder(food_features)  # [batch, num_foods, hidden_dim]
        
        # Encode context (goals + current state)
        context_encoded = self.context_encoder(context)  # [batch, hidden_dim]
        context_encoded = context_encoded.unsqueeze(1)  # [batch, 1, hidden_dim]
        
        # Apply attention: foods attend to context
        attended_foods, _ = self.attention(
            food_encoded, 
            context_encoded.expand(-1, self.num_foods, -1),
            context_encoded.expand(-1, self.num_foods, -1)
        )  # [batch, num_foods, hidden_dim]
        
        # Predict servings for each food
        servings = self.serving_predictor(attended_foods).squeeze(-1)  # [batch, num_foods]
        servings = servings * 2  # Scale to 0-2 servings
        
        return servings


class MealPlannerTrainer:
    def __init__(self, df, device='cpu'):
        self.df = df
        self.device = device
        self.model = None
        self.food_features = None
        self.food_names = None
        
    def prepare_data(self, prefs=None):
        """Prepare and filter dataframe based on preferences"""
        df = self.df.copy()
        
        # Apply dietary preferences
        if prefs:
            if "vegetarian" in prefs:
                df = df[~df["category"].str.lower().eq("meat")]
            if "vegan" in prefs:
                df = df[
                    (~df["category"].str.lower().eq("meat")) &
                    (~df["category"].str.lower().eq("dairy")) &
                    (~df["name"].str.lower().str.contains(r"\begg\b", na=False))
                ]
            if "kosher" in prefs or "halal" in prefs:
                df = df[~df["name"].str.contains(r"\b(pork|ham|bacon)\b", case=False, na=False)]
        
        # One-hot encode categories
        df = pd.get_dummies(df, columns=["category"], dtype=int)
        
        # Store food names
        self.food_names = df["name"].values
        
        # Extract features: [calories, protein, carbs, fat, ...category_dummies]
        nutrient_cols = ['calories', 'protein_g', 'carbs_g', 'fat_g']
        category_cols = [col for col in df.columns if col.startswith('category_')]
        
        feature_cols = nutrient_cols + category_cols
        self.food_features = torch.FloatTensor(df[feature_cols].values).to(self.device)
        
        # Initialize model
        num_foods = len(df)
        num_features = len(feature_cols)
        self.model = NeutritionPlanner(num_foods, num_nutrients=4, hidden_dim=128).to(self.device)
        
        return df
    
    def create_context_tensor(self, goals_dict, currentStanding):
        """Create context tensor from goals and current state"""
        # Remaining nutrients needed
        remaining = [
            goals_dict["target_calories"] - currentStanding["current_calories"],
            goals_dict["target_protein"] - currentStanding["current_protein"],
            goals_dict["target_carbs"] - currentStanding["current_carbs"],
            goals_dict["max_fat"] - currentStanding["current_fat"]
        ]
        
        # Goals
        goals = [
            goals_dict["target_calories"],
            goals_dict["target_protein"],
            goals_dict["target_carbs"],
            goals_dict["max_fat"]
        ]
        
        # Concatenate: [remaining, goals]
        context = torch.FloatTensor(remaining + goals).unsqueeze(0).to(self.device)
        return context
    
    def compute_loss(self, servings, context, food_features):
        """
        Custom loss function that penalizes deviation from nutritional goals
        and enforces constraints
        """
        batch_size = servings.shape[0]
        
        # Extract nutrient columns (first 4 features)
        nutrients = food_features[:, :, :4]  # [batch, num_foods, 4]
        
        # Calculate actual nutrients from servings
        actual_nutrients = torch.sum(servings.unsqueeze(-1) * nutrients, dim=1)  # [batch, 4]
        
        # Extract remaining targets from context (first 4 values)
        targets = context[:, :4]  # [batch, 4]
        
        # Deviation loss: minimize difference from targets
        weights = torch.FloatTensor([1.0, 2.0, 1.0, 1.0]).to(self.device)  # protein weighted more
        deviation_loss = torch.sum(weights * torch.abs(actual_nutrients - targets))
        
        # Sparsity loss: encourage selecting fewer foods
        sparsity_loss = 0.1 * torch.sum(torch.sigmoid(servings * 10))  # soft threshold
        
        # Diversity loss: encourage variety across categories
        # (categories are in features beyond first 4)
        category_features = food_features[:, :, 4:]  # [batch, num_foods, num_categories]
        selected_categories = torch.sum(
            servings.unsqueeze(-1) * category_features, dim=1
        )  # [batch, num_categories]
        diversity_loss = -0.05 * torch.sum(torch.clamp(selected_categories, 0, 1))
        
        total_loss = deviation_loss + sparsity_loss + diversity_loss
        
        return total_loss, {
            'deviation': deviation_loss.item(),
            'sparsity': sparsity_loss.item(),
            'diversity': diversity_loss.item(),
            'actual_nutrients': actual_nutrients[0].detach().cpu().numpy()
        }
    
    def train_for_plan(self, goals_dict, currentStanding, prefs=None, num_iterations=1000, lr=0.01):
        """Train model to generate a meal plan for specific goals"""
        # Prepare data
        df = self.prepare_data(prefs)
        
        # Create context
        context = self.create_context_tensor(goals_dict, currentStanding)
        
        # Prepare food features (add batch dimension)
        food_features_batch = self.food_features.unsqueeze(0)  # [1, num_foods, num_features]
        
        # Optimizer
        optimizer = optim.Adam(self.model.parameters(), lr=lr)
        
        # Training loop
        best_loss = float('inf')
        best_servings = None
        
        for iteration in range(num_iterations):
            optimizer.zero_grad()
            
            # Forward pass
            servings = self.model(food_features_batch, context)
            
            # Compute loss
            loss, metrics = self.compute_loss(servings, context, food_features_batch)
            
            # Backward pass
            loss.backward()
            optimizer.step()
            
            # Track best solution
            if loss.item() < best_loss:
                best_loss = loss.item()
                best_servings = servings.detach().clone()
            
            if iteration % 100 == 0:
                print(f"Iteration {iteration}: Loss = {loss.item():.2f}, "
                      f"Deviation = {metrics['deviation']:.2f}")
        
        return self.extract_plan(best_servings, metrics)
    
    def extract_plan(self, servings, metrics):
        """Convert model output to meal plan format"""
        servings_np = servings.squeeze().cpu().numpy()
        
        # Round servings and filter out near-zero values
        servings_rounded = np.round(servings_np)
        threshold = 0.5
        
        plan = {}
        for i, (name, serving) in enumerate(zip(self.food_names, servings_rounded)):
            if serving >= threshold:
                # Get category from dataframe
                category = self.df[self.df["name"] == name]["category"].values[0] if "category" in self.df.columns else "unknown"
                plan[name] = (int(serving), category)
        
        return {
            "plan": plan if len(plan) > 0 else None,
            "metrics": metrics['actual_nutrients']
        }


def create_plan(goals_dict, prefs, currentStanding):
    """Main function compatible with original interface"""
    # Load data
    conn = sqlite3.connect("foods.db")
    cur = conn.cursor()
    cur.execute("""
                SELECT * FROM foods
                """)


    rows = cur.fetchall()
    for row in rows:
        print(row)

    conn.close()
    exit()

    df = pd.read_sql("SELECT name, calories, protein, carbs, fat, category, spread FROM foods")
    
    # Normalize spread column
    df["spread"] = df["spread"].replace({"Yes": 1, "No": 0, True: 1, False: 0}).fillna(0).astype(int)
    df["category"] = df["category"].astype(str)
    
    # Create trainer
    device = 'cuda' if torch.cuda.is_available() else 'cpu'
    trainer = MealPlannerTrainer(df, device=device)
    
    # Train and generate plan
    result = trainer.train_for_plan(goals_dict, currentStanding, prefs, num_iterations=500)
    
    print(result)
    return result


# Example usage
if __name__ == "__main__":
    result = create_plan(
        {"target_calories": 2500, "target_protein": 150, "target_carbs": 100, "max_fat": 150},
        None,
        {"current_calories": 0, "current_protein": 0, "current_carbs": 0, "current_fat": 0}
    )