const input = document.getElementById("question");
input.addEventListener("keydown", (e) => {
  if (e.key === "Enter") {
    alert("You asked: " + input.value);
  }
});