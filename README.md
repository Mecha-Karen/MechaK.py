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
```py
import MK

client = MK.client('$API TOKEN')

@self.command()
async def invert(ctx, user: discord.Member):
    image = await client.image('invert', user.avatar_url_as('png'))
    await ctx.send(file=discord.File(fp=image, filename='invert.png'))
```
