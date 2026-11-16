document.addEventListener("DOMContentLoaded", function() {
    
    // ==========================================
    // 1. ЛОГИКА ПЛАВНОЙ ПАГИНАЦИИ
    // ==========================================
    const paginationLinks = document.querySelectorAll('.pagination .link');
    paginationLinks.forEach(link => {
        link.addEventListener('click', function(e) {
            const href = this.getAttribute('href');
            if (!href || href === '#' || this.closest('li').classList.contains('disabled')) return;
            e.preventDefault();
            window.scrollTo({ top: 0, behavior: 'smooth' });
            setTimeout(() => { window.location.href = href; }, 400); 
        });
    });


    // ==========================================
    // 2. ЛОГИКА ФИЛЬТРА ЦЕН (ДВОЙНОЙ ПОЛЗУНОК)
    // ==========================================
    const minRange = document.getElementById('min-price-range');
    const maxRange = document.getElementById('max-price-range');
    
    // Проверяем, есть ли вообще ползунок на странице
    if (minRange && maxRange) {
        const minInput = document.getElementById('min-price-input');
        const maxInput = document.getElementById('max-price-input');
        const sliderRange = document.getElementById('slider-range');
        const filterForm = document.getElementById('filter-form');

        const absoluteMin = parseInt(minRange.min);
        const absoluteMax = parseInt(minRange.max);
        const minGap = Math.round((absoluteMax - absoluteMin) * 0.02) || 100;

        function updateSlider() {
            let minVal = parseInt(minRange.value);
            let maxVal = parseInt(maxRange.value);

            if (minVal > maxVal - minGap) {
                minVal = maxVal - minGap;
                minRange.value = minVal;
            }
            if (maxVal < minVal + minGap) {
                maxVal = minVal + minGap;
                maxRange.value = maxVal;
            }

            if (minInput) minInput.value = minVal;
            if (maxInput) maxInput.value = maxVal;

            if (sliderRange) {
                const range = absoluteMax - absoluteMin;
                const leftPercent = ((minVal - absoluteMin) / range) * 100;
                const rightPercent = ((maxVal - absoluteMin) / range) * 100;
                
                sliderRange.style.left = leftPercent + '%';
                sliderRange.style.width = (rightPercent - leftPercent) + '%';
            }
        }

        minRange.addEventListener('input', updateSlider);
        maxRange.addEventListener('input', updateSlider);

        // Отправка формы при отпускании ползунка
        if (filterForm) {
            minRange.addEventListener('change', function() { filterForm.submit(); });
            maxRange.addEventListener('change', function() { filterForm.submit(); });
        }
        
        if (minInput) minInput.addEventListener('change', function() { minRange.value = this.value; updateSlider(); if(filterForm) filterForm.submit(); });
        if (maxInput) maxInput.addEventListener('change', function() { maxRange.value = this.value; updateSlider(); if(filterForm) filterForm.submit(); });

        updateSlider();
    }


    // ==========================================
    // 3. АВТОМАТИЧЕСКОЕ ПРИМЕНЕНИЕ ФИЛЬТРА (ЧЕКБОКСЫ)
    // ==========================================
    const filterForm = document.getElementById('filter-form');
    
    if (filterForm) {
        // Находим ВСЕ чекбоксы внутри формы фильтра
        const checkboxes = filterForm.querySelectorAll('input[type="checkbox"]');
        
        checkboxes.forEach(checkbox => {
            checkbox.addEventListener('change', function() {
                // При клике на чекбокс отправляем форму
                filterForm.submit();
            });
        });
    }
});