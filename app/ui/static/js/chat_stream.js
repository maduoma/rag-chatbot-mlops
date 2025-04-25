// app/ui/static/js/chat_stream.js

document.addEventListener("DOMContentLoaded", () => {
    const form = document.querySelector("form[action='/chat']");
    const textarea = form.querySelector("textarea");
    const liveDiv = document.getElementById("live-response");
  
    form.addEventListener("submit", async (e) => {
      e.preventDefault();
      const query = textarea.value.trim();
      if (!query) return;
  
      // Disable form
      textarea.disabled = true;
  
      // Show live response area
      liveDiv.innerHTML = "";
      liveDiv.style.display = "block";
  
      const response = await fetch("/chat-stream", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ query })
      });
  
      const result = await response.json();
      const fullText = result.answer;
      let i = 0;
  
      const typer = setInterval(() => {
        if (i < fullText.length) {
          liveDiv.innerHTML += fullText[i++];
        } else {
          clearInterval(typer);
          setTimeout(() => {
            window.location.reload(); // Show entire history again
          }, 800);
        }
      }, 20);
    });
  });
  