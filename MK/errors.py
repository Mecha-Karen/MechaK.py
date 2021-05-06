class HTTPException(Exception):
  def __new__(cls, message: str) -> object:
    return super().__new__(cls, message)
    
class APIException(HTTPException):
  pass

class APIWarning(Warning):
  pass

def raise_error(response) -> None:
  code = response['code']
  error = response['error']

  raise APIException(f'{code}: {error}')
