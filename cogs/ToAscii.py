import nextcord, requests, os
#from PIL import Image
from nextcord.ext import commands
import ascii_magic as asci

#to return the file from the either url or attachment, and checking if its valid
def toFile(url, attach):
	if attach != []:
		name, ext=os.path.split(attach[0].filename)
		pic = attach[0]
	elif attach == [] and url != None:
		try:
				response = requests.get(url)
				if response != None:
					print("URL is valid and exists on the internet")
					return True
		except requests.ConnectionError:
				print("URL does not exist on Internet")
				return False
	return pic, ext
			


class ToAscii(commands.Cog):
	def __init__(self, client):
		self.client = client

	@commands.command()
	async def toascii(self, ctx, columns:int=120):
		print(bool(ctx.message.attachments))
		if ctx.message.attachments:
				print(columns)
				msg = await ctx.channel.send("converting image!")
				attachment = ctx.message.attachments[0]
				name, ext = os.path.splitext(attachment.filename)
				filen = f"temp.{ext}"
				await attachment.save(filen)
				hill = asci.from_image_file(img_path=filen, columns=columns ,mode=asci.Modes.ASCII)
				os.remove(filen)
				path = "tmp.txt"
				asci.to_file(path=path, art=hill)
				await ctx.channel.send(file=nextcord.File(path))
				os.remove(path)
				await msg.delete()
		else: await ctx.channel.send(content="No image")
def setup(client): client.add_cog(ToAscii(client))