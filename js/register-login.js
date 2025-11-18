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