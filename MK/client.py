import asyncio
import random
import re
import typing as tp
from urllib.parse import quote, urlencode
import aiohttp
import base64

import .errors

__all__ = (
    "Client"
)

async def get_bytes(_decoded: str):
    encoded = _decoded.encode('utf-8')  ## Originally decoded so its a string
    binary = base64.b64decode(encoded)
    return binary

class Client:
    __slots__ = ('token', 'session', 'loop')
    
    def __init__(self, token: str, session: aiohttp.ClientSession = None, loop: asyncio.AbstractEventLoop = None) -> None:
        self.token = token
        self.base = 'https://mechakaren.xyz/api/'
        self.session = session or aiohttp.ClientSession(loop = loop or asyncio.get_event_loop())
        
    async def image(_filter: str, image_url: str) -> tp.Union[bytes, str]:
        new_url = self.base
        new_url += '?filter={}'.format(_filter.lower())
        
        resp = await self.session.post(new_url, data={'image_url': image_url}, headers = {'Authorization': self.token})
        
        if resp.status == 400:
            raise errors.BadRequest('API Raised an Exception: %s' % await resp.json()['error'])
        if resp.status == 404:
            raise errors.NotFound('API Raised an Exception: %s' % await resp.json()['error'])
        if resp.status == 401 or resp.status == 403:
            raise errors.AuthError('API Raised an Excpetion: %s' % await resp.json()['error'])
        if resp.status == 405:
            raise errors.MethodError('API Raised an Exception: %s' % await resp.json()['error'])
        if resp.status == 429:
            raise errors.Ratelimit('API Raised an Exception: %s' % await resp.json()['error'])
        data = await resp.json()
        image = data['_bytes']
        ## decoded in utf-8, base64
        _bytes = get_bytes(image)
        return _bytes
            
