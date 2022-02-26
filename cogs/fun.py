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
				

	@commands.command(aliases=["hit","smack"])
	async def slap(self,ctx, *targ):
		target = " ".join([f"{targ[i]}" for i in range(len(targ))])
		slapper = ctx.message.author.mention
		all_slaps = ["slapped", "smacked", "hit"]
		slaps = random.choice(all_slaps)
		print("Slap was ran")
		print("Target spotted",target)
		print("Assilant spotted",slapper)
		if OWNER in target: 
				print("Someone tried to slap Bongs")
				if slapper == OWNER:
						print("Bongs tried to slap himslef")
						await ctx.channel.send("Don't hurt yourself majesty")
				elif slapper != OWNER:
						print("Someone else tried to slap Bongs")
						await ctx.channel.send("No one slaps the Potato King!")
		elif MASTER in target or MASTWO in target:
				await ctx.channel.send("You are not allowed to slap daddy!")
				
		elif str(ctx.author.id) in target:
				await ctx.channel.send(embed=discord.Embed(description=f"{slapper} {slaps} {target},but regret hurting themself"))
			
		elif "790123597246889994" in target:
				await ctx.channel.send(embed=discord.Embed(description=f"{slapper} {slaps} {target}"))
				await ctx.channel.send("I am sad now :pensive:")
	
		elif not(OWNER in target) and not(MASTER in target) and not(MASTWO in target) and not(str(ctx.author.id) in target):
				await ctx.channel.send(embed=discord.Embed(description=f"{slapper} {slaps} {target}"))



	# THE HUG COMMAND
	@commands.command()
	async def hug(self, ctx, *,target):
		member_ping = ctx.author.mention
		huggie = random.choice(["hugs", "gives a big hug to", ":people_hugging:"])
		print("Hug was ran")
		print(target)
		await ctx.channel.send(embed=discord.Embed(description=f"{member_ping} {huggie} {target}"))
		if member_ping in target:
			await ctx.channel.send(embed=discord.Embed(description=ctx.author.mention + " tries to hug themself, realises that they are lonely and becomes sad"))
			await ctx.channel.send("Oh don't be sad!  " )
			await ctx.channel.send(embed=discord.Embed(description=f"<@!790123597246889994> {huggie} {member_ping}"))
			return
		elif "<@!790123597246889994>" in target or "<@790123597246889994>" in target:
			print("Someone hugged me, YAY!")
			await ctx.channel.send('Oh thank you!')
			await ctx.channel.send(embed=discord.Embed(description=f'<@!790123597246889994> hugs {member_ping}  back'))
			
def setup(client):
	client.add_cog(Commands(client))