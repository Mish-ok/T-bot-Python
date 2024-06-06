import telebot
import pandas as pd

# Вставьте ваш токен бота Telegram
TELEGRAM_BOT_TOKEN = 'YOUR TOKEN'

# Инициализация бота
bot = telebot.TeleBot(TELEGRAM_BOT_TOKEN)

# Загрузка данных из файла Excel
try:
    df = pd.read_excel('Err.xlsx')
    print("Файл Excel загружен успешно.")
    print("Столбцы в файле Excel:", df.columns.tolist())

    # Переименовывание столбцов для соответствия новым названиям
    df.rename(columns={'B': 'Описание', 'С': 'Решение'}, inplace=True)
    # Удаление пробелов в начале и конце строк в колонке A
    df['A'] = df['A'].astype(str).str.strip()
except FileNotFoundError:
    print("Ошибка: файл 'your_file.xlsx' не найден.")
    exit(1)
except Exception as e:
    print(f"Ошибка при чтении файла Excel: {e}")
    exit(1)

# Обработчик команды /start
@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "Привет! Пиши скорее код ошибки, поиогу расшифровать.")

# Обработчик текстовых сообщений
@bot.message_handler(func=lambda message: True)
def handle_message(message):
    query = message.text.strip()
    print(f"Получен запрос: {query}")

    # Преобразование запроса к строке и удаление пробелов
    query = str(query).strip()

    # Поиск в колонке A
    result = df[df['A'] == query]

    if not result.empty:
        for _, row in result.iterrows():
            model = f"Модель: {row['Модель']}"
            module = f"Модуль: {row['Модуль']}"
            description = f"Описание: {row['Описание']}"
            solution = f"Решение: {row['Решение']}"
            
            bot.reply_to(message, model)
            bot.reply_to(message, module)
            bot.reply_to(message, description)
            bot.reply_to(message, solution)
    else:
        bot.reply_to(message, "Данные не найдены.")
        print(f"Запрос '{query}' не найден в данных.")

# Запуск бота
if __name__ == '__main__':
    print("Бот запущен и готов к работе.")
    bot.polling(none_stop=True)
