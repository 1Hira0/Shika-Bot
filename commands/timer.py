from discord.ext import commands
import discord
from asyncio import sleep

class Timer(commands.Cog):
	def __init__(self, client):
		self.client = client

	@commands.command(aliases=["reminder", "alarm"])
	async def timer(self, ctx, wait:int=60, *,reason=None):
		txt = await ctx.channel.send(f"Setting timer for {wait}")
		if reason == None: 
		    reason = wait
		msg = f"**Your timer for {reason} has ended**"
		embed=discord.Embed(title="Timer" , description=msg)
		await txt.edit(content=f'set timer for {reason} ')
		await sleep(wait)
		await ctx.channel.send(content=f"**{ctx.author.mention}**", embed=embed)

def setup(client):client.add_cog(Timer(client))    