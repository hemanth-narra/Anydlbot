import os
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton

@Client.on_message(filters.command("files"))
async def handle_files_command(client, message):
    # Set the path to the root directory
    path = "/DATA/Media/Downloads/"
    
    # Create an inline keyboard
    keyboard = InlineKeyboardMarkup()
    
    # Recursively traverse the directory tree
    for root, dirs, files in os.walk(path):
        for file in files:
            # Get the relative path to the file
            relpath = os.path.relpath(os.path.join(root, file), path)
            
            # Check if the file is a video
            if relpath.endswith((".mp4", ".avi", ".mov")):
                # Add a button for the file
                keyboard.add(InlineKeyboardButton(relpath, callback_data=f"file:{relpath}"))
    
    # Send the message with the inline keyboard
    await message.reply_text("Video files:", reply_markup=keyboard)

@Client.on_callback_query(filters.regex("^file:"))
async def handle_file_callback(client, callback_query):
    # Get the relative path to the selected file
    relpath = callback_query.data.split(":", 1)[1]
    
    # Set the path to the root directory
    path = "/DATA/Media/Downloads/"
    
    # Get the absolute path to the selected file
    abspath = os.path.join(path, relpath)
    
    # Send the selected file to the user as a video
    await client.send_video(callback_query.from_user.id, abspath)
