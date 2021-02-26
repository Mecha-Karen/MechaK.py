# MechaK.py
Official API for the Mecha Karen API

Because im lazy to upload to pypi, to get the module `pip install git+https://github.com/Seniatical/MechaK.py/`

**Usage:**
```py
>>> import MK
>>> client = MK.client('$API TOKEN')
>>> my_math = await client.math('1 + 1')
>>> print(my_math)
2
>>> ## Not to copy just an example
```

Intergrating with discord.py

Due to the unsupported method of using raw bytes to send which hasn't been added to discord.py
We have to use a seperate library to send our file. This speeds up the API as we dont need to save files.
I will issue a temp fix in the future!

```py
import MK
import aiofiles

client = MK.client('$API TOKEN')

@self.command()
async def invert(ctx, user: discord.Member):
    image = await client.image('invert', user.avatar_url_as(static_format='png'))
    async with aiofiles.open('filename.png', mode='wb') as f:
        await f.write(image)
    await ctx.send(file=discord.File('./filename.png', filename='invert.png'))
```
