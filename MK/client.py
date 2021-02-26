import asyncio
import random
import re
import typing as tp ## Nobody make a joke here.
import aiohttp
import base64

from .errors import *

__all__ = (
    "Client"
)

async def get_bytes(_decoded: str):
    encoded = _decoded.encode('utf-8')  ## Originally decoded so its a string
    binary = base64.b64decode(encoded)
    return binary

class Client:
    __slots__ = ('token', 'session', 'loop', 'base')
    
    def __init__(self, token: str, session: aiohttp.ClientSession = None, loop: asyncio.AbstractEventLoop = None) -> None:
        self.token = token
        self.base = 'https://api.mechakaren.xyz/'
        self.session = session or aiohttp.ClientSession(loop = loop or asyncio.get_event_loop())
        
    async def image(self, _filter: str, image_url: str) -> tp.Union[bytes, str]:
        new_url = self.base
        new_url += 'v1/image?filter={}'.format(_filter.lower())
        
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
        _bytes = await get_bytes(image)
        return _bytes
            
    async def math(self, equation: str) -> str:
        new_url = self.base
        new_url += 'v1/math'
        
        resp = await self.session.post(new_url, json={'equation': equation}, headers = {'Authorization': self.token})
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
        return resp.json()['output']
    
    async def chatbot(self, message: str) -> str:
        new_url = self.base
        new_url += 'v1/chatbot'
        
        resp = await self.session.post(new_url, data={'message': message}, headers = {'Authorization': self.token})
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
        return resp.json()['output']
        
        
