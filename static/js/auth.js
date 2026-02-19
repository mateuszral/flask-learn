const showForm = (type) => {
    const loginForm = document.querySelector('.login-form');
    const registerForm = document.querySelector('.register-form');
    const loginTab = document.querySelector('.login-tab');
    const registerTab = document.querySelector('.register-tab');

    if (type === 'login') {
        loginForm.classList.add('active');
        loginTab.classList.add('active');
        registerForm.classList.remove('active');
        registerTab.classList.remove('active');
    } else {
        registerForm.classList.add('active');
        registerTab.classList.add('active');
        loginForm.classList.remove('active');
        loginTab.classList.remove('active');
    }
}

const togglePassword = () => {
    const input = document.querySelector('.password-field');
    const toggle = document.querySelector('.toggle-password');

    if (input.type === 'password') {
        input.type = 'text';
        toggle.textContent = 'Hide';
    } else {
        input.type = 'password';
        toggle.textContent = 'Show';
    }
}