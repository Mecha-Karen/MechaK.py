# Mecha Karen API docs!

#### Endpoints:
The API currently has 4 endpoints!
    - 3 UP 
    - 1 DOWN

#### Chatbot:
This endpoint is the chatbot were it allows users to interact with a robot and talk with them

Offers:
Deep analysis of keywords to optimise its responses!
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
  Quick responses and can solve problems
  Worded responses | Not perfect as of now!
  
Soon to come:
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

Current Filters:
  invert<br/>
  equalize <br/>
  grayscale<br/>
  mirror <br/>
  posterize <br/>
  solarize<br/>
  transpose <br/>
  flip<br/>
  blur<br/>
  
  // More coming soon!
  
Notes:
Images returned are encoded in `BASE-64` - Which has been decoded to `UTF-8`
To access the bytes first encode to `UTF-8` then decode the `BASE-64`

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
