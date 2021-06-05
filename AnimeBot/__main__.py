from pyrogram import  idle, Client
from AnimeBot import goth
from AnimeBot.plugins import ALL_MODULES
import importlib

for module in ALL_MODULES:
    imported_module = importlib.import_module("AnimeBot.plugins." + module)
    importlib.reload(imported_module)


if __name__ == "__main__":
    goth.start()
    idle()
