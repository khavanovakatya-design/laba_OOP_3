document.addEventListener('DOMContentLoaded', function () {
  const csrfToken = document.cookie.match(/csrftoken=([^;]+)/)?.[1]
                 || document.querySelector('[name=csrfmiddlewaretoken]')?.value;

  // === Добавление / удаление (toggle) на карточках товаров ===
  document.querySelectorAll('.js-wishlist-toggle').forEach(function (btn) {
    btn.addEventListener('click', function (e) {
      e.preventDefault();
      const url = this.dataset.url;

      fetch(url, {
        method: 'POST',
        headers: {
          'X-CSRFToken': csrfToken,
          'X-Requested-With': 'XMLHttpRequest',
        },
      })
        .then(r => r.json())
        .then(data => {
          // краска сердечка
          this.classList.toggle('active', data.in_wishlist);
          const path = this.querySelector('path');
          if (path) path.setAttribute('fill', data.in_wishlist ? '#F76B6A' : 'currentColor');

          // счётчик в шапке
          const badge = document.querySelector('.wishlist-badge');
          if (badge) badge.textContent = data.count;
        })
        .catch(err => console.error('wishlist toggle error:', err));
    });
  });

  // === Удаление со страницы вишлиста ===
  document.querySelectorAll('.js-wishlist-remove').forEach(function (btn) {
    btn.addEventListener('click', function (e) {
      e.preventDefault();
      const itemId = this.dataset.itemId;

      fetch(`/wishlist/remove/${itemId}/`, {
        method: 'POST',
        headers: {
          'X-CSRFToken': csrfToken,
          'X-Requested-With': 'XMLHttpRequest',
        },
      })
        .then(r => r.json())
        .then(() => {
          const card = document.getElementById(`wishlist-item-${itemId}`);
          if (card) card.remove();

          const grid = document.getElementById('wishlist-grid');
          if (grid && grid.children.length === 0) {
            window.location.reload();  // покажем пустое состояние
          }
        })
        .catch(err => console.error('wishlist remove error:', err));
    });
  });
});