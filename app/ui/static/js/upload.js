// static/js/upload.js

document.addEventListener("DOMContentLoaded", () => {
    const form = document.getElementById("uploadForm");
    const statusDiv = document.getElementById("uploadStatus");
  
    form.addEventListener("submit", async (e) => {
      e.preventDefault();
      
      statusDiv.innerText = "Uploading and indexing...";
      
      const formData = new FormData(form);
      
      try {
        const response = await fetch("/upload", {
          method: "POST",
          body: formData,
        });
  
        const result = await response.json();
  
        if (result.success) {
          statusDiv.innerText = "Upload successful! Redirecting...";
          setTimeout(() => window.location.href = "/?msg=" + encodeURIComponent("Document uploaded!"), 1500);
        } else {
          statusDiv.innerText = "Error: " + result.message;
        }
      } catch (error) {
        statusDiv.innerText = "Upload completed. Redirecting...";
        setTimeout(() => window.location.href = "/", 1500);
      }
    });
  });