import logging
import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder
from aiogram.fsm.context import FSMContext
from aiogram import Router

# Замените на ваш токен
TOKEN = "7710438070:AAEBhq6RYwBIz3_3FHtv_EBWaaiOCg7PcBY"

# Список людей в формате "Фамилия И.О."
people = [
    "Бурма В.Л.",
    "Волошин Д.А.",
    "Дзиковский М.И.",
    "Долгушин Л.Ю.",
    "Ивашкевич М.А.",
    "Костин А.Э.",
    "Кудряшов А.А.",
    "Кучерук Д.В.",
    "Лесникова Д.С.",
    "Лидер А.Н.",
    "Лобанов А.В.",
    "Лучкин В.С.",
    "Малахов С.Д.",
    "Миличкина К.Е.",
    "Морщинин А.Н.",
    "Николаев С.Е.",
    "Павленко В.А.",
    "Петушков И.А.",
    "Смирнов А.В.",
    "Сорокин Ю.М.",
    "Тимошенко В.А.",
    "Фролов Н.Е.",
    "Чернорай В.Д.",
    "Шаронов Ю.В.",
]

# Хранение отметок пользователей
attendance = set()

# Настройка логирования
logging.basicConfig(level=logging.INFO)

# Создаем бота и диспетчер
bot = Bot(token=TOKEN)
dp = Dispatcher()

# Создаем маршрутизатор
router = Router()


# Функция для генерации клавиатуры
def generate_keyboard():
    builder = ReplyKeyboardBuilder()
    for person in people:
        status = "✅" if person in attendance else "❌"
        builder.button(text=f"{status} {person}")
    builder.button(text="Отметить")
    builder.adjust(1)  # Одна кнопка на строку
    return builder.as_markup(resize_keyboard=True)


# Обработчик команды /start
@router.message(Command("start"))
async def start_handler(message: types.Message):
    global attendance
    attendance.clear()  # Очищаем отметки при запуске
    await message.answer("Отметьте присутствующих:", reply_markup=generate_keyboard())


# Обработчик кнопок
@router.message()
async def button_handler(message: types.Message):
    global attendance
    text = message.text

    if text.startswith("✅") or text.startswith("❌"):
        name = text[2:]  # Убираем символы статуса
        if name in people:  # Проверяем, что имя есть в списке
            if name in attendance:
                attendance.remove(name)
            else:
                attendance.add(name)
            await message.answer("Обновлено!", reply_markup=generate_keyboard())
        else:
            await message.answer("Ошибка: Некорректное имя.")

    elif text == "Отметить":
        if attendance:
            response = "Присутствуют:\n" + "\n".join(f"{i+1}. {name}" for i, name in enumerate(attendance))
        else:
            response = "Никто не отмечен."
        await message.answer(response)


# Главная функция запуска бота
async def main():
    dp.include_router(router)  # Подключаем маршрутизатор
    await bot.delete_webhook(drop_pending_updates=True)  # Удаляем старые вебхуки
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
