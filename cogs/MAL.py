from nextcord.ext import commands
#import malclient

#mal = malclient.Client()

class MAL(commands.Cog):
	def __init__(self, client):
		self.client = client
	
	
	@commands.command()
	async def something(ctx):
		pass
def setup(client):
	client.add_cog(MAL(client))