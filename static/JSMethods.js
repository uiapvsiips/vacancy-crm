window.onload = function() {
    // Получаем кнопку "Добавить вакансию"
    const addJobButton = document.querySelector('#add-job-btn');

    // Получаем контейнер с формой вакансии
    const jobFormContainer = document.querySelector('#job-form-container');

    // Добавляем обработчик клика на кнопку
    addJobButton.addEventListener('click', function() {
        // Если контейнер скрыт, показываем его плавно
        if (jobFormContainer.style.display == '') {
            jobFormContainer.style.display = 'block';
            jobFormContainer.style.opacity = 0;
            let opacity = 0;
            const intervalId = setInterval(() => {
                if (opacity < 1) {
                    opacity += 0.05;
                    jobFormContainer.style.opacity = opacity;
                } else {
                    clearInterval(intervalId);
                }
            }, 30);
        } else { // Иначе скрываем контейнер плавно
            let opacity = 1;
            const intervalId = setInterval(() => {
                if (opacity > 0) {
                    opacity -= 0.05;
                    jobFormContainer.style.opacity = opacity;
                } else {
                    clearInterval(intervalId);
                    jobFormContainer.style.display = '';
                }
            }, 30);
        }
    });
};