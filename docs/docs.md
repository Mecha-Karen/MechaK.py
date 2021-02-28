# Mecha Karen API docs!

#### Endpoints:

Chatbot:
```yaml
UP: False
DOWNTIME: Unknown ... UPTIME: None
  -Cause: "Missing Module :: TENSORFLOW -> ETA: Unknown"
METHOD: POST
JSON DATA FORMAT: {'message': '%MESSAGE%'}

RETURNS:
  {
    "Bearer": USERID,
    "response": {
      "tags": ["greeting", "casual", etc...],
      "callback": "%MESSAGE%",
      "answer": "Hello There..."
    }
  }
  
HEADERS:
  Authorization: $API TOKEN
```
