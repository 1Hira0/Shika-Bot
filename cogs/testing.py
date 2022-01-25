from discord.ext import commands
#from bs4 import BeautifulSoup 

class Test(commands.Cog):
	def __init__(self, client):
		self.client = client

	@commands.command()
	async def test(self, ctx, *,content):
		await ctx.channel.send("No tests going on")
		await ctx.channel.send("Last test: Test No.2")
		

		





def setup(client):client.add_cog(Test(client))