// JavaScript для проекта Reptile Interactive Cursor

class ReptileCursor {
  constructor() {
    this.mouseX = 0;
    this.mouseY = 0;
    this.reptileX = 0;
    this.reptileY = 0;
    this.isMoving = false;
    this.trail = [];
    this.maxTrailLength = 20;

    this.init();
  }

  init() {
    this.createReptile();
    this.bindEvents();
    this.animate();
  }

  createReptile() {
    // Создаем контейнер для рептилии
    const container = document.createElement('div');
    container.className = 'reptile-container';
    document.body.appendChild(container);

    // Создаем SVG рептилии
    const svg = document.createElementNS('http://www.w3.org/2000/svg', 'svg');
    svg.className = 'reptile-svg';
    svg.setAttribute('viewBox', '0 0 200 200');
    svg.innerHTML = this.createReptileSkeleton();

    container.appendChild(svg);
    this.reptileElement = svg;
  }

  createReptileSkeleton() {
    return `
            <!-- Голова -->
            <circle cx="100" cy="50" r="15" class="reptile-skeleton"/>
            <circle cx="95" cy="45" r="2" class="reptile-skeleton"/>
            <circle cx="105" cy="45" r="2" class="reptile-skeleton"/>
            
            <!-- Позвоночник -->
            <path d="M 100 65 Q 90 80 85 100 Q 80 120 75 140 Q 70 160 65 180" class="reptile-skeleton"/>
            
            <!-- Ребра -->
            <path d="M 85 70 Q 70 75 60 80" class="reptile-skeleton"/>
            <path d="M 85 80 Q 70 85 60 90" class="reptile-skeleton"/>
            <path d="M 85 90 Q 70 95 60 100" class="reptile-skeleton"/>
            <path d="M 85 100 Q 70 105 60 110" class="reptile-skeleton"/>
            
            <!-- Передние лапы -->
            <path d="M 85 70 Q 70 60 60 50 Q 50 40 40 35" class="reptile-skeleton"/>
            <path d="M 40 35 Q 35 30 30 25 Q 25 20 20 15" class="reptile-skeleton"/>
            <path d="M 40 35 Q 45 30 50 25 Q 55 20 60 15" class="reptile-skeleton"/>
            
            <path d="M 115 70 Q 130 60 140 50 Q 150 40 160 35" class="reptile-skeleton"/>
            <path d="M 160 35 Q 165 30 170 25 Q 175 20 180 15" class="reptile-skeleton"/>
            <path d="M 160 35 Q 155 30 150 25 Q 145 20 140 15" class="reptile-skeleton"/>
            
            <!-- Задние лапы -->
            <path d="M 75 120 Q 60 110 50 100 Q 40 90 30 85" class="reptile-skeleton"/>
            <path d="M 30 85 Q 25 80 20 75 Q 15 70 10 65" class="reptile-skeleton"/>
            <path d="M 30 85 Q 35 80 40 75 Q 45 70 50 65" class="reptile-skeleton"/>
            
            <path d="M 125 120 Q 140 110 150 100 Q 160 90 170 85" class="reptile-skeleton"/>
            <path d="M 170 85 Q 175 80 180 75 Q 185 70 190 65" class="reptile-skeleton"/>
            <path d="M 170 85 Q 165 80 160 75 Q 155 70 150 65" class="reptile-skeleton"/>
            
            <!-- Хвост -->
            <path d="M 65 180 Q 60 190 55 200" class="reptile-skeleton"/>
        `;
  }

  bindEvents() {
    // Отслеживание движения мыши
    document.addEventListener('mousemove', (e) => {
      this.mouseX = e.clientX;
      this.mouseY = e.clientY;
      this.isMoving = true;

      // Создаем след
      this.createTrail(e.clientX, e.clientY);

      // Сброс флага движения через небольшую задержку
      clearTimeout(this.movementTimeout);
      this.movementTimeout = setTimeout(() => {
        this.isMoving = false;
      }, 100);
    });

    // Обработка клика
    document.addEventListener('click', (e) => {
      this.onClick(e.clientX, e.clientY);
    });

    // Обработка выхода мыши за пределы окна
    document.addEventListener('mouseleave', () => {
      this.isMoving = false;
    });

    // Обработка входа мыши в окно
    document.addEventListener('mouseenter', () => {
      this.isMoving = true;
    });
  }

