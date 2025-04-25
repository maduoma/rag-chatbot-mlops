// static/js/copy.js

document.addEventListener("DOMContentLoaded", () => {
    const copyIcons = document.querySelectorAll(".copy-icon");
  
    copyIcons.forEach(icon => {
      icon.addEventListener("click", () => {
        const text = icon.closest(".message").innerText;
        navigator.clipboard.writeText(text).then(() => {
          icon.setAttribute("title", "Copied!");
          setTimeout(() => icon.setAttribute("title", "Copy"), 1000);
        });
      });
    });
  });
  