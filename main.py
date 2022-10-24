import os
import time
import discord
from discord import Intents
from discord.ext import commands
from dotenv import load_dotenv
import replicate
from IPython.display import display

load_dotenv()

replicate_api_token = os.environ['REPLICATE_API_TOKEN']

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(
  command_prefix="/",
  description="Crea il tuo Pokémon!",
  intents=intents,
)
  
@bot.command(uguale=["aiuto"])
async def aiuto(ctx):
  """Comandi del bot in Italiano"""
  await ctx.send("Usa /createmon e l'input per generare il tuo nuovo Pokémon preferito!")

@bot.command(equals=["cm"])
async def cm(ctx, *, new_p):
  """Generate your new favourite Pokémon!"""        
  msg = await ctx.send(f"“{new_p}”\n> Generating...")
  model = replicate.models.get("lambdal/text-to-pokemon")
  for image in model.predict(prompt=f"“{new_p}”",num_output=1,num_inference_steps=50,guidance_scale=7.5):
    display(image)
  await msg.edit(content=f"“{new_p}”\n{image}\nDo you like this Pokémon?")
  mp = "✅"
  nmp = '❌'

  await msg.add_reaction(mp)
  await msg.add_reaction(nmp)
  
  def check(reaction, user):
        return user == ctx.author and str(
            reaction.emoji) in [mp, nmp]

  member = ctx.author

  while True:
      try:
          reaction, user = await bot.wait_for("reaction_add", timeout=10.0, check=check)

          if str(reaction.emoji) == mp:
              await msg.edit(content=f"“{new_p}”\n{image}\n{user} likes this new Pokémon!")
          if str(reaction.emoji) == nmp:
              await msg.edit(content=f"I'm sorry that didn't come out a Pokémon that you like {user}, but you can try again!")
              time.sleep(10)
              await msg.delete()
      except:
        msg.edit(content="error")
              
@bot.command(identico=["cm_ita"])
async def cm_ita(ctx, *, new_p):
  """Genera il tuo nuovo Pokémon preferito!"""        
  msg = await ctx.send(f"“{new_p}”\n> Generando...")
  model = replicate.models.get("lambdal/text-to-pokemon")
  for image in model.predict(prompt=f"“{new_p}”",num_output=1,num_inference_steps=50,guidance_scale=7.5):
    display(image)
  await msg.edit(content=f"“{new_p}”\n{image}\nTi piace questo Pokémon?")
  
  mp = "✅"
  nmp = '❌'

  await msg.add_reaction(mp)
  await msg.add_reaction(nmp)
  
  def check(reaction, user):
        return user == ctx.author and str(
            reaction.emoji) in [mp, nmp]

  member = ctx.author

  while True:
      try:
          reaction, user = await bot.wait_for("reaction_add", timeout=10.0, check=check)

          if str(reaction.emoji) == mp:
              await msg.edit(content=f"“{new_p}”\n{image}\nA {user} piace questo nuovo Pokémon!")
          if str(reaction.emoji) == nmp:
              await msg.edit(content=f"Mi dispiace che non sia uscito un Pokémon che ti piaccia {user}, ma puoi sempre riprovarci!")
              time.sleep(10)
              await msg.delete()
              
      except:
        msg.edit(content="error")
 




bot.run(os.environ['DISCORD_TOKEN'])