// gpt_enter.js
// Handles Enter-to-send for the chat input, with Shift+Enter for newline

document.addEventListener("DOMContentLoaded", () => {
  const form = document.getElementById("gpt-chat-form");
  const textarea = document.getElementById("gpt-input");

  if (!form || !textarea) return;

  textarea.addEventListener("keydown", function (e) {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      if (textarea.value.trim() !== "") {
        form.submit();
      }
    }
  });

  // Optional: auto-grow textarea
  textarea.addEventListener("input", function () {
    this.style.height = "auto";
    this.style.height = (this.scrollHeight) + "px";
  });
});
