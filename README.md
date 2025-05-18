# bignugget

**Телеграм-бот для оповіщення (поки немає) про тривоги та генерації карти активних областей України**

---

## Опис

`bignugget` — легкий Telegram-бот на Python, який:
- Періодично запитує API тривог в Україні та зберігає їх у локальному JSON (`alerts_data.json`)
- Генерує кольорову карту України з підсвіткою областей, де оголошено тривогу
- Надсилає користувачу меню з двома діями:  
  1. 🗺️ Показати актуальну мапу тривог  
  2. 🚨 Перевірити поточний список тривог у текстовому вигляді  
- Працює на базі **aiogram** та **Pillow**

## Вимоги

- Python 3.12 або вище  
- Бібліотеки: aiogram, Pillow, python-dotenv, alerts-in-ua

---

## Швидкий старт

1. **Клонування репозиторію**  
   ```bash
   git clone https://github.com/mLeviGen/bignugget.git
   cd bignugget
   ```

2. **Створіть віртуальне середовище**  
   ```bash
   python3.12 -m venv .venv
   ```
   Linux/macOS
   ```bash
   source .venv/bin/activate
   ```
   Windows
   ```bash
   .\.venv\Scripts\activate
   ```
3. **Встановіть залежності**
   ```bash
   pip install --upgrade pip
   pip install aiogram Pillow python-dotenv alerts-in-ua
   ```
4. **Налаштування змінних оточення**
   Створіть файл .env у корені проєкту з такими параметрами:
   ```bash
   TELEGRAM_BOT_TOKEN=<ваш токен від BotFather>
   ALERTS_IN_UA_TOKEN=<API-ключ для сервісу alerts_in_ua>
   ```
5. **Запуск бота**
   ```bash
   python main.py
   ```

## Додатково

- Щоб змінити інтервал оновлення тривог, відкоригуйте затримку в `alerts_event.py` (рядок з `asyncio.sleep(7)`).
- Для кастомізації вигляду карти змініть шаблон `app/images/UK2.png` та папку масок `app/images/menus/*.png`.
- Використовуйте logging для налагодження — рівень можна змінити в `main.py` через `logging.basicConfig(level=logging.DEBUG)`.

