from aiogram import Router, F
from aiogram.types import Message

from harmony_hound.presentation.telegram.keyboards.main_keyboards import start_keyboard

user_router = Router()

@user_router.message(F.text == "ℹ️ Info")
async def info (
        message: Message
):
    builder = start_keyboard(message)

    return await message.answer(
        "Hi, I'm Harmony Hound, and I can recognize songs, pretty cool, huh ?\n\n\
  What you can do:\n\
  \t\t 1. You can send me an audio/video file from your device\n\
  \t\t 2. Record a Telegram audio or video message in bottom\n\
  \t\t\t\t   right and capture music playing around you\n\n\
  Constraints:\n\
  \t\t 1. Minimal file duration accepted is 5 seconds\n\
  \t\t 2. Maximal file size is 100 Mb\n\
  \t\t 3. Optimal duration for uploaded file\n\
  \t\t\t\t   is 10-15 second (file with longer duration will be shorted)",
        reply_markup=builder.as_markup(resize_keyboard=True)
    )

@user_router.message(F.text == "💁‍♂️ Help")
async def help(
        message: Message
):
    builder = start_keyboard(message)

    return await message.answer(
        "Drop any audio file to the bot in the chat, "
        "wait for a couple of seconds, and enjoy your results!",
        reply_markup=builder.as_markup(resize_keyboard=True)
    )