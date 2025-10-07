import { useState } from "react";
import { Plus, X } from "lucide-react";

export default function DietaryPreferences({ preferences, setPreferences }) {
  const [newFood, setNewFood] = useState("");

  const handlePreferenceChange = (key, value) => {
    setPreferences({
      ...preferences,
      [key]: value
    });
  };

  const addFoodToExclude = () => {
    if (newFood.trim() && !preferences.foodsToExclude.includes(newFood.trim())) {
      setPreferences({
        ...preferences,
        foodsToExclude: [...preferences.foodsToExclude, newFood.trim()]
      });
      setNewFood("");
    }
  };

  const removeFoodFromExclude = (food) => {
    setPreferences({
      ...preferences,
      foodsToExclude: preferences.foodsToExclude.filter(f => f !== food)
    });
  };

  return (
    <div className="dietary-preferences">
      <div className="card">
        <div className="card-header">
          <h3>Dietary Preferences</h3>
          <p className="card-description">
            Select your dietary preferences to get personalized meal recommendations
          </p>
        </div>
        <div className="card-content">
          <div className="preference-group">
            <h4>Diet Type</h4>
            <div className="checkbox-group">
              <label className="checkbox-label">
                <input
                  type="checkbox"
                  checked={preferences.vegetarian}
                  onChange={(e) => handlePreferenceChange('vegetarian', e.target.checked)}
                />
                <span className="checkmark"></span>
                Vegetarian
              </label>
              <label className="checkbox-label">
                <input
                  type="checkbox"
                  checked={preferences.vegan}
                  onChange={(e) => handlePreferenceChange('vegan', e.target.checked)}
                />
                <span className="checkmark"></span>
                Vegan
              </label>
              <label className="checkbox-label">
                <input
                  type="checkbox"
                  checked={preferences.kosher}
                  onChange={(e) => handlePreferenceChange('kosher', e.target.checked)}
                />
                <span className="checkmark"></span>
                Kosher
              </label>
              <label className="checkbox-label">
                <input
                  type="checkbox"
                  checked={preferences.halal}
                  onChange={(e) => handlePreferenceChange('halal', e.target.checked)}
                />
                <span className="checkmark"></span>
                Halal
              </label>
            </div>
          </div>

          <div className="preference-group">
            <h4>Foods to Exclude</h4>
            <p className="group-description">
              Add specific foods you'd like to avoid in your meal plan
            </p>
            <div className="add-food-container">
              <input
                type="text"
                className="input"
                placeholder="Enter food name (e.g., nuts, dairy, gluten)"
                value={newFood}
                onChange={(e) => setNewFood(e.target.value)}
                onKeyPress={(e) => e.key === 'Enter' && addFoodToExclude()}
              />
              <button 
                className="btn btn--secondary btn--small"
                onClick={addFoodToExclude}
                disabled={!newFood.trim()}
              >
                <Plus size={16} />
              </button>
            </div>
            
            {preferences.foodsToExclude.length > 0 && (
              <div className="excluded-foods">
                {preferences.foodsToExclude.map((food, index) => (
                  <div key={index} className="excluded-food-tag">
                    {food}
                    <button
                      className="remove-food-btn"
                      onClick={() => removeFoodFromExclude(food)}
                    >
                      <X size={14} />
                    </button>
                  </div>
                ))}
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  );
}
