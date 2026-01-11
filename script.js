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

/* =========================================
   2. REDIRECT LOGIC (Go to Dashboard)
   ========================================= */

// Select the actual forms
const signInForm = document.querySelector('.sign-in form');
const signUpForm = document.querySelector('.sign-up form');

// Handle Login Submit
if (signInForm) {
    signInForm.addEventListener('submit', (e) => {
        e.preventDefault(); // Stop the page from reloading
        // Here you would usually check password, but for now:
        window.location.href = "03_dashboard.html"; 
    });
}

// Handle Sign Up Submit
if (signUpForm) {
    signUpForm.addEventListener('submit', (e) => {
        e.preventDefault(); // Stop the page from reloading
        // Redirect to dashboard after signup
        window.location.href = "03_dashboard.html"; 
    });
}

