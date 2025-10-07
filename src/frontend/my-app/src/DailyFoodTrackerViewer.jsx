import { Trash2, Plus } from "lucide-react";

export default function DailyFoodTracker({
  items,
  calories,
  protein,
  carbs,
  fat,
  name,
  totals,
  setItems,
  setName,
  setCalories,
  setProtein,
  setCarbs,
  setFat,
  setTotals,
}) {
  function addItem() {
    if (!name || !calories) return;
    const entry = {
      id: crypto.randomUUID(),
      name,
      calories: Number(calories),
      protein: Number(protein) || 0,
      carbs: Number(carbs) || 0,
      fat: Number(fat) || 0,
    };
    setItems([entry, ...items]);
    setTotals({
      calories: +entry.calories,
      protein: +entry.protein,
      carbs: +entry.carbs,
      fat: +entry.fat,
    });
    setName("");
    setCalories("");
    setProtein("");
    setCarbs("");
    setFat("");
  }

  function removeItem(id) {
    setItems(items.filter((i) => i.id !== id));
  }

  // const totals = items.reduce(
  //   (acc, it) => {
  //     acc.calories += it.calories;
  //     acc.protein += it.protein;
  //     acc.carbs += it.carbs;
  //     acc.fat += it.fat;
  //     return acc;
  //   },
  //   { calories: 0, protein: 0, carbs: 0, fat: 0 }
  // );

  return (
    <div>
      <div className="card">
        <div className="card-header">Current Intake (Optional)</div>
        <div className="card-description">
          Add foods you've already eaten today to get a more personalized meal plan. 
          You can skip this step to generate a complete daily meal plan.
        </div>
        <div className="card-content">
          <input
            className="input"
            placeholder="Name"
            value={name}
            onChange={(e) => setName(e.target.value)}
          />
          <div
            style={{
              display: "grid",
              gridTemplateColumns: "repeat(4, 1fr)",
              gap: "8px",
            }}
          >
            <input
              className="input"
              type="number"
              placeholder="Calories"
              value={calories}
              onChange={(e) => setCalories(e.target.value)}
            />
            <input
              className="input"
              type="number"
              placeholder="Protein"
              value={protein}
              onChange={(e) => setProtein(e.target.value)}
            />
            <input
              className="input"
              type="number"
              placeholder="Carbs"
              value={carbs}
              onChange={(e) => setCarbs(e.target.value)}
            />
            <input
              className="input"
              type="number"
              placeholder="Fat"
              value={fat}
              onChange={(e) => setFat(e.target.value)}
            />
          </div>
          <button
            className="btn"
            onClick={addItem}
            style={{ marginTop: "12px" }}
          >
            <Plus size={16} style={{ marginRight: "4px" }} />
            Add
          </button>
        </div>
      </div>

      <div className="card">
        <div className="card-header">Today's Foods</div>
        <div className="card-content">
          {items.length === 0 && (
            <p style={{ fontSize: "14px", color: "#777" }}>
              No foods added yet. That's okay! You can proceed to generate a complete daily meal plan.
            </p>
          )}
          {items.map((it) => (
            <div key={it.id} className="food-item">
              <div>
                <div className="font-medium">{it.name}</div>
                <div className="food-meta">
                  {it.calories} kcal • P {it.protein} • C {it.carbs} • F{" "}
                  {it.fat}
                </div>
              </div>
              <button
                className="btn btn--ghost"
                onClick={() => removeItem(it.id)}
              >
                <Trash2 size={16} />
              </button>
            </div>
          ))}
        </div>
      </div>

      <div className="card">
        <div className="card-header">Current Totals</div>
        <div className="card-content">
          <div>Calories: {totals.calories}</div>
          <div>Protein: {totals.protein} g</div>
          <div>Carbs: {totals.carbs} g</div>
          <div>Fat: {totals.fat} g</div>
          {totals.calories === 0 && (
            <p style={{ fontSize: "12px", color: "#6b7280", marginTop: "8px", fontStyle: "italic" }}>
              No foods logged yet - you'll get a complete daily meal plan!
            </p>
          )}
        </div>
      </div>
    </div>
  );
}
