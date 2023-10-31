import os

from moviepy.editor import VideoFileClip, concatenate_videoclips
import moviepy.editor as mp
from telegram import Update, InputMediaVideo
from telegram.ext import CallbackContext

async def start(update: Update, context: CallbackContext):
    await update.message.reply_text("Отправьте мне видео, и я преобразую его в видеокружок.")

async def process_video(update: Update, context: CallbackContext):
    video_file = await context.bot.getFile(update.message.video.file_id)
    await video_file.download_to_drive("input_video.mp4")

    # Отправлять состояние обработки видео
    await context.bot.send_chat_action(chat_id=update.message.chat_id, action="RECORD_VIDEO_NOTE")

    # Prеобразование видео в видеокружок
    input_video = mp.VideoFileClip("input_video.mp4")
    w, h = input_video.size
    circle_size = 360
    aspect_ratio = float(w) / float(h)
    
    if w > h:
        new_w = int(circle_size * aspect_ratio)
        new_h = circle_size
    else:
        new_w = circle_size
        new_h = int(circle_size / aspect_ratio)
        
    resized_video = input_video.resize((new_w, new_h))
    output_video = resized_video.crop(x_center=resized_video.w/2, y_center=resized_video.h/2, width=circle_size, height=circle_size)
    output_video.write_videofile("output_video.mp4", codec="libx264", audio_codec="aac", bitrate="5M")

    # Отправка видеокружка в чат
    with open("output_video.mp4", "rb") as video:
        await context.bot.send_video_note(chat_id=update.message.chat_id, video_note=video, duration=int(output_video.duration), length=circle_size)

    # Удаление видео с сервера
    os.remove("input_video.mp4")
    os.remove("output_video.mp4")
