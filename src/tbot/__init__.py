import traceback
import os

from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode

from src.config import settings


bot = Bot(token=settings.TELEGRAM_BOT_API_KEY, parse_mode=ParseMode.HTML)
dp = Dispatcher()

# Get the list of all Python files in the module directory
file_list = []
for foldername, subfolders, filenames in os.walk(os.path.dirname(__file__)):
    for filename in filenames:
        if filename.endswith(".py"):
            file_list.append(os.path.join(foldername, filename))

file_list.reverse()

# Import each file as a module
for file_path in file_list:
    filename = os.path.basename(file_path)
    if filename.startswith("__init__.py"):
        continue
    # Remove the ".py" extension
    module_name = file_path.replace('/', '.')[5:-3]
    try:
        __import__(module_name, fromlist=["*"])
    except Exception as e:
        traceback.print_exc()
