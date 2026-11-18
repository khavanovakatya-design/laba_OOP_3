document.addEventListener("DOMContentLoaded", function() {

    document.querySelectorAll('.qty-btn').forEach(btn => {
        btn.addEventListener('click', function(e) {
            e.stopImmediatePropagation(); // Останавливаем другие скрипты
        });
    });
    
    // ==========================================
    // 1. ЛОГИКА ДОБАВЛЕНИЯ В КОРЗИНУ (AJAX)
    // ==========================================
    const addToCartForms = document.querySelectorAll('.ajax-add-to-cart');

    addToCartForms.forEach(form => {
        form.addEventListener('submit', function(e) {
            e.preventDefault(); // Отменяем перезагрузку страницы

            // Принудительно синхронизируем видимое поле количества со скрытым перед отправкой
            const mainQty = document.getElementById('main-qty-input');
            const hiddenQty = document.getElementById('product-qty-input');
            if (mainQty && hiddenQty) {
                hiddenQty.value = mainQty.value;
            }

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

                    // Обновляем счетчик в шапке
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


    // ==========================================
    // 2. ЛОГИКА КНОПОК + и - НА СТРАНИЦЕ ТОВАРА
    // ==========================================
    const mainQtyInput = document.getElementById('main-qty-input');
    const hiddenQtyInput = document.getElementById('product-qty-input');
    const btnDecrease = document.getElementById('btn-decrease');
    const btnIncrease = document.getElementById('btn-increase');

    if (mainQtyInput && hiddenQtyInput) {
        
        // Функция синхронизации
        function syncQuantity() {
            hiddenQtyInput.value = mainQtyInput.value;
        }

        // Кнопка МИНУС
        if (btnDecrease) {
            btnDecrease.addEventListener('click', function(e) {
                e.preventDefault();
                e.stopImmediatePropagation(); // Блокируем встроенный скрипт темы
                
                let currentVal = parseInt(mainQtyInput.value) || 1;
                if (currentVal > 1) {
                    mainQtyInput.value = currentVal - 1;
                    syncQuantity();
                }
            });
        }

        // Кнопка ПЛЮС
        if (btnIncrease) {
            btnIncrease.addEventListener('click', function(e) {
                e.preventDefault();
                e.stopImmediatePropagation(); // Блокируем встроенный скрипт темы
                
                let currentVal = parseInt(mainQtyInput.value) || 1;
                mainQtyInput.value = currentVal + 1;
                syncQuantity();
            });
        }

        // Ручной ввод числа в поле
        mainQtyInput.addEventListener('input', syncQuantity);

        // Инициализация при загрузке
        syncQuantity();
    }


    // ==========================================
    // 3. КРАСИВОЕ ВСПЛЫВАЮЩЕЕ УВЕДОМЛЕНИЕ
    // ==========================================
    function showNotification(message, isError = false) {
        // Удаляем старое уведомление, если оно есть (чтобы не дублировались)
        const oldToast = document.getElementById('cart-toast');
        if (oldToast) oldToast.remove();

        const toast = document.createElement('div');
        toast.id = 'cart-toast';
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

        // Анимация появления
        setTimeout(() => { toast.style.transform = 'translateX(0)'; }, 100);

        // Анимация исчезновения
        setTimeout(() => {
            toast.style.transform = 'translateX(120%)';
            setTimeout(() => toast.remove(), 300);
        }, 3000);
    }

});