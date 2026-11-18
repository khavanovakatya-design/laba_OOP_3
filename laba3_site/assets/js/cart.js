document.addEventListener("DOMContentLoaded", function() {
    
    // Находим все формы добавления в корзину (по классу, который мы добавим в HTML)
    const addToCartForms = document.querySelectorAll('.ajax-add-to-cart');

    addToCartForms.forEach(form => {
        form.addEventListener('submit', function(e) {
            e.preventDefault(); // Отменяем перезагрузку страницы

            const url = this.action;
            const formData = new FormData(this);

            // Отправляем AJAX запрос
            fetch(url, {
                method: 'POST',
                body: formData,
                headers: {
                    'X-Requested-With': 'XMLHttpRequest' // Сообщаем Django, что это AJAX
                }
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    // Показываем всплывающее уведомление
                    showNotification(data.message);

                    // Обновляем счетчик в шапке (если у вас есть элемент с классом cart-badge)
                    const cartBadges = document.querySelectorAll('.cart-badge');
                    cartBadges.forEach(badge => {
                        badge.textContent = data.cart_total_items;
                    });
                }
            })
            .catch(error => {
                console.error('Ошибка:', error);
                showNotification('Ошибка при добавлении в корзину', true);
            });
        });
    });

    // Красивое всплывающее уведомление
    function showNotification(message, isError = false) {
        const toast = document.createElement('div');
        toast.style.cssText = `
            position: fixed; top: 20px; right: 20px; z-index: 9999;
            background-color: ${isError ? '#dc3545' : '#00234D'}; color: white; 
            padding: 15px 25px; border-radius: 5px; 
            box-shadow: 0 4px 12px rgba(0,0,0,0.15);
            font-family: 'Poppins', sans-serif; font-size: 14px;
            transform: translateX(120%); transition: transform 0.3s ease;
            border-left: 5px solid ${isError ? '#ffc107' : '#28a745'};
        `;
        toast.textContent = message;
        document.body.appendChild(toast);

        setTimeout(() => { toast.style.transform = 'translateX(0)'; }, 100);

        setTimeout(() => {
            toast.style.transform = 'translateX(120%)';
            setTimeout(() => toast.remove(), 300);
        }, 3000);
    }
});