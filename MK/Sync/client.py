import requests
import os
import typing as tp
from io import BytesIO
from .. import errors

class Client:
    __slots__ = ('token', 'path', 'base')
    
    def __init__(self, token: str, path: str = None) -> None:
        r"""
        Sync Client for the Mecha Karen API

        Parameters
        ----------------
        token:`class: str`: Your API Token
        path:`class: str`: Optional path to save images - Defaults to os.getcwd()
        """
        self.token = token
        self.path = path
        self.base = 'https://api.mechakaren.xyz/v1/'

    def image(self, filter: str, image_url: str, authorization: str = None, path: str = None,
              filename: str = 'result', extension: str = None, save: bool = False,
              raw: bool = False, override_raw: bool = False) -> tp.Any:
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
        base += 'image?filter={}'.format(filter)
        auth = authorization or self.token

        response = requests.post(
            base, headers = {'Authorization': auth},
            json = {'image_url': image_url}
            )

        if override_raw:
            return response

        if response.status_code != 200:
            json = response.json()
            errors.raise_error(json)

        image = response.content

        if save:
            path = (path or self.path) or os.getcwd()

            content_type = response.headers['Content-Type']

            if content_type == 'image/png':
                ext = '.png'
            elif content_type == 'image/gif':
                ext = '.gif'
            else:
                ext = '.text'
            ext = extension or ext
            filepath = f'{path}/{filename}{ext}'

            with open(filepath, 'wb') as file:
                file.write(image)

            return filepath
        io = BytesIO(image)
        return io if not raw else {'filtered': io, 'response': io}

    def chatbot(self, message: str, authorization: str = None, true_json: bool = False,
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

        response = requests.post(
            base, headers = {'Authorization': authorization}, json = {'message': message}
            )
        if override_raw:
            return response
        result = response.json()

        if json_:
            return result

        if response.status_code != 200:
            errors.raise_error(result)

        if true_json:
            return result

        return result['response']['answer'] if not raw else {'filtered': result['response']['answer'], 'response': response}

    def math(self, equation: str, use_url: bool = False,
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
            base = requests.utils.requote_uri(base)

            response = requests.get(base)

        else:
            response = requests.get(base, json={'equation': equation})

        if override_raw:
            return response
        result = response.json()

        if json_:
            return result

        if response.status_code != 200:
            errors.raise_error(result)

        if true_json:
            return result

        return result['Results']['Output'] if not raw else {'filtered': result['Results']['Output'], 'response': response}

    def anime(self, category: str, authorization: str = None,
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

        response = requests.get(base, headers = {'Authorization': authorization})

        if override_raw:
            return response

        json = response.json()

        if json_:
            return json

        if response.status_code != 200:
            errors.raise_error(json)

        if true_json:
            return json

        return json['data'][0] if not raw else {'filtered': json['data'][0], 'response': response}

    def __enter__(self, *args, **kwargs) -> object:
        return self

    def __exit__(self, *args, **kwargs) -> None:
        del self
