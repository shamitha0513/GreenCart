/* GreenCart Global Theme & UI JavaScript */

document.addEventListener("DOMContentLoaded", function () {
  const themeToggleBtn = document.getElementById("themeToggleBtn");
  const themeIcon = document.getElementById("themeIcon");
  
  // 1. Initialize Theme Preference from localStorage
  const savedTheme = localStorage.getItem("greencart_theme") || "light";
  applyTheme(savedTheme);

  if (themeToggleBtn) {
    themeToggleBtn.addEventListener("click", function () {
      const currentTheme = document.documentElement.getAttribute("data-bs-theme");
      const newTheme = currentTheme === "dark" ? "light" : "dark";
      applyTheme(newTheme);
    });
  }

  function applyTheme(theme) {
    document.documentElement.setAttribute("data-bs-theme", theme);
    localStorage.setItem("greencart_theme", theme);
    
    if (themeIcon) {
      if (theme === "dark") {
        themeIcon.className = "bi bi-sun-fill text-warning";
      } else {
        themeIcon.className = "bi bi-moon-stars-fill text-dark";
      }
    }
  }

  // 2. Initialize Bootstrap Tooltips & Popovers
  const tooltipTriggerList = document.querySelectorAll('[data-bs-toggle="tooltip"]');
  [...tooltipTriggerList].map(tooltipTriggerEl => new bootstrap.Tooltip(tooltipTriggerEl));
});
