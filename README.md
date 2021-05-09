# MechaK.py
Official API for the Mecha Karen API

Because im lazy to upload to pypi, to get the module `pip install git+https://github.com/Seniatical/MechaK.py/`

## Async Usage:
```py
import asyncio
from MK.Async import Client

async def my_coro():
	client = Client(token='My Secret Token', **kwargs)
	
	...

	## Using with
	async with Client(token='My Secret Token', **kwargs) as client:
		...

asyncio.run(my_coro())
```

## Sync Usage:
```py
from MK.Sync import Client

with Client(*args, *kwargs) as client:
	path = client.image(invert, 'my-url', save=True, path='./Images')

## Define the client using the class
client = Client(*args, **kwargs)

...
```

## Handling the response yourself

**Sync**
```py
from MK.Sync import Client

with Client(*args, **kwargs) as client:
	with client.image('FILTER', 'IMAGE-URL', override_raw = True) as response:
		...
```

**Async**
```py
from MK.Async import Client
import asyncio

async def my_coro():
	async with Client(*args, **kwargs) as client:
		async with (await client.image('FILTER', 'IMAGE-URL', override_raw = True)) as response:
			...

asyncio.run(my_coro())
```

## Intergrating with discord.py
```py
from MK.Async import Client

client = Client(token='My Secret Token', **kwargs)

@self.command()
async def invert(ctx, user: discord.Member):
    image = await client.image('invert', str(user.avatar_url_as(static_format='png')))
    ## You can put any image file as long as it can accessed by the API
    ## recomend using PNG as its less likely to cause P MODE errors! 
    await ctx.send(file=discord.File(fp=image, filename='invert.png'))
```
