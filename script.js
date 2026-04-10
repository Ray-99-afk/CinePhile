/* =========================================
   1. TOGGLE LOGIC (Slide between Login/Signup)
   ========================================= */
const container = document.getElementById('auth-container');
const registerBtn = document.getElementById('register');
const loginBtn = document.getElementById('login');

// Check if these elements exist (to prevent errors on other pages)
if (container && registerBtn && loginBtn) {
    registerBtn.addEventListener('click', () => {
        container.classList.add("active");
    });

    loginBtn.addEventListener('click', () => {
        container.classList.remove("active");
    });
}

