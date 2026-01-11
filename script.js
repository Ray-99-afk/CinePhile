// We only run this code if we are on the Login Page
const container = document.getElementById('auth-container');
const registerBtn = document.getElementById('register');
const loginBtn = document.getElementById('login');

// Check if these elements exist before adding listeners
if (container && registerBtn && loginBtn) {
    registerBtn.addEventListener('click', () => {
        container.classList.add("active");
    });

    loginBtn.addEventListener('click', () => {
        container.classList.remove("active");
    });
} else {
    console.log("Not on login page, skipping auth scripts.");
}