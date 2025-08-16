const input = document.getElementById("Calories");
input.addEventListener("keydown", (e) => {
  if (e.key === "Enter") {
    alert("You asked: " + input.value);
  }
});