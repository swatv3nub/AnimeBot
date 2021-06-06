import os
import time
import logging
from pyrogram import Client, filters
from config import TOKEN, API_ID, API_HASH
from functools import partial
from telegraph import Telegraph

#StartTime for pinging purpose
StartTime = time.time()
#Client
goth = Client(
    ':memory:',
    bot_token=TOKEN,
    api_id=API_ID,
    api_hash=API_HASH,
)
#Command Handler
cmd = partial(filters.command, prefixes=["/", "!"])
#Logger
LOG_FORMAT = (
    '''
    [%(asctime)s.%(msecs)03d] %(filename)s:%(lineno)s
    %(levelname)s: %(message)s''')
logging.basicConfig(
    level=logging.ERROR,
    format=LOG_FORMAT,
    datefmt="%m-%d %H:%M",
    filename="error.log",
    filemode="w",
)
console = logging.StreamHandler()
console.setLevel(logging.ERROR)
formatter = logging.Formatter(LOG_FORMAT)
console.setFormatter(formatter)
logging.getLogger("").addHandler(console)
log = logging.getLogger()
#telegraph for nhentai
telegraph = Telegraph()
telegraph.create_account(short_name="goth")