import discord
import random
import asyncio
from discord.ext import commands

OWNER = '639259314074157077'
MASTER = '602098932260143124'
MASTWO =  '847861640833007686'

class Commands(commands.Cog):
	def __init__(self, client):
		self.client = client

	@commands.Cog.listener()
	async def on_ready(self):
		pass



	@commands.command()
	async def rps(self, ctx):
			choices = ["🪨", "✂️","📄"]
			mymass = await ctx.channel.send(f"Please choose an option from :rock:, ✂️ or 📄")
			await mymass.add_reaction("🪨")
			await mymass.add_reaction("✂️")
			await mymass.add_reaction("📄")

			def check(reaction, user):
				return user == ctx.author and str(reaction.emoji) in choices
			while True:
					try:
							reaction, user = await self.client.wait_for("reaction_add", timeout=10, check=check)
							print(reaction)
							print(user)
							react = reaction
							reaction = str(reaction.emoji)
							compChoice = random.choice(choices)
							if reaction == "🪨":
									print(f"{user} chose rock")
									if compChoice == "✂️":
											await mymass.edit(content="Oh nooooooooooo \n I lost, you totally crushed me :pensive:")
											print("Computer lost")
									elif compChoice == "📄":
											await mymass.edit(content="Oh I won yay! \n I covered over you :stuck_out_tongue_winking_eye: ")
											print("Computer won")
							elif reaction == "✂️":
									if compChoice == "📄":
											await mymass.edit(content="Oh nooooooooooo! \n I lost, you scissored me :face_with_raised_eyebrow:")
											print("Computer lost")
									elif compChoice == "🪨":
											await mymass.edit(content="Oh I won yay! \n I crushed you :stuck_out_tongue_closed_eyes:")
											print("Computer won")
							elif reaction == "📄":
									if compChoice == "🪨":
											await mymass.edit(content="Oh nooooooooooo! \n I lost, you covered me :rolling_eyes:")
											print("Computer lost")
									elif compChoice == "✂️":
											await mymass.edit(content="Oh! I won yay! \n I cut right through your mind :sunglasses:")
											print("Computer won")
							if compChoice == reaction:
									print("both tied")
									await mymass.edit(content="Oh! We tied :neutral_face:")
							await mymass.remove_reaction(react, user)
							await ctx.channel.send(content="NEW GAME!", delete_after=2)
					except asyncio.TimeoutError:
							await ctx.channel.send("Timeout!")
							break
				
def setup(client):
	client.add_cog(Commands(client))