document.addEventListener("DOMContentLoaded", function() {
    
    // ==========================================
    // 1. ЗАПОЛНЕНИЕ ФОРМЫ ИЗ ПРОФИЛЯ
    // ==========================================
    const fillBtn = document.getElementById('fill-profile-btn');
    
    if (fillBtn) {
        fillBtn.addEventListener('click', function() {
            const profileData = {
                lastName: fillBtn.dataset.lastName || "",
                firstName: fillBtn.dataset.firstName || "",
                middleName: fillBtn.dataset.middleName || "",
                phone: fillBtn.dataset.phone || "",
                email: fillBtn.dataset.email || "",
                region: fillBtn.dataset.region || "",
                city: fillBtn.dataset.city || "",
                postalCode: fillBtn.dataset.postalCode || "",
                address: fillBtn.dataset.address || ""
            };

            const fields = {
                'checkout-last-name': profileData.lastName,
                'checkout-first-name': profileData.firstName,
                'checkout-middle-name': profileData.middleName,
                'checkout-phone': profileData.phone,
                'checkout-email': profileData.email,
                'checkout-region': profileData.region,
                'checkout-city': profileData.city,
                'checkout-postal-code': profileData.postalCode,
                'checkout-address': profileData.address
            };

            for (const [id, value] of Object.entries(fields)) {
                const input = document.getElementById(id);
                if (input) {
                    input.value = value;
                }
            }
        });
    }

    // ==========================================
    // 2. ПРОВЕРКА ФОРМЫ ПЕРЕД ОФОРМЛЕНИЕМ ЗАКАЗА
    // ==========================================
    // Находим кнопку "Оформить заказ" (она находится внутри формы отправки)
    const checkoutSubmitBtn = document.querySelector('form[action*="checkout_success"] button');
    const checkoutForm = document.getElementById('checkout-form');

    if (checkoutSubmitBtn && checkoutForm) {
        checkoutSubmitBtn.addEventListener('click', function(e) {
            // Проверяем, все ли обязательные поля формы (с атрибутом required) заполнены
            if (!checkoutForm.checkValidity()) {
                // Если есть пустые поля, показываем подсказку браузера
                checkoutForm.reportValidity();
                // Отменяем отправку формы
                e.preventDefault(); 
                return false;
            }
            // Если всё ок, форма отправляется дальше
        });
    }
});