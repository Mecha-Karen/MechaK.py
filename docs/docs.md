# Mecha Karen API docs!

#### Endpoints:
The API currently has 4 endpoints!
    - 3 UP 
    - 1 DOWN

#### Chatbot:
This endpoint is the chatbot were it allows users to interact with a robot and talk with them

Offers:
Deep analysis of keywords to optimise its responses!<br/>
If it cannot understand a sentence its automatically logged so my creators can help improve me!!!

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
  
curl example:
    $ curl -XPOST 'https://api.mechakaren.xyz/v1/chatbot' \
    -H "Authorization: $TOKEN" \
    -H "Content-Type: application/json" \
    -d {"message": "Hello"}
```

#### Math:
This endpoint solves simple maths problems for you and understands equations in english such as `one add one`.

Offers:
<br/>
  Quick responses and can solve problems<br/>
  Worded responses | Not perfect as of now!
  
Soon to come:<br/>
  More advanced math equations!
  
```yaml
UP: True
UPTIME: 93.532 %
METHOD: POST
JSON DATA FORMAT: {"equation": "one add one"}

RETURNS:
  {
    "Bearer": USERID,
    "answer": 2
  }
  
HEADERS:
  Authorization: $API TOKEN
  
curl example:
    $ curl -XPOST 'https://api.mechakaren.xyz/v1/math' \
    -H "Authorization: $TOKEN" \
    -H "Content-Type: application/json" \
    -d {"equation": "one add one"}
```

#### Image Manipulation:
Applies various filters to your images.

**Current Filters**:<br/>
  BASIC and one of the fastest to finish:<br>
  ```
  invert
  equalize 
  grayscale
  mirror 
  posterize 
  solarize
  transpose 
  flip
  blur
  ```
  
  Experimental:
  ```
  gamma
  rainbow
  autumn
  twilight
  cartoon
  warp
  cartoon
  bone
  winter
  ocean
  summer
  spring
  cool
  hsv
  hot
  parula
  magma
  plasma
  viridis
  cividis
  twil
  turbo
  green
  ```
  
Notes:
Images returned are encoded in `BASE-64` - Which has been decoded to `UTF-8`<br/>
To access the bytes first encode to `UTF-8` then decode the `BASE-64`

**Example of how to retrieve the image in `python`:**
```py
import requests
import base64

r = requests.post('https://api.mechakaren.xyz/v1/image?filter=invert',
                  json = {'image_url': 'my secret image url'},
                  headers = {'Authorization': 'my secret token'}
                )
json = r.json()
bytes = json['bytes']

with open('./my_file.png', 'wb') as f:
    encoded = bytes.encode('utf-8')
    raw = base64.b64decode(encoded)
    f.write(raw)
```

```yaml
UP: True
UPTIME: 95.3454 %
METHOD: POST
JSON DATA FORMAT: {'image_url': 'URL OF IMAGE'}

RETURNS:
  {
    "Bearer": USERID,
    "bytes": Bytes of the new image
  }
  
HEADERS:
  Authorization: $API TOKEN
  
curl example:
    $ curl -XPOST 'https://api.mechakaren.xyz/v1/image?filter=FILTER HERE' \
    -H "Authorization: $TOKEN" \
    -H "Content-Type: application/json" \
    -d {"image_url": "image url"}
```

#### Anime
Returns gifs and images on a certain category!

Categories:
    SLAP >> WIP :: coming soon<br/>
    kill >> WIP :: Active / Low content -> count 6<br/>
    hug >> WIP :: Active / decent content -> count 40 - 50<br/>
    pat >> WIP :: Active / decent content -> count 40 - 50<br/>
    kiss >> WIP :: Active / decent content -> count 40 - 50<br/>
    
```yaml
UP: True
UPTIME: NOT LOGGED
METHOD: GET

RETURNS:
  {
    "Bearer": USERID,
    "category": "PAT",
    "data": [
        URL
    ]
  }
  
HEADERS:
  Authorization: $API TOKEN
  
curl example:
    $ curl 'https://api.mechakaren.xyz/v1/anime?category=CATEGORY HERE' \
    -H "Authorization: $TOKEN"
