/* global axios */

const openBtnLogin = document.querySelector('.login');
const loginBtn = document.querySelector('.loginBtn');

loginBtn.addEventListener('click', () => {
    openBtnLogin.style.display = 'flex';
    openBtnRegister.style.display = 'none';
});


const openBtnRegister = document.querySelector('.register');
const registerBtn = document.querySelector('.registerBtn');

registerBtn.addEventListener('click', () => {
    openBtnRegister.style.display = 'flex';
    openBtnLogin.style.display = 'none';
})


axios.defaults.baseURL = 'http://127.0.0.1:8000';
axios.defaults.withCredentials = false;

const emailRegisterInput = document.getElementById('emailRegister');
const passwordRegisterInput = document.getElementById('passwordRegister');
const registerSubmitBtn = document.getElementById('signinBtnRegister');
const msgRegister = document.getElementById('msgRegister');

registerSubmitBtn.addEventListener('click', async () => {
    const email = emailRegisterInput.value.trim();
    const password = passwordRegisterInput.value.trim();

    msgRegister.textContent = '';

    if (!email || !password) {
        msgRegister.textContent = 'Please provide email and password.';
        msgRegister.style.color = 'red';
        return;
    }

    try {
        const response = await axios.post('/users/register', {
            email: email,
            password: password
        });

        msgRegister.textContent = 'Registered successfully!';
        msgRegister.style.color = 'green';

        return response;

    } catch (error) {
        console.error(error);
        msgRegister.textContent = 'Registration failed.';
        msgRegister.style.color = 'red';
    }
});