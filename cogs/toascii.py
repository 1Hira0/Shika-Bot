import nextcord, requests, os
from PIL import Image
from nextcord.ext import commands
import ascii_magic as asci
from nextcord import SlashOption

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
	jizz=SlashOption(name="size", description="How big the ascii should be, bigger=detailed+time taking", 
                           	  default=120, min_value=50, max_value=1000, required=False)
	convertion = SlashOption(name='type', description='Type to convert into',
                             default=asci.Modes.ASCII, required=False,
                             choices={'ASCII text file(grayscale)':asci.Modes.ASCII, 
                                      'HTML text gile(full color)':asci.Modes.HTML})
	@nextcord.slash_command(name="toascii", description='Converts given image into ascii')
	async def toasc(self, ctx:nextcord.Interaction, img:nextcord.Attachment, columns:int=jizz, mode=convertion):
		name, ext = os.path.splitext(img.filename)
		await img.save(f'temp.{ext}')
		emb = nextcord.Embed(title=f'Converting {name}.{ext}', description = 'Please wait. \nBigger files/convertion size takes long to convert',color=nextcord.Color.red)
		await ctx.response.send_message(embed=emb)
		msg = await ctx.original_message()
		hill = asci.from_image_file(img_path=f'temp.{ext}', columns=columns ,mode=mode)
		emb = nextcord.Embed(title='Convertion done!', description='Trying to send. Please wait', color=nextcord.Color.dark_green)
		await msg.edit(embed=emb)
		os.remove(f'temp.{ext}')
		path = "tmp.txt"
		if mode==asci.Modes.ASCII:
			asci.to_file(path=path, art=hill)
		elif mode==asci.Modes.HTML: asci.to_html_file(path=path, art=hill)
		await msg.edit(embed=None, content='Sending!')
		await ctx.send(file=nextcord.File(path))
		await ctx.delete_original_message()
		os.remove(path)
def setup(client): client.add_cog(ToAscii(client))
