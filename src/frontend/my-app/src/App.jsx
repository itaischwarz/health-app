import { useState } from "react";
import { Target, Utensils, Settings, Sparkles, ArrowRight, ArrowLeft } from "lucide-react";
import DailyFoodTracker from "./DailyFoodTrackerViewer";
import TargetsView from "./TargetsView";
import DietaryPreferences from "./components/DietaryPreferences";
import MealPlanViewer from "./components/MealPlanViewer";
import ProgressIndicator from "./components/ProgressIndicator";
import "./styles.css";

export default function App() {
  const [currentStep, setCurrentStep] = useState(1);
  const [items, setItems] = useState([]);
  const [totals, setTotals] = useState({
    calories: 0,
    protein: 0,
    carbs: 0,
    fat: 0,
  });
  const [name, setName] = useState("");
  const [calories, setCalories] = useState("");
  const [protein, setProtein] = useState("");
  const [carbs, setCarbs] = useState("");
  const [fat, setFat] = useState("");
  const [targets, setTargets] = useState({
    calories: "",
    protein: "",
    carbs: "",
    fat: "",
  });
  const [dietaryPrefs, setDietaryPrefs] = useState({
    vegetarian: false,
    vegan: false,
    kosher: false,
    halal: false,
    foodsToExclude: []
  });
  const [mealPlan, setMealPlan] = useState(null);
  const [loading, setLoading] = useState(false);

  const steps = [
    { id: 1, title: "Current Intake (Optional)", icon: Utensils },
    { id: 2, title: "Nutrition Targets", icon: Target },
    { id: 3, title: "Dietary Preferences", icon: Settings },
    { id: 4, title: "Meal Plan", icon: Sparkles }
  ];

  const generateMealPlan = async () => {
    setLoading(true);
    try {
      console.log("Generating meal plan with:", { targets, totals, dietaryPrefs });
      
      // Build preferences string
      const prefs = [];
      if (dietaryPrefs.vegetarian) prefs.push("vegetarian");
      if (dietaryPrefs.vegan) prefs.push("vegan");
      if (dietaryPrefs.kosher) prefs.push("kosher");
      if (dietaryPrefs.halal) prefs.push("halal");
      
      const response = await fetch(
        "http://127.0.0.1:8000/plan?" +
          new URLSearchParams({
            calories: targets.calories,
            protein: targets.protein,
            carbs: targets.carbs,
            fat: targets.fat,
            total_calories: totals.calories,
            total_protein: totals.protein,
            total_carbs: totals.carbs,
            total_fat: totals.fat,
            prefs: prefs.join(",")
          })
      );
      
      const data = await response.json();
      console.log("Response from backend:", data);
      
      // Use the actual meal plan from backend
      setMealPlan(data);
      
      setCurrentStep(4);
    } catch (error) {
      console.error("Error generating meal plan:", error);
      alert("Error generating meal plan. Please try again.");
    } finally {
      setLoading(false);
    }
  };

  const nextStep = () => {
    if (currentStep < 4) {
      setCurrentStep(currentStep + 1);
    }
  };

  const prevStep = () => {
    if (currentStep > 1) {
      setCurrentStep(currentStep - 1);
    }
  };

  const renderCurrentStep = () => {
    switch (currentStep) {
      case 1:
        return (
          <DailyFoodTracker
            name={name}
            items={items}
            calories={calories}
            protein={protein}
            carbs={carbs}
            fat={fat}
            totals={totals}
            setName={setName}
            setItems={setItems}
            setCalories={setCalories}
            setProtein={setProtein}
            setCarbs={setCarbs}
            setFat={setFat}
            setTotals={setTotals}
          />
        );
      case 2:
        return <TargetsView targets={targets} setTargets={setTargets} />;
      case 3:
        return <DietaryPreferences preferences={dietaryPrefs} setPreferences={setDietaryPrefs} />;
      case 4:
        return <MealPlanViewer mealPlan={mealPlan} />;
      default:
        return null;
    }
  };

  const canProceed = () => {
    switch (currentStep) {
      case 1:
        return true; // Allow proceeding even with zero current intake
      case 2:
        return targets.calories && targets.protein && targets.carbs && targets.fat;
      case 3:
        return true; // Dietary preferences are optional
      default:
        return false;
    }
  };

  return (
    <div className="app">
      <div className="container">
        <div className="header">
          <h1>Smart Meal Planner</h1>
          <p className="subtitle">Get personalized meal recommendations based on your nutrition goals</p>
        </div>

        <ProgressIndicator steps={steps} currentStep={currentStep} />

        <div className="step-content">
          {renderCurrentStep()}
        </div>

        <div className="navigation">
          {currentStep > 1 && (
            <button className="btn btn--secondary" onClick={prevStep}>
              <ArrowLeft size={16} />
              Previous
            </button>
          )}
          
          <div className="nav-spacer" />
          
          {currentStep < 3 && (
            <button 
              className="btn btn--primary" 
              onClick={nextStep}
              disabled={!canProceed()}
            >
              Next
              <ArrowRight size={16} />
            </button>
          )}
          
          {currentStep === 3 && (
            <button 
              className="btn btn--primary btn--large" 
              onClick={generateMealPlan}
              disabled={loading}
            >
              {loading ? (
                <>
                  <div className="spinner" />
                  Generating Plan...
                </>
              ) : (
                <>
                  <Sparkles size={16} />
                  Generate My Meal Plan
                </>
              )}
            </button>
          )}
        </div>
      </div>
    </div>
  );
}
