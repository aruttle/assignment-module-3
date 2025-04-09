document.addEventListener("DOMContentLoaded", () => {
    const form = document.getElementById("contactForm");
    const responseText = document.getElementById("formResponse");
  
    if (form) {
      form.addEventListener("submit", (e) => {
        const name = document.getElementById("name").value.trim();
        const email = document.getElementById("email").value.trim();
        const message = document.getElementById("message").value.trim();
  
        if (!name || !email || !message) {
          e.preventDefault();
          responseText.textContent = "Please fill in all fields.";
          responseText.style.color = "red";
        }
      });
    }
  });
  