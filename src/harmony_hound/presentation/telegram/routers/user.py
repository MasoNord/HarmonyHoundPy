import os
import uuid
from pathlib import Path

from aiogram import Router, F
from aiogram.types import Message
from aiogram.filters.command import Command

from harmony_hound.application.common.utils import get_project_root, get_static_root
from harmony_hound.main.config import bot
from harmony_hound.presentation.telegram.keyboards.main_keyboards import start_keyboard
from harmony_hound.presentation.telegram.services.google_drive_service import GoogleDriveService
from harmony_hound.presentation.telegram.services.recognition_service import RecognitionService

user_router = Router()

SCOPES = ["https://www.googleapis.com/auth/drive.metadata.readonly", "https://www.googleapis.com/auth/drive.file"]


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

@user_router.message(F.voice)
async def audio_processing(message: Message):
    google_drive_service = GoogleDriveService()
    recognition_service = RecognitionService()

    voice_id = message.voice.file_id

    file = await bot.get_file(voice_id)

    file_path = file.file_path

    file_type = message.voice.mime_type.split("/")[1]
    file_name = str(uuid.uuid4()) + "." + file_type

    print(f"voice file id {message.voice.file_id}")
    print(f"file_path: {file_path}")
    print(f"file_type: {file_type}")
    print(f"file_name: {file_name}")

    full_file_path = get_static_root() / file_name

    await bot.download_file(file_path, full_file_path)

    file_id = google_drive_service.upload_file(full_file_path)

    web_view_link = google_drive_service.get_web_view_link(file_id)

    google_drive_service.apply_share_flag(file_id)

    # --- Recognise song by web_view_link ---
    result = recognition_service.recognise_song(web_view_link)

    google_drive_service.delete_file_by_id(file_id)

    os.remove(full_file_path)

    print(str(result))

    return await message.answer("Success!")

@user_router.message(F.video_note)
async def video_processing(message: Message):
    google_drive_service = GoogleDriveService()
    recognition_service = RecognitionService()

    video_id = message.video_note.file_id

    print(f"Video Note file ID{video_id}")

    file = await bot.get_file(video_id)

    file_path = file.file_path

    file_type = "mp4"
    file_name = str(uuid.uuid4()) + "." + file_type

    full_file_path = get_static_root() / file_name

    await bot.download_file(file_path, full_file_path)

    file_id = google_drive_service.upload_file(full_file_path)

    web_view_link = google_drive_service.get_web_view_link(file_id)

    google_drive_service.apply_share_flag(file_id)

    # --- Recognise song by web_view_link ---
    result = recognition_service.recognise_song(web_view_link)

    google_drive_service.delete_file_by_id(file_id)

    os.remove(full_file_path)

    print(str(result))

    return await message.answer("Success!")

@user_router.message(F.video)
async def video_file_processing(message: Message):
    google_drive_service = GoogleDriveService()
    recognition_service = RecognitionService()

    video_id = message.video.file_id

    video = await bot.get_file(video_id)

    file_path = video.file_path

    file_type = message.video.mime_type.split('/')[1]
    file_name = str(uuid.uuid4()) + '.' + file_type

    print(f"video file id {message.video.file_id}")
    print(f"file_path: {file_path}")
    print(f"file_type: {file_type}")
    print(f"file_name: {file_name}")

    full_file_path = get_static_root() / file_name

    await bot.download_file(file_path, full_file_path)

    file_id = google_drive_service.upload_file(full_file_path)

    web_view_link = google_drive_service.get_web_view_link(file_id)

    google_drive_service.apply_share_flag(file_id)

    # --- Recognise song by web_view_link ---
    result = recognition_service.recognise_song(web_view_link)

    google_drive_service.delete_file_by_id(file_id)

    os.remove(full_file_path)

    print(str(result))

    return await message.answer("Success!")

