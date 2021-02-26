import asyncio
import random
import re
import typing as tp
from urllib.parse import quote, urlencode

import .errors

class Client:
    def __init__(self, token: str):
        self.token = token