  createTrail(x, y) {
    const trailDot = document.createElement('div');
    trailDot.className = 'reptile-trail';
    trailDot.style.left = x + 'px';
    trailDot.style.top = y + 'px';

    document.body.appendChild(trailDot);

    // Удаляем след через 1 секунду
    setTimeout(() => {
      if (trailDot.parentNode) {
        trailDot.parentNode.removeChild(trailDot);
      }
    }, 1000);
  }

  onClick(x, y) {
    // Анимация при клике
    this.reptileElement.classList.add('moving');

    // Создаем эффект волны
    this.createClickEffect(x, y);

    // Убираем класс анимации
    setTimeout(() => {
      this.reptileElement.classList.remove('moving');
    }, 300);
  }

  createClickEffect(x, y) {
    const effect = document.createElement('div');
    effect.style.position = 'fixed';
    effect.style.left = x + 'px';
    effect.style.top = y + 'px';
    effect.style.width = '20px';
    effect.style.height = '20px';
    effect.style.border = '2px solid rgba(255, 255, 255, 0.8)';
    effect.style.borderRadius = '50%';
    effect.style.pointerEvents = 'none';
    effect.style.transform = 'translate(-50%, -50%)';
    effect.style.animation = 'click-ripple 0.6s ease-out forwards';

    // Добавляем CSS анимацию если её нет
    if (!document.getElementById('click-animation')) {
      const style = document.createElement('style');
      style.id = 'click-animation';
      style.textContent = `
                @keyframes click-ripple {
                    0% {
                        transform: translate(-50%, -50%) scale(0);
                        opacity: 1;
                    }
                    100% {
                        transform: translate(-50%, -50%) scale(10);
                        opacity: 0;
                    }
                }
            `;
      document.head.appendChild(style);
    }

    document.body.appendChild(effect);

    setTimeout(() => {
      if (effect.parentNode) {
        effect.parentNode.removeChild(effect);
      }
    }, 600);
  }

  animate() {
    // Плавное следование за курсором
    const ease = 0.15;
    this.reptileX += (this.mouseX - this.reptileX) * ease;
    this.reptileY += (this.mouseY - this.reptileY) * ease;

    // Позиционирование рептилии
    if (this.reptileElement) {
      this.reptileElement.style.left = (this.reptileX - 100) + 'px';
      this.reptileElement.style.top = (this.reptileY - 100) + 'px';

      // Добавляем класс движения
      if (this.isMoving) {
        this.reptileElement.classList.add('moving');
      } else {
        this.reptileElement.classList.remove('moving');
      }
    }

    // Продолжаем анимацию
    requestAnimationFrame(() => this.animate());
  }

  // Метод для изменения стиля рептилии
  changeReptileStyle(style) {
    if (this.reptileElement) {
      this.reptileElement.style.filter = style;
    }
  }

  // Метод для добавления дополнительных эффектов
  addGlowEffect() {
    if (this.reptileElement) {
      this.reptileElement.style.filter = 'drop-shadow(0 0 10px rgba(255, 255, 255, 0.5))';
    }
  }

  // Метод для удаления эффектов
  removeEffects() {
    if (this.reptileElement) {
      this.reptileElement.style.filter = 'none';
    }
  }
}

// Инициализация при загрузке страницы
document.addEventListener('DOMContentLoaded', () => {
  const reptileCursor = new ReptileCursor();

  // Добавляем дополнительные эффекты по желанию
  // reptileCursor.addGlowEffect();

  // Глобальный доступ к объекту (для отладки)
  window.reptileCursor = reptileCursor;
});

// Обработка изменения размера окна
window.addEventListener('resize', () => {
  // Пересчитываем позицию при изменении размера окна
  if (window.reptileCursor) {
    window.reptileCursor.mouseX = window.mouseX || 0;
    window.reptileCursor.mouseY = window.mouseY || 0;
  }
});

// Дополнительные утилиты
const ReptileUtils = {
  // Создание случайного цвета для рептилии
  randomColor() {
    const colors = ['#ffffff', '#00ff00', '#00ffff', '#ff00ff', '#ffff00'];
    return colors[Math.floor(Math.random() * colors.length)];
  },

  // Изменение размера рептилии
  resizeReptile(scale) {
    if (window.reptileCursor && window.reptileCursor.reptileElement) {
      window.reptileCursor.reptileElement.style.transform = `scale(${scale})`;
    }
  },

  // Включение/выключение следа
  toggleTrail() {
    // Можно добавить логику для включения/выключения следа
    console.log('Trail toggled');
  }
};

// Экспорт для использования в других модулях
if (typeof module !== 'undefined' && module.exports) {
  module.exports = { ReptileCursor, ReptileUtils };
}
