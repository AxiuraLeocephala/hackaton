const buttons = document.querySelectorAll('.nav__button');
const authForm = document.getElementById('authForm');
const authClose = document.getElementById('authClose');
const authTitle = document.getElementById('authTitle');
const loginForm = document.getElementById('loginForm');
const registerLink = document.getElementById('registerLink');
const profile = document.getElementById('profile');
const profileName = document.getElementById('profileName');
const logoutBtn = document.getElementById('logoutBtn');

let currentRole = null; // кто вошёл — судья или организатор

// --- показать/скрыть элементы интерфейса ---
function updateUIAfterLogin(role) {
    // скрываем кнопки входа
    buttons.forEach(btn => btn.style.display = 'none');
    // скрываем регистрацию
    if (registerLink) registerLink.style.display = 'none';
    // показываем профиль
    profile.style.display = 'flex';
    profileName.textContent = role === 'organizer' ? 'Организатор' : 'Судья';
}

function resetUI() {
    buttons.forEach(btn => btn.style.display = 'inline-block');
    if (registerLink) registerLink.style.display = 'inline';
    profile.style.display = 'none';
    profileName.textContent = '';
}

// При нажатии на кнопку — показываем форму
buttons.forEach(button => {
    button.addEventListener('click', () => {
        currentRole = button.dataset.role; // сохраняем роль
        authTitle.textContent = `Вход как ${currentRole === 'organizer' ? 'организатор' : 'судья'}`;
        authForm.style.display = 'block'; // показываем форму
    });
});

// закрыть форму
authClose.addEventListener('click', () => {
    authForm.style.display = 'none';
});

// При отправке формы — отправляем POST-запрос
loginForm.addEventListener('submit', async (e) => {
    e.preventDefault();

    if (!currentRole) {
        alert('Выберите роль перед входом!');
        return;
    }

    const login = document.getElementById('login').value;
    const password = document.getElementById('password').value;

    try {
        console.log(currentRole);
        const response = await fetch('https://ungraciously-gracious-surgeonfish.cloudpub.ru/authenticate', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({
                who_is: currentRole,
                login: login,
                password: password
            })
        });

        if (!response.ok) throw new Error('Ошибка при отправке запроса');

        const data = await response.json();
        console.log('Ответ от сервера:', data);

        localStorage.setItem('role', currentRole);
        updateUIAfterLogin(currentRole);

        alert('Вход выполнен!');
        authForm.style.display = 'none'; // скрыть форму после успешного входа
    } catch (error) {
        console.error('Ошибка:', error);
        alert('Ошибка при входе. Проверьте данные.');
    }
});

// --- выход ---
logoutBtn.addEventListener('click', () => {
    localStorage.removeItem('role');
    currentRole = null; // сбрасываем текущую роль
    resetUI();
});

// --- при загрузке страницы ---
document.addEventListener('DOMContentLoaded', () => {
    const savedRole = localStorage.getItem('role');
    if (savedRole) {
        updateUIAfterLogin(savedRole);
    }
});