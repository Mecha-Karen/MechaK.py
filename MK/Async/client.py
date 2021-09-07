import asyncio
import os
import typing as tp     ## Nobody make a joke here.
import aiohttp
import base64
import io

from .. import errors

__all__ = (
    "Client"
)

try:
    import aiofiles
except ImportError:
    import warnings
    warnings.warn('`aiofiles` is not installed - Using default file opener which is sync\npip install aiofiles', errors.APIWarning)
    aiofiles = None

try:
    from requests.utils import requote_uri
except ImportError:
    import warnings
    warnings.warn('`requests` is not installed - Maths endpoint may be affected\npip install requests', errors.APIWarning)
    requote_uri = None

class Client:
    __slots__ = ('token', 'session', 'loop', 'base', 'path', 'filter_uri')
    
    def __init__(self, token: str, path: str = None, session: aiohttp.ClientSession = None, loop: asyncio.AbstractEventLoop = None,
                 *, filter_uri: bool = True, ver: str = 'v1'
                ) -> None:
        r"""
        Make requests to each endpoint and filter how you would like it to handle the requests, this client is async so ``await`` syntax is required when calling each endpoint.
        
        Parameters
        ----------
        token:`class:str`:Your API access token
        path:`class:Optional[Union[bytes, str, os.Pathlike]]`:Default path to save your files, defaults to your current working directory
        session:`class:Optional[ClientSession]`:An aiohttp session to make requests from, creates a new session if not provided
        loop:`class:Optional[AbstractEventLoop]`:An asyncio event loop to create the new session if applicable, uses `get_event_loop` if not provided
        filter_url:`class:Optional[bool]:`:Option to use `/endpoint` instead of `?filter=...` when making image requests
        
        .. versionadded::
            2.0a
        ver:`class:Optional[str]:`:Change the API endpoint version to make requests on
        
        .. versionadded::
            2.0a
        """
        
        self.token = token
        self.base = f'https://api.mechakaren.xyz/{ver}/'

        loop = loop or asyncio.get_event_loop()
        self.loop = loop
        
        self.session = session or aiohttp.ClientSession(loop = loop)
        self.path = path
        self.filter_uri = filter_uri

    async def image(self, filter: str, image_url: str, authorization: str = None, path: str = os.getcwd(), save: bool = False,
                    filename: str = 'result', extension: str = '.png', raw: bool = False, override_raw: bool = False) -> tp.Union[io.BytesIO, str, None, dict]:
        r"""
        Make a request to the image endpoint

        Parameters
        ---------------
        filter:`class: str`: The endpoint to ping e.g. Invert / Flip etc...
        image_url:`class: str`: Image to actually edit - Best to use .png
        authorization:`class: str`: Optional feature to overwrite the token provided when iniating a client
        path:`class: str`: New path to save the file - Overwrites the path from the client
        save:`class: bool`: Option to save the result image from the API to a file
        filename:`class: str`: Option to rename the file being saved - Only applicable if `save` is set a True
        extension:`class: str`: Option to change the file extension - overwrites the current option
        raw:`class: bool`: Returns a dict with the filtered response + the raw response
        override_raw:`class: bool`: Return just the response

        returns: tp.Union[str, io.BytesIO, None]:
            Returns a string if your saving it to a file - Path to the file
            Returns the BytesIO object if your not saving it
            Returns `None` if there was an error in the request
        """
        base = self.base
        
        if not self.filter_uri:
            base += f'image?filter={filter}'
        else:
            base += f'image/{filter}'
        authorization = authorization or self.token

        response = await self.session.get(
            base, headers = {'Authorization': authorization}, json = {'source_url': image_url}
            )
        if override_raw:
            return response

        if response.status != 200:
            error = await response.json()
            errors.raise_error(error)

        result = await response.read()

        if save:
            if response.content_type == 'image/gif':
                temp_ext = '.gif'
            elif response.content_type == 'text/plain':
                # Endpoints such as `asciify` return images as text
                temp_ext = '.txt'
            else:
                temp_ext = '.png'
            extension = extension or temp_ext
            path = path or (self.path or './')

            file_path = f'{path}/{filename}{extension}'
            
            if not aiofiles:
                with open(file_path, 'wb') as file:
                    file.write(result)
            else:
                async with aiofiles.open(file_path, 'wb') as file:
                    await file.write(result)

            return file_path if not raw else {'filtered': filepath, 'response': response}

        return io.BytesIO(result) if not raw else {'filtered': io.BytesIO(result), 'response': response}

    async def chatbot(self, message: str, authorization: str = None, true_json: bool = False,
                      json_: bool = False, raw: bool = False, override_raw: bool = False) -> tp.Union[None, str, dict]:
        r"""
        Make a request to the chatbot endpoint

        Parameters
        ----------------
        message:`class: str`: The message to be used by the chatbot
        authorization:`class: str`: Optional feature to overwrite the token provided when iniating a client
        true_json:`class: bool`: Return just the json which was recieved by API
        json_:`class: bool`: Return just the json which was recieved by the API - Bypasses any errors
        raw:`class: bool`: Return a dict with the filtered response + the raw response
        override_raw:`class: bool`: Return just the raw response
        """
        base = self.base
        base += f'chatbot'
        authorization = authorization or self.token

        response = await self.session.get(
            base, headers = {'Authorization': authorization}, json = {'message': message}
            )
        if override_raw:
            return response

        if json_:
            return await response.json()

        if response.status != 200:
            error = await response.json()
            errors.raise_error(error)

        result = await response.json()

        if true_json:
            return result

        return result['response']['answer'] if not raw else {'filtered': result['response']['answer'], 'response': response}

    async def math(self, equation: str, use_url: bool = False,
                   true_json: bool = False, json_: bool = False,
                   raw: bool = False, override_raw: bool = False) -> tp.Union[str, dict, None]:
        r"""
        Make a request to the math endpoint

        Parameters
        ----------------
        equation:`class: str`: Equation to be parsed
        use_url:`class: str`: Instead of nesting the equation in the response it shoves it in the URL
        true_json:`class: bool`: Return just the json which was recieved by API
        json_:`class: bool`: Return just the json which was recieved by the API - Bypasses any errors
        raw:`class: bool`: Return a dict with the filtered response + the raw response
        override_raw:`class: bool`: Return just the raw response
        """
        base = self.base
        base += 'math'

        if use_url:
            base += '?equation={}'.format(equation)
            try:
                base = await self.loop.run_in_executor(None, requote_uri, base)
                base = base.result()
            except AttributeError as error:
                raise errors.APIException('Requests module is needed to use the extension `use_url`')

            response = await self.session.get(base)

        else:
            response = await self.session.get(base, json={'equation': equation})

        if override_raw:
            return response

        if json_:
            return await response.json()

        if response.status != 200:
            error = await response.json()
            errors.raise_error(error)

        result = await response.json()

        if true_json:
            return result

        return result['Results']['Output'] if not raw else {'filtered': result['Results']['Output'], 'response': response}

    async def anime(self, category: str, authorization: str = None,
                    true_json: bool = False, json_: bool = False,
                    raw: bool = False, override_raw: bool = False) -> tp.Union[str, dict, None]:
        r"""
        Make a request to the anime endpoint

        Parameters
        ----------------
        category:`class: str`: Specific category to get a response from
        authorization:`class: str`: Optional feature to overwrite the token provided when iniating a client
        true_json:`class: bool`: Return just the json which was recieved by API
        json_:`class: bool`: Return just the json which was recieved by the API - Bypasses any errors
        raw:`class: bool`: Return a dict with the filtered response + the raw response
        override_raw:`class: bool`: Return just the raw response
        """
        base = self.base
        base += 'anime?category={}'.format(category)
        authorization = authorization or self.token

        response = await self.session.get(base, headers = {'Authorization': authorization})

        if override_raw:
            return response

        json = await response.json()

        if json_:
            return json

        if response.status != 200:
            errors.raise_error(json)

        if true_json:
            return json

        return json['data'][0] if not raw else {'filtered': json['data'][0], 'response': response}

    async def __aexit__(self, *args, **kwargs) -> None:
        await self.session.close(); del self
        return True

    async def __aenter__(self, *args, **kwargs) -> ".Client":
        return self
