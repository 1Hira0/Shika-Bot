from datetime import datetime
import nextcord, requests, os
from nextcord import SlashOption, Interaction
from nextcord.ext import commands
import json

habitica_userKeys = requests.post("https://habitica.com/api/v3/user/auth/local/login?", data={"username":"1Hira0", "password":os.environ['1Hira0']}).json()
headers = {"x-api-user":habitica_userKeys['data']['id'], "x-api-key":habitica_userKeys['data']['apiToken']}

sub = SlashOption(name="subject", 
                  description='Subject of the homework. If other, then write the subject name in text, eg-"Arts - Draw water"', 
                  choices=['Hindi', 'English', "Mathematics", "Science", "Social Science", "Other"])
h_type = SlashOption(name='type', 
                     description='For other, for eg its "making a ppt"-"AI - Make ppt on_"', 
                     choices=['Do', 
                              'Write', 
                              'Learn', 
                              'other']
                    )

diff = SlashOption(name="difficulty", description="Difficulty of the homework", choices={"Trivial":'0.1',"Easy":'1',"Medium":'1.5',"Hard":'2'})
d_d = SlashOption(description="Please enter in DD/MM/YY (use 0 when 1 digit)", required=False, default="No due date")
atchmts = SlashOption(description='Any attachments/files for the homework', required=False, default='Koya:No')

class Homework(commands.Cog):
    def __init__(self, client): self.client = client

    @nextcord.slash_command(name='homework', description =" ᲼", guild_ids=[951344945762013195])
    async def hw(self, ctx:Interaction, subject:str=sub, tip=h_type, homework:str=SlashOption(description='For no homework please use "None"'), diff=diff, due_date=d_d, attachments:nextcord.Attachment=atchmts):
        await ctx.send('Please wait for response', ephemeral=True)
        if ctx.user.id in [649989137423794189, 602098932260143124] and ctx.channel_id == 988469149992898600:
            print('got user is god')
            if subject == "Other": subject, homework = homework.split("-")
            print('split homework')
            if tip != 'other':homework = tip + ' ' + homework
            print('addedtip')
            d = ""
            if due_date != "No due date": d = f"<t:{str(datetime.strptime(due_date, '%d/%m/%y').timestamp())[:-2]}:F>"
            await ctx.send(f"{subject} - {homework + d}")
            print('added due date')
            if attachments != "Koya:No" : 
                print('got attachment')
                material = await attachments.to_file()
                print('got material')
                await ctx.send(file=material)
                print('sent file')
            print('sent message')
            if due_date != "No due date":
                requests.post('https://habitica.com/api/v3/tasks/user', 
                              data={"text":subject, "type": "todo", "notes":homework, "priority":diff, "date":datetime.strptime(due_date, '%d/%m/%y')}, 
                              headers=headers)
            else:requests.post('https://habitica.com/api/v3/tasks/user', 
                              data={"text":subject, "type": "todo", "notes":homework, "priority":diff}, 
                              headers=headers)
            msg = await ctx.original_message()
            await msg.add_reaction("✅")
            await msg.add_reaction('❌')
        else: await ctx.send("You are not allowed to use that", ephemeral=True)
    @nextcord.slash_command(name='edit', description='Edit a homework', guild_ids=[951344945762013195])
    async def edithw(self, ctx:Interaction, msg_id, new_content, attachment=SlashOption(required=False, default="None"), embed=SlashOption(description="To add the prepared embed (from /embed) to the message", choices=["Yes", "No"], default='No', required=False)):
        if not (ctx.user.id in [649989137423794189, 602098932260143124] and ctx.channel_id == 988469149992898600): 
            await ctx.send("You are not allowed to use that", ephemeral=True)
            return
        msg = await ctx.channel.fetch_message(msg_id)
        if embed != "No": 
            with open("embed.json", "r") as myemb:
                embdata = json.load
            await msg.edit(content=new_content, embed=emb)
        await msg.edit(content=new_content, file=None)
        await ctx.send('Message edited!', ephemeral=True ,embed=nextcord.Embed(title='Message link', url=msg.jump_url, description=f"From \n```{msg.content}``` \nTo \n```{new_content}```"))
def setup(client):client.add_cog(Homework(client))