const input = document.getElementById("Calories");
const calories = 2000;
input.value = calories;
input.addEventListener("keydown", (e) => {
  if (e.key === "Enter") {
    
    alert(calories - input.value);
  }
});