# MechaK.py
Official API for the Mecha Karen API

Because im lazy to upload to pypi, to get the module `pip install git+https://github.com/Seniatical/MechaK.py/`

**Usage:**
```py
>>> import MK
>>> client = MK.Client('$API TOKEN')
>>> my_math = await client.math('1 + 1')
>>> print(my_math)
2
>>> ## Not to copy just an example
```

Intergrating with discord.py

raw bytes issue has been fixed enjoy!

```py
import MK

client = MK.Client('$API TOKEN')

@self.command()
async def invert(ctx, user: discord.Member):
    image = await client.image('invert', str(user.avatar_url_as(static_format='png')))
    ## You can put any image file as long as it can accessed by the API
    ## recomend using PNG as its less likely to cause P MODE errors! 
    await ctx.send(file=discord.File(fp=image, filename='invert.png'))
```
