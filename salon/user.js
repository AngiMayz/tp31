// Пример данных пользователя
const currentUser = JSON.parse(localStorage.getItem('currentUser')) || {
  id: 1,
  name: "Пользователь",
  avatar: "images/avatar.png",
  cart: ["Стрижка", "Окрашивание"],
  gifts: ["Скидка 10%", "Подарок шампунь"],
  favorites: ["Маникюр", "Педикюр"]
};

// Инициализация страницы
window.onload = function () {
  if (!currentUser) {
    alert('Для доступа к личному кабинету необходимо войти');
    window.location.href = 'login.html';
  }

  renderTabs();
  renderUserData();
};

// Функция для рендеринга табов
function renderTabs() {
  const tabs = document.querySelectorAll('.tab');
  const tabPanes = document.querySelectorAll('.tab-pane');

  tabs.forEach(tab => {
    tab.addEventListener('click', function () {
      // Деактивировать все табы и панели
      tabs.forEach(t => t.classList.remove('active'));
      tabPanes.forEach(p => p.classList.remove('active'));

      // Активировать текущий таб и соответствующую панель
      this.classList.add('active');
      const targetPane = document.getElementById(this.dataset.tab);
      targetPane.classList.add('active');
    });
  });

  // Активировать первый таб по умолчанию
  tabs[0].click();
}

// Функция для рендеринга данных пользователя
function renderUserData() {
  // Отображение аватара
  document.querySelector('.profile-avatar').src = currentUser.avatar;

  // Отображение услуг в корзине
  const cartList = document.querySelector('#cart .services-list');
  cartList.innerHTML = '';
  currentUser.cart.forEach(service => {
    const item = document.createElement('p');
    item.textContent = service;
    cartList.appendChild(item);
  });

  // Отображение подарков
  const giftsList = document.querySelector('#gifts .gifts-list');
  giftsList.innerHTML = '';
  currentUser.gifts.forEach(gift => {
    const item = document.createElement('p');
    item.textContent = gift;
    giftsList.appendChild(item);
  });

  // Отображение избранных услуг
  const favoritesList = document.querySelector('#favorites .favorites-list');
  favoritesList.innerHTML = '';
  currentUser.favorites.forEach(favorite => {
    const item = document.createElement('p');
    item.textContent = favorite;
    favoritesList.appendChild(item);
  });
}

// Выход из системы
document.querySelector('.logout-btn').addEventListener('click', function () {
  localStorage.removeItem('currentUser');
  alert('Вы вышли из системы');
  window.location.href = 'index.html';
});