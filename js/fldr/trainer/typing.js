const texts = [
    'Съешь ещё этих мягких французских булок, да выпей чаю.',
    'Слепая печать — полезный навык.',
    'Быстрая печать экономит время.',
    'Тренируйтесь каждый день!',
    'Клавиатура — ваш инструмент.',
    'Успехов в обучении!',
    'В лесу родилась ёлочка, в лесу она росла.',
    'Каждый охотник желает знать, где сидит фазан.',
    'Съешь ещё этих мягких французских булок, да выпей чаю.',
    'Широкая электрификация южных губерний даст мощный толчок подъёму сельского хозяйства.',
    'В чащах юга жил бы цитрус? Да, но фальшивый экземпляр!',
    'Любя, съешь щипцы, — вздохнёт мэр, — кайф жгуч.',
    'Эх, чужак! Общий съём цен шляп (юфть) — вдрызг!',
    'Пять ярких чаек съели шесть булок, взяв джем.',
    'Дружба начинается с улыбки.',
    'Зима. Мороз. Солнце ярко светит.',
    'Быстро летит время, когда занят делом.',
    'Ученье — свет, а неученье — тьма.',
    'На дворе трава, на траве дрова.',
    'Лёгкий бриз колышет зелёные листья.',
    'Прыгучий ёж шёл вдоль ручья.'
];

let currentText = '';
let startTime = null;
let errorCount = 0;
let finished = false;

const textToType = document.getElementById('text-to-type');
const userInput = document.getElementById('user-input');
const speedStat = document.getElementById('speed');
const errorsStat = document.getElementById('errors');
const restartBtn = document.getElementById('restart-btn');

function getRandomText() {
    return texts[Math.floor(Math.random() * texts.length)];
}

function startTest() {
    currentText = getRandomText();
    textToType.innerHTML = '';
    for (let i = 0; i < currentText.length; i++) {
        const span = document.createElement('span');
        span.textContent = currentText[i];
        textToType.appendChild(span);
    }
    userInput.value = '';
    errorCount = 0;
    finished = false;
    startTime = null;
    speedStat.textContent = 'Скорость: 0 зн/мин';
    errorsStat.textContent = 'Ошибки: 0';
    userInput.disabled = false;
    userInput.focus();
}

userInput.addEventListener('input', () => {
    if (finished) return;
    if (!startTime) startTime = Date.now();
    const value = userInput.value;
    let errors = 0;
    for (let i = 0; i < currentText.length; i++) {
        const charSpan = textToType.children[i];
        if (value[i] == null) {
            charSpan.className = '';
        } else if (value[i] === currentText[i]) {
            charSpan.className = 'correct';
        } else {
            charSpan.className = 'incorrect';
            errors++;
        }
    }
    errorCount = errors;
    errorsStat.textContent = `Ошибки: ${errorCount}`;
    // Скорость
    const elapsed = (Date.now() - startTime) / 1000 / 60; // минуты
    const speed = elapsed > 0 ? Math.round(value.length / elapsed) : 0;
    speedStat.textContent = `Скорость: ${speed} зн/мин`;
    // Проверка окончания
    if (value === currentText) {
        finished = true;
        userInput.disabled = true;
        speedStat.textContent += ' (Готово!)';
    }
});

restartBtn.addEventListener('click', startTest);

// Стили для подсветки
const style = document.createElement('style');
style.textContent = `
    .correct { color: #4a90e2; }
    .incorrect { color: #e94f4f; background: #ffeaea; border-radius: 2px; }
`;
document.head.appendChild(style);

// Запуск при загрузке
window.addEventListener('DOMContentLoaded', startTest); 