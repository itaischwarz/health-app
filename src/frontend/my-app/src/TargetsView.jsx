export default function TargetsForm({ targets, setTargets }) {
  // Generic handler to update any field
  const handleChange = (key, value) => {
    setTargets({
      ...targets,
      [key]: value,
    });
  };

  return (
    <div>
      <h3>What is your target calories</h3>
      <input
        className="input"
        type="text"
        id="target_calories"
        value={targets.calories}
        onChange={(e) => handleChange("calories", e.target.value)}
      />

      <h3>What is your target protein</h3>
      <input
        className="input"
        type="text"
        id="target_protein"
        value={targets.protein}
        onChange={(e) => handleChange("protein", e.target.value)}
      />

      <h3>What is your target carbs</h3>
      <input
        className="input"
        type="text"
        id="target_carbs"
        value={targets.carbs}
        onChange={(e) => handleChange("carbs", e.target.value)}
      />

      <h3>What is your maximum fat</h3>
      <input
        className="input"
        type="text"
        id="max_fat"
        value={targets.fat}
        onChange={(e) => handleChange("fat", e.target.value)}
      />
    </div>
  );
}
