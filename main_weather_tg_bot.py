import requests
import datetime
from config import tg_bot_token, open_weather_token
from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor

bot = Bot(token=tg_bot_token)
dp = Dispatcher(bot)

@dp.message_handler(commands=["start"])
async def start_command(message: types.Message):
    await message.reply("Привет, напиши мне название города, чтобы узнать какая погодка сегодня!")

@dp.message_handler()
async def get_weather(message: types.Message):
    code_to_smile = {

        "Clear": "\U00002600 Ясно \U00002600",
        "Clouds": "\U00002601 Облачно \U00002601",
        "Rain": "\U00002614 Дождь \U00002614",
        "Drizzle": "\U00002614 Дождь \U00002614",
        "Thunderstorm": "\U000026A1 Гроза \U000026A1",
        "Snow": "\U0001F328 Снег \U0001F328",
        "Mist": "\U0001F32B Туман \U0001F32B"

    }

    try:
        r = requests.get(
          f"https://api.openweathermap.org/data/2.5/weather?q={message.text}&appid={open_weather_token}&units=metric&lang=ru"
        )
        data = r.json()

        city = data["name"]
        cur_weather = data["main"]["temp"]
        weather_description = data["weather"][0]["main"]
        if weather_description in code_to_smile:
            wd = code_to_smile[weather_description]
        else:
            wd = "Посмотри в окно, не пойму что за погода!"

        humidity = data["main"]["humidity"]
        pressure = data["main"]["pressure"] // 1.33
        wind = data["wind"]["speed"]
        sunrise_timestamp = datetime.datetime.fromtimestamp(data["sys"]["sunrise"])
        sunset_timestamp = datetime.datetime.fromtimestamp(data["sys"]["sunset"])
        length_of_the_day = datetime.datetime.fromtimestamp(data["sys"]["sunset"]) - datetime.datetime.fromtimestamp(
            data["sys"]["sunrise"])
        await message.reply(f"\U0001F30F{datetime.datetime.now().strftime('%d-%m-%Y %H:%M')}\U0001F4C5\n"
              f"\U000025AA Погода в городе {city}\n\U000025AA Температура: {cur_weather} °С {wd}\n"
              f"\U000025AA Влажность: {humidity} %\U0001F4A6\n\U000025AA Давление: {pressure} мм рт.ст.\n"
              f"\U000025AA Скорость ветра: {wind} м/с\n\U000025AA Рассвет: {sunrise_timestamp}\U0001F304\n"
              f"\U000025AA Закат: {sunset_timestamp}\U0001F305\n"
              f"\U000025AA Продолжительность дня: {length_of_the_day}\n"
              f"Хорошего дня!\U0001F49C"
              )

    except :
        await message.reply("\U00002620 Проверьте название города! \U00002620")

if __name__ == '__main__':
    executor.start_polling(dp)

