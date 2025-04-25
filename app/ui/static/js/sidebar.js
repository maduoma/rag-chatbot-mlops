// app/ui/static/js/sidebar.js

document.addEventListener("DOMContentLoaded", () => {
    const toggle = document.getElementById("toggleSidebar");
    const sidebar = document.getElementById("sidebar");
  
    if (toggle) {
      toggle.addEventListener("click", () => {
        sidebar.classList.toggle("collapsed");
      });
    }
  });

  // app/ui/static/js/sidebar.js

document.addEventListener("DOMContentLoaded", () => {
    const toggle = document.getElementById("toggleSidebar");
    const sidebar = document.getElementById("sidebar");
  
    if (toggle) {
      toggle.addEventListener("click", () => {
        sidebar.classList.toggle("collapsed");
      });
    }
  
    // Dropdown visibility
    const kebabButtons = document.querySelectorAll(".kebab-btn");
    kebabButtons.forEach(btn => {
      btn.addEventListener("click", (e) => {
        e.preventDefault();
        e.stopPropagation();
        closeAllDropdowns();
        const menu = btn.nextElementSibling;
        menu.style.display = "block";
      });
    });
  
    document.body.addEventListener("click", closeAllDropdowns);
  
    function closeAllDropdowns() {
      const dropdowns = document.querySelectorAll(".kebab-dropdown");
      dropdowns.forEach(dd => dd.style.display = "none");
    }
  });
  
  function confirmDelete() {
    return confirm("Are you sure you want to delete this chat session?");
  }
  
  // app/ui/static/js/sidebar.js

document.addEventListener("DOMContentLoaded", () => {
    const toggle = document.getElementById("toggleSidebar");
    const sidebar = document.getElementById("sidebar");
  
    if (toggle) {
      toggle.addEventListener("click", () => {
        sidebar.classList.toggle("collapsed");
      });
    }
  
    // Dropdown visibility
    const kebabButtons = document.querySelectorAll(".kebab-btn");
    kebabButtons.forEach(btn => {
      btn.addEventListener("click", (e) => {
        e.preventDefault();
        e.stopPropagation();
        closeAllDropdowns();
        const menu = btn.nextElementSibling;
        menu.style.display = "block";
      });
    });
  
    document.body.addEventListener("click", closeAllDropdowns);
  
    function closeAllDropdowns() {
      const dropdowns = document.querySelectorAll(".kebab-dropdown");
      dropdowns.forEach(dd => dd.style.display = "none");
    }
  });
  
  function confirmDelete() {
    return confirm("Are you sure you want to delete this chat session?");
  }
  