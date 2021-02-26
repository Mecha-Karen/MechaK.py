class HTTPException(Exception):
  def __init__(self, response: dict):
    self.code = response['code']
    self.message = response['error']
    
class BadRequest(Exception):
  pass

class InternalServerError(Exception):
  pass

class AuthError(Exception):
  pass

class NotFound(Exception):
  pass

class Ratelimit(Exception):
  pass

class MethodError(Exception):
  pass
