const input = document.getElementById("
    ");
input.addEventListener("keydown", (e) => {
  if (e.key === "Enter") {
    alert("You asked: " + input.value);
  }
});