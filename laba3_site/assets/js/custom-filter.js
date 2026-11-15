document.addEventListener("DOMContentLoaded", function() {
    
    // ==========================================
    // 1. ЛОГИКА ПЛАВНОЙ ПАГИНАЦИИ
    // ==========================================
    const paginationLinks = document.querySelectorAll('.pagination .link');

    paginationLinks.forEach(link => {
        link.addEventListener('click', function(e) {
            const href = this.getAttribute('href');
            
            // Если это неактивная кнопка или пустая ссылка, ничего не делаем
            if (!href || href === '#' || this.closest('li').classList.contains('disabled')) {
                return;
            }

            // Отменяем стандартный переход по ссылке
            e.preventDefault();

            // 1. Плавно прокручиваем экран вверх
            window.scrollTo({
                top: 0,
                behavior: 'smooth'
            });

            // 2. Ждем окончания прокрутки и переходим по ссылке
            setTimeout(() => {
                window.location.href = href;
            }, 400); 
        });
    });


    // ==========================================
    // 2. ЛОГИКА ФИЛЬТРА ЦЕН (ДВОЙНОЙ ПОЛЗУНОК)
    // ==========================================
    const minRange = document.getElementById('min-price-range');
    const maxRange = document.getElementById('max-price-range');
    const minInput = document.getElementById('min-price-input');
    const maxInput = document.getElementById('max-price-input');
    const sliderRange = document.getElementById('slider-range');
    const applyBtn = document.getElementById('apply-price-filter');

    // Если на странице нет ползунка (например, мы на главной), прерываем выполнение
    if (!minRange || !maxRange) return;

    const absoluteMin = parseInt(minRange.min);
    const absoluteMax = parseInt(minRange.max);
    
    // Минимальный разрыв между ползунками (чтобы они не слиплись)
    const minGap = Math.round((absoluteMax - absoluteMin) * 0.02) || 100;

    function updateSlider() {
        let minVal = parseInt(minRange.value);
        let maxVal = parseInt(maxRange.value);

        // Защита от пересечения
        if (minVal > maxVal - minGap) {
            minVal = maxVal - minGap;
            minRange.value = minVal;
        }
        if (maxVal < minVal + minGap) {
            maxVal = minVal + minGap;
            maxRange.value = maxVal;
        }

        // Обновляем текстовые поля
        minInput.value = minVal;
        maxInput.value = maxVal;

        // Красим активную полоску между ползунками
        const range = absoluteMax - absoluteMin;
        const leftPercent = ((minVal - absoluteMin) / range) * 100;
        const rightPercent = ((maxVal - absoluteMin) / range) * 100;
        
        sliderRange.style.left = leftPercent + '%';
        sliderRange.style.width = (rightPercent - leftPercent) + '%';
    }

    // Слушатели для движения ползунков
    minRange.addEventListener('input', updateSlider);
    maxRange.addEventListener('input', updateSlider);

    // Слушатели для ручного ввода в поля
    minInput.addEventListener('change', function() {
        minRange.value = this.value;
        updateSlider();
    });
    maxInput.addEventListener('change', function() {
        maxRange.value = this.value;
        updateSlider();
    });

    // Применение фильтра
    applyBtn.addEventListener('click', function() {
        const minVal = minRange.value;
        const maxVal = maxRange.value;
        // Перезагружаем страницу с GET-параметрами
        window.location.href = `?min_price=${minVal}&max_price=${maxVal}`;
    });

    // Инициализация при загрузке страницы
    updateSlider();
});