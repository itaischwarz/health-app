const input = document.getElementById("Calories");
i
input.addEventListener("keydown", (e) => {
  if (e.key === "Enter") {
    alert("You asked: " + 2000 - input.value);
  }
});