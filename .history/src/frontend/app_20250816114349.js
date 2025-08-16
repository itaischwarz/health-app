const input = document.getElementById("Calories");
int calories = 2000;
input.addEventListener("keydown", (e) => {
  if (e.key === "Enter") {
    alert("You asked: " + 2000 - input.value);
  }
});