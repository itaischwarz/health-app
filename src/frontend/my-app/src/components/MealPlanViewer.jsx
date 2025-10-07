import { Utensils, Target, TrendingUp, TrendingDown } from "lucide-react";

export default function MealPlanViewer({ mealPlan }) {
  if (!mealPlan) {
    return (
      <div className="meal-plan-viewer">
        <div className="card">
          <div className="card-content">
            <div className="empty-state">
              <Utensils size={48} className="empty-icon" />
              <h3>No Meal Plan Generated</h3>
              <p>Generate a meal plan to see your personalized recommendations here.</p>
            </div>
          </div>
        </div>
      </div>
    );
  }

  const { plan, metrics } = mealPlan;
  const [calories, protein, carbs, fat] = metrics;

  return (
    <div className="meal-plan-viewer">
      <div className="card">
        <div className="card-header">
          <h3>Your Personalized Meal Plan</h3>
          <p className="card-description">
            Here's your optimized meal plan based on your goals and preferences
          </p>
        </div>
        <div className="card-content">
          <div className="meal-plan-grid">
            <div className="meal-items">
              <h4>Recommended Foods</h4>
              <div className="food-list">
                {Object.entries(plan).map(([food, servings]) => (
                  <div key={food} className="meal-item">
                    <div className="food-info">
                      <span className="food-name">{food}</span>
                      <span className="serving-size">{servings} serving{servings !== 1 ? 's' : ''}</span>
                    </div>
                    <div className="food-icon">
                      <Utensils size={20} />
                    </div>
                  </div>
                ))}
              </div>
            </div>

            <div className="nutrition-summary">
              <h4>Nutrition Summary</h4>
              <div className="nutrition-metrics">
                <div className="metric">
                  <div className="metric-icon calories">
                    <Target size={20} />
                  </div>
                  <div className="metric-content">
                    <span className="metric-value">{calories}</span>
                    <span className="metric-label">Calories</span>
                  </div>
                </div>
                
                <div className="metric">
                  <div className="metric-icon protein">
                    <TrendingUp size={20} />
                  </div>
                  <div className="metric-content">
                    <span className="metric-value">{protein}g</span>
                    <span className="metric-label">Protein</span>
                  </div>
                </div>
                
                <div className="metric">
                  <div className="metric-icon carbs">
                    <TrendingUp size={20} />
                  </div>
                  <div className="metric-content">
                    <span className="metric-value">{carbs}g</span>
                    <span className="metric-label">Carbs</span>
                  </div>
                </div>
                
                <div className="metric">
                  <div className="metric-icon fat">
                    <TrendingDown size={20} />
                  </div>
                  <div className="metric-content">
                    <span className="metric-value">{fat}g</span>
                    <span className="metric-label">Fat</span>
                  </div>
                </div>
              </div>
            </div>
          </div>

          <div className="meal-plan-actions">
            <button className="btn btn--primary">
              Save Meal Plan
            </button>
            <button className="btn btn--secondary">
              Generate New Plan
            </button>
          </div>
        </div>
      </div>
    </div>
  );
}
