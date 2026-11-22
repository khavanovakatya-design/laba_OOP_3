document.addEventListener("DOMContentLoaded", function() {
    const searchForm = document.getElementById('live-search-form');
    const searchInput = document.getElementById('live-search-input');
    const dropdown = document.getElementById('search-results-dropdown');
    let debounceTimer;

    // Блокируем отправку формы при нажатии Enter (чтобы страница не перезагружалась)
    if (searchForm) {
        searchForm.addEventListener('submit', function(e) {
            e.preventDefault();
        });
    }

    if (searchInput && dropdown) {
        searchInput.addEventListener('input', function() {
            const query = this.value.trim();
            
            // Очищаем предыдущий таймер
            clearTimeout(debounceTimer);
            
            // Если ввели меньше 2 символов — скрываем список
            if (query.length < 2) {
                dropdown.style.display = 'none';
                return;
            }

            // Ждем 300 мс после последнего ввода
            debounceTimer = setTimeout(() => {
                // Отправляем AJAX запрос
                fetch(`${window.SEARCH_URL}?q=${encodeURIComponent(query)}`)
                    .then(response => response.json())
                    .then(data => {
                        dropdown.innerHTML = ''; // Очищаем старые результаты
                        
                        if (data.results.length > 0) {
                            data.results.forEach(product => {
                                // Создаем ссылку
                                const item = document.createElement('a');
                                item.href = product.url;
                                item.style.cssText = 'display: flex; align-items: center; padding: 10px 15px; border-bottom: 1px solid #eee; text-decoration: none; color: #333; transition: background 0.2s;';
                                
                                item.onmouseover = () => item.style.backgroundColor = '#f8f9fa';
                                item.onmouseout = () => item.style.backgroundColor = 'transparent';
                                
                                // Картинка
                                const img = document.createElement('img');
                                img.src = product.image;
                                img.style.cssText = 'width: 40px; height: 40px; object-fit: cover; border-radius: 4px; margin-right: 15px;';
                                
                                // Текст
                                const info = document.createElement('div');
                                info.innerHTML = `<div style="font-weight: 500; font-size: 14px; margin-bottom: 2px;">${product.title}</div>
                                                  <div style="color: #00234D; font-weight: bold; font-size: 13px;">${parseFloat(product.price).toLocaleString('ru-RU')} ₽</div>`;
                                
                                item.appendChild(img);
                                item.appendChild(info);
                                dropdown.appendChild(item);
                            });
                        } else {
                            // Если ничего не найдено
                            dropdown.innerHTML = '<div style="padding: 15px; text-align: center; color: #777;">Товаров с таким названием нет 😔</div>';
                        }
                        
                        dropdown.style.display = 'block';
                    })
                    .catch(error => console.error('Ошибка поиска:', error));
            }, 300);
        });

        // Скрываем список при клике вне области поиска
        document.addEventListener('click', function(e) {
            if (!searchInput.contains(e.target) && !dropdown.contains(e.target)) {
                dropdown.style.display = 'none';
            }
        });
        
        // Показываем список снова при фокусе
        searchInput.addEventListener('focus', function() {
             if (this.value.trim().length >= 2 && dropdown.innerHTML !== '') {
                 dropdown.style.display = 'block';
             }
        });
    }
});