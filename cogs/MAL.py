import math
import os
from datetime import date

import nextcord
import requests
from mangareader import get_mangareader
from nextcord import ButtonStyle, Interaction, SlashOption, ui
from nextcord.ext import commands

thisyear = date.today().year

mal_url = 'https://api.myanimelist.net/v2'
headers = {'Authorization': f"Bearer {os.environ['mal']}"}
auth = {'X-MAL-CLIENT-ID':f"{os.environ['clientid']}"}
mal_icon = "https://cdn.myanimelist.net/img/sp/icon/apple-touch-icon-256.png"
animix_icon = 'https://animixplay.to/icon.png'
mangareader_icon = "https://mangareader.to/images/apple-touch-icon.png"

seasons = {"January":"winter", "February":"winter", "March"    :"winter",
           "April"  :"spring", "May"     :"spring", "June"     :"spring",
	       "July"   :"summer", "August"  :"summer", "September":"summer",
           "October":"fall"  , "November":"fall"  , "December" :"fall"  }
cho = {
    "Top Anime Series"       :'all'         ,
    "Top Airing Anime"       :'airing'      ,
    "Top Upcoming Anime"     :'upcoming'    ,
    "Top Anime TV Series"    :'tv'          ,
    "Top Anime OVA Series"   :'ova'         ,
    "Top Anime Movies"       :'movie'       ,
    "Top Anime Specials"     :'special'     ,
    "Top Anime by Popularity":'bypopularity',
    "Top Favorited Anime"    :'favorite'    }
cho2 = {
    "All"           :"all"         ,
    "Top Manga"     :"manga"       ,
    "Top Novels"    :"novels"      ,
    "Top One-shots" :"oneshots"    ,
    "Top Doujinshi" :"doujin"      ,
    "Top Manhwa"    :"manhwa"      ,
    "Top Manhua"    :"manhua"      ,
    "Most Popular"  :"bypopularity",
    "Most Favorited":"favorite"}

animeSl_limit=SlashOption(name="limit",default=5,
        required=False, min_value=1, max_value=20, 
        description="Amount of search results")

class Pages(ui.View):
    def __init__(self, pages:list, embed:nextcord.Embed, eid:int):
        super().__init__()
        self.page_no = 1
        self.contents = pages
        self.embed = embed
        self.page_nos = len(pages)
        self.authorID = eid
    @ui.button(emoji="◀", style=ButtonStyle.green, disabled=True)
    async def backward(self, button:ui.Button, ctx:Interaction):
        if self.page_no == self.page_nos: 
            self.forward.disabled = False
            self.forward.style= ButtonStyle.green
        self.page_no -= 1
        self.embed.description=self.contents[self.page_no-1]
        if self.page_no == 1: 
            button.disabled = True
            button.style = ButtonStyle.danger
        self.no.label = f"{self.page_no}/{self.page_nos}"
        await ctx.response.edit_message(embed=self.embed, view=self)
    	
    @ui.button(label='1', disabled=True, style=ButtonStyle.green)
    async def no(self, button:ui.Button, ctx:Interaction):return

    @ui.button(emoji="▶", style=ButtonStyle.green)
    async def forward(self, button:ui.Button, ctx:Interaction):
        self.page_no += 1
        self.embed.description=self.contents[self.page_no-1]
        if self.page_no == self.page_nos: 
            button.disabled = True
            button.style = ButtonStyle.danger
        if self.page_no == 2:
            self.backward.disabled = False
            self.backward.style=ButtonStyle.green
            self.no.label = f"{self.page_no}/{self.page_nos}"
        await ctx.response.edit_message(embed=self.embed, view=self)
    		
    async def interaction_check(self, interaction: Interaction):
    	return interaction.user.id == self.authorID

class Choose(nextcord.ui.View):
    def __init__(self, id:int):
        super().__init__(timeout=60)
        self.value = 0
        self.authorID = id
        self.options = [self.option1,self.option2,self.option3,self.option4,self.option5]
    @nextcord.ui.button(label='1', style=nextcord.ButtonStyle.blurple)
    async def option1(self, button:nextcord.ui.Button, ctx:Interaction):
        self.value = 0
        for butt in self.options:butt.disabled = True
        self.stop()

    @nextcord.ui.button(label='2', style=nextcord.ButtonStyle.blurple)
    async def option2(self, button:nextcord.ui.Button, ctx:Interaction):
        self.value = 1
        for butt in self.options:butt.disabled = True
        self.stop()

    @nextcord.ui.button(label='3', style=nextcord.ButtonStyle.blurple)
    async def option3(self, button:nextcord.ui.Button, ctx:Interaction):
        self.value = 2
        for butt in self.options:butt.disabled = True
        self.stop()

    @nextcord.ui.button(label='4', style=nextcord.ButtonStyle.blurple)
    async def option4(self, button:nextcord.ui.Button, ctx:Interaction):
        self.value = 3
        for butt in self.options:butt.disabled = True
        self.stop()

    @nextcord.ui.button(label='5', style=nextcord.ButtonStyle.blurple)
    async def option5(self, button:nextcord.ui.Button, ctx:Interaction):
        self.value = 4
        for butt in self.options:butt.disabled = True
        self.stop()
    async def interaction_check(self, interaction: Interaction):
        return interaction.user.id == self.authorID

class Anime(commands.Cog):
    
    def __init__(self, client): self.client = client

    @nextcord.slash_command(name="anime")
    async def anime(self, ctx:Interaction): ...
    animeSl_name=SlashOption(
        name="anime",
        description="Name of the anime"
    )
    @anime.subcommand(
        name="search", description="Search for anime"
    )
    async def search(self, ctx:Interaction, anime:str=animeSl_name, limit:int=animeSl_limit):
        print("search used")
        response = requests.get(url=f"{mal_url}/anime?q={anime}&limit={limit}&nsfw={ctx.channel.nsfw}", headers=auth)
        print(response.status_code, f"\n{response.url}")
        if response.status_code == 200:
            r = response.json()['data']
            text = "\n".join([f"{i+1}. {r[i]['node']['title']}" for i in range(len(r))])
            emb=nextcord.Embed(description=text, color=nextcord.Color(0x2E51A2))
            emb.set_author(name=f"Search results for {anime}", icon_url=mal_icon,
    		               url=f"https://myanimelist.net/anime.php?q={anime.replace(' ', '%20')}&cat=anime")
            emb.set_footer(text="Want more info? Tap on the title to see more information")
            await ctx.response.send_message(embed=emb)

        elif r.status_code!= 400: 
            await ctx.response.send_message(content=f"Not found '{anime}'", ephemeral=True)
    
    
    @anime.subcommand(name="info", description=("anime info"))
    async def info(self, ctx:Interaction, name:str=animeSl_name):
        view = Choose(id=ctx.user.id)
        anime  = requests.get(url=f"{mal_url}/anime?q={name}&limit={5}&nsfw={ctx.channel.nsfw}", headers=auth)
        r = anime.json()['data']
        text = "\n".join([f"{i+1}. {r[i]['node']['title']}" for i in range(len(r))])
        emb=nextcord.Embed(description=text, color=nextcord.Color(0x2E51A2))
        emb.set_author(name=f"For {name}", icon_url=mal_icon,
    	               url=f'https://myanimelist.net/search/all?q={name.replace(" ", "%20")}&cat=all')
        emb.set_footer(text=f"Not in here? Tap on the title to open MyAnimelist")
        await ctx.response.send_message(embed=emb, view=view)
        await view.wait()
        chosen = view.value
        
    
        if anime.status_code == 200:
            animeID = anime.json()['data'][chosen]['node']['id']
            response = requests.get(url=f"{mal_url}/anime/{animeID}?fields=title,main_picture,alternative_titles,start_date,end_date,synopsis,related_anime,related_manga,mean,rank,nsfw,created_at,status,genres,rating,num_episodes,average_episode_duration,recommendations,studios,opening_themes,ending_themes",  headers=auth)
            r = response.json()
            print(r)
            #nsfw shit
            nsfw = ""
            if r['nsfw'] != 'white': nsfw = "\nnfsw"
            #number of episode(s)
            ep_num = f"\n{r['num_episodes']} episode"
            if r['num_episodes'] < 2: ep_num = f"{ep_num}s"
            #description of show
            synp = r['synopsis'].replace('\n\n','\n')
            #total time needed to complete the show (calulated from avg. time,in sec, for one ep - given from MAL )
            time_needed = f"\ntotal run time: {math.floor((r['num_episodes'] * r['average_episode_duration'])/3600)} hours {((r['num_episodes'] * r['average_episode_duration'])//60)%60} minutes"
            if ' 0 hours 0 minutes' in time_needed : time_needed = ''
            print(time_needed)
            #genre of the show
            genre = ''
            if 'genres' in r :genre = f"\n{', '.join([i['name'] for i in r['genres']])}"
            else: genre = '\ngenre: Not available yet'
            #recommendation/relatable shows
            recom = ''
            lee = len(r['recommendations'])
            if lee>20: lee =20
            if r['recommendations']:recom +=  "\nsimilar: "+(',\n'.join([f"[{r['recommendations'][i]['node']['title']}](https://myanimelist.net/anime/{r['recommendations'][i]['node']['id']})" for i in range(len(r['recommendations']))]))
            #studio which made this show
            studio = ''
            if r['studios']: studio = "\n\nStudio(s): "+ (", ".join(f"[{studio['name']}](https://myanimelist.net/anime/producer/{studio['id']})" for studio in r['studios']))
            #start & end date of release/ airing/ not released
            if r['status'] == 'not_yet_aired':timing = "\nNot aired yet"
            elif r['status'] == 'currently_airing': timing = f"\nfrom {r['start_date']} to ?(airing)"
            elif r['status'] == 'finished_airing':timing = f"\nfrom {r['start_date']} to {r['end_date']} - Finished airing"
            #rank on MAL
            ranga = '' #ranga is a character from Tensei Slime Datta Ken (That Time I Got Reincarnated as a Slime)
            if 'rank' in r: 
                if   str(r['rank']).endswith('1'): ranga = f"🏆: {r['rank']}st"
                elif str(r['rank']).endswith('2'): ranga = f"🏆: {r['rank']}nd"
                elif str(r['rank']).endswith('3'): ranga = f"🏆: {r['rank']}rd"
                else: ranga = f"🏆: {r['rank']}th"
            else: ranga = 'Not ranked yet'
            avg = 'Not scored yet'
            if 'mean' in r: avg=f"\n⭐:{r['mean']}"
            rating=''
            if 'rating' in r: rating = "\nAge rating: "+r['rating']
            r_manga = ''
            lee = len(r['related_manga'])
            if lee>20: lee =20
            if r['related_manga']: 
                r_manga = '\nRelated manga: ' + '\n'.join(
                    [f"{r['related_manga'][i]['relation_type_formatted']}: [{r['related_manga'][i]['node']['title']}](https://myanimelist.net/manga/{r['related_manga'][i]['node']['id']})" for i in range(lee)]
                    )
            r_anime = ""
            lee = len(r['related_anime'])
            if lee>37: lee =37
            if r['related_anime']: 
                r_anime = '\nRelated anime: ' + '\n'.join(
                    [f"{r['related_anime'][i]['relation_type_formatted']}: [{r['related_anime'][i]['node']['title']}](https://myanimelist.net/anime/{r['related_anime'][i]['node']['id']})" for i in range(lee)]
                    ) 
            ops = ''
            if 'opening_themes' in r: 
                if r['opening_themes']:ops = "\n" + '\n'.join(song['text'] for song in r['opening_themes'])
            eds = ''
            if 'ending_themes' in r: 
                if r['ending_themes'] : eds = "\n" + '\n'.join(song['text'] for song in r['ending_themes'])
            contents = [f"**{r['alternative_titles']['en']}** \n{synp}", f" {studio} {avg} ||  {ranga} {genre} {ep_num} {time_needed} {nsfw} {timing} {rating} {ops} {eds}", f"{recom} {r_anime} {r_manga}"]
            emb= nextcord.Embed(title=r['title'], description=contents[0], color=nextcord.Color(0x2E51A2), url= f"https://myanimelist.net/anime/{animeID}")
            emb.set_author(name="Tap here to play", icon_url=animix_icon,
    		               url= f"https://animixplay.to/anime/{animeID}")
            emb.set_footer(text="Want more info? Tap on the title to open it on MyAnimelist", icon_url=mal_icon)
            emb.set_thumbnail(url=r['main_picture']['large'])
            butt = Pages(pages=contents, embed=emb, eid=ctx.user.id)
            await ctx.edit_original_message(embed=emb, view=butt)
            timed_out = await butt.wait()
            butt.backward.disabled = True
            butt.forward.style = ButtonStyle.grey
            butt.no.style = ButtonStyle.grey
            butt.backward.style = ButtonStyle.grey
            butt.forward.disabled = True
            await ctx.edit_original_message(view=butt)
        else:await ctx.response.send_message(content='Not found', ephemeral=True)

    animeSl_limit.description='limit of anime'
    animeSl_limit.max_value = 500
    animeSl_limit.default = 20
    animeSl_ranks=SlashOption(name="type", description='Type of ranking',
    							required=True, choices=list(cho.keys()))
    
    
    @anime.subcommand(name='ranking', description='Anime ranking')
    async def rank(self, ctx: Interaction, tip:str=animeSl_ranks, limit:int=animeSl_limit):
        global cho
        _type = cho[tip]
        ranking = requests.get(f'{mal_url}/anime/ranking?ranking_type={_type}&limit={limit}&nsfw={ctx.channel.nsfw}', headers=auth)
        print(ranking.status_code)
        if ranking.status_code == 200:
            r = ranking.json()['data']
            contents = []
            for i in range(int(len(r)/10)): 
                contents.append("\n".join([f"{((i*10)+j)+1}. {r[(i*10)+j]['node']['title']}" for j in range(10)]))
            pages = len(contents)
            cur_page = 1
            emb=nextcord.Embed(description=contents[cur_page-1], color=nextcord.Color(0x2E51A2))
            emb.set_author(name=tip, url=f'https://myanimelist.net/topanime.php?type={_type}', 
    		icon_url=mal_icon)
            emb.set_footer(text=f"Page {cur_page}/{pages}")
            butt = Pages(pages=contents, embed=emb, eid=ctx.user.id)
            await ctx.response.send_message(embed=emb, view=butt)
            await butt.wait()
            butt.backward.disabled = True
            butt.forward.style = ButtonStyle.grey
            butt.no.style = ButtonStyle.grey
            butt.backward.style = ButtonStyle.grey
            butt.forward.disabled = True
            await ctx.edit_original_message(view=butt)
            
    animeSl_limit.max_value = 100
    animeSl_year = SlashOption(name="year", description="year of anime release", required=True, min_value=1965, max_value=thisyear, default=thisyear)
    animeSl_season = SlashOption(name="season", description="season of anime release", required=True, choices=seasons)
    @anime.subcommand(name='season', description='Anime of seasons')
    async def seasonal(self, ctx:Interaction, year:int=animeSl_year, season:str=animeSl_season, limit:int=animeSl_limit):
        response = requests.get(url=f"{mal_url}/anime/season/{year}/{season}?limit={limit}&nsfw={ctx.channel.nsfw}", headers=auth)
        print(response.text)
        if response.status_code == 200:
            r_dict = response.json()
            contents = []
            for i in range(int(len(r_dict['data'])/10)): 
                try:
                    contents.append("\n".join([f"{((i*10)+j)+1}. {r_dict['data'][(i*10)+j]['node']['title']}" for j in range(10)]))
                except IndexError: print("something happened")
            pages = len(contents)
            cur_page = 1
            emb=nextcord.Embed(description=contents[cur_page-1], color=nextcord.Color(0x2E51A2))
            emb.set_author(name=f"{r_dict['season']['season'].capitalize()} {r_dict['season']['year']}", 
                           url=f"https://myanimelist.net/anime/season/{r_dict['season']['year']}/{r_dict['season']['season']}",  
                           icon_url=mal_icon)
            emb.set_footer(text=f"Want more info? Tap on the title for more info")
            butt = Pages(pages=contents, embed=emb, eid=ctx.user.id)
            await ctx.response.send_message(embed=emb, view=butt)
            await butt.wait()
            butt.backward.disabled = True
            butt.forward.style = ButtonStyle.grey
            butt.no.style = ButtonStyle.grey
            butt.backward.style = ButtonStyle.grey
            butt.forward.disabled = True
            await ctx.edit_original_message(view=butt)
        elif response.status_code <= 400:await ctx.send(content=f"error:{response.text}", ephemeral=True)

class Manga(commands.Cog):
    def __init__(self, client): self.client = client
		
    @nextcord.slash_command(name="manga", description="manga")
    async def manga(self, ctx:Interaction): ...
    mangaSl_name=SlashOption(
        name="manga",
        description="Name of the manga")
    animeSl_limit.default=5,
    animeSl_limit.max_value=20
    @manga.subcommand(
        name="search", description="Search for manga")
    async def mangasearch(self, ctx:Interaction, manga:str=mangaSl_name, limit:int=animeSl_limit):
        print("search used")
        r = requests.get(url=f"{mal_url}/manga?q={manga}&limit={limit}&nsfw={ctx.channel.nsfw}", headers=auth)
        print(r.status_code, f"\n{r.url}")
        if r.status_code == 200:
            r_dict = r.json()['data']
            text = "\n".join([f"{i+1}. {r_dict[i]['node']['title']}" for i in range(len(r_dict))])
            print(f"\n'{text}'\n")
            emb=nextcord.Embed(description=text, color=nextcord.Color(0x2E51A2))
            emb.set_author(name=f"Search results for {manga}", 
    		url=f"https://myanimelist.net/search/all?q={manga}&cat=all", 
    		icon_url=mal_icon
            )
            await ctx.response.send_message(embed=emb)
        elif r.status_code == 400: 
            await ctx.response.send_message(content=f"Not found '{manga}'", ephemeral=True)
        
        
    @manga.subcommand(name="info", description=("Information on a manga"))
    async def mangainfo(self, ctx:Interaction, name:str=mangaSl_name):
        view = Choose(id=ctx.user.id)
        manga  = requests.get(url=f"{mal_url}/manga?q={name}&limit={5}&nsfw={ctx.channel.nsfw}", headers=auth)
        r = manga.json()['data']
        text = "\n".join([f"{i+1}. {r[i]['node']['title']}" for i in range(len(manga.json()['data']))])
        print(text)
        emb=nextcord.Embed(description=text, color=nextcord.Color(0x2E51A2))
        emb.set_author(name=f"For {name}"
    	, url=f'https://myanimelist.net/search/all?q={name.replace(" ", "%20")}&cat=all', 
    		#, 
    		#icon_url=mal_icon
            )
        emb.set_footer(text=f"Not in here? Tap on the title to open MyAnimelist")
        await ctx.response.send_message(embed=emb, view=view)
        await view.wait()
        chosen = view.value
        
        if manga.status_code == 200:
            print(manga.json())
            mangaID = manga.json()['data'][chosen]['node']['id']
            response = requests.get(url=f"{mal_url}/manga/{mangaID}?"+"fields=id,title,main_picture,alternative_titles,start_date,end_date,synopsis,mean,rank,popularity,num_list_users,num_scoring_users,nsfw,created_at,updated_at,media_type,status,genres,my_list_status,num_volumes,num_chapters,authors{first_name,last_name},pictures,background,related_anime,related_manga,recommendations,serialization",  headers=auth)
            r = response.json()
            print("Got Manga")
            creators = "\n"+"\n".join([f"{author['role']} by {author['node']['first_name']} {author['node']['last_name']}" for author in r['authors']])
            titles = [tit.lower() for tit in r['alternative_titles']['synonyms']] + [r['alternative_titles']['en'].lower(), r['title'].lower(), r['alternative_titles']['ja']]
            pirate = get_mangareader(r['title'])
            try:
                reading = [tit for tit in titles if tit.lower() in pirate.keys()][0]
                print(reading)
            except IndexError:
                reading='reading'
                pirate[reading]= f"https://mangareader.to/search?keyword={r['title']}".replace(' ', "+")
                print(pirate[reading])
				
            #description of manga
            synp = r["synopsis"].replace("\n\n", "\n")
            #rank of manga
            genre = ''
            if 'genres' in r :genre = f"\n{', '.join([i['name'] for i in r['genres']])}"
            else: genre = '\ngenre: Not available yet'
            #recommendation/relatable mangas
            recom = ''
            
            lee = len(r['recommendations'])
            if lee >5:lee = 5
            if r['recommendations']:recom +=  "\nsimilar: "+(',\n'.join([f"[{r['recommendations'][i]['node']['title']}](https://myanimelist.net/manga/{r['recommendations'][i]['node']['id']})" for i in range(len(['recommendations']))]))
            #rank on MAL
            ranga = '' #ranga is a character from Tensei Slime Datta Ken (That Time I Got Reincarnated as a Slime)
            if 'rank' in r: 
                ranga = f"🏆: {r['rank']}"
                if   str(r['rank']).endswith('1'): ranga+="st"
                elif str(r['rank']).endswith('2'): ranga+="nd"
                elif str(r['rank']).endswith('3'): ranga+="rd"
                else: ranga += "th"
            else: ranga = 'Not ranked yet'
            #score of manga on MAL
            avg = ''
            if 'mean' in r: avg=f"\n⭐:{r['mean']}"
            else:avg = 'Not scored yet'
            #status + chapters + publishing dates
            chapters = f"\nNo. of chapter(s): {r['num_chapters']}"
            if r['status'] == "not_yet_published": 
                pub_dates = chapters = ""
                r['title'] += " (not published yet)"
            elif r['status'] == 'currently_publishing': 
                r['title'] = f"{r['title']} (currently publishing)"
                chapters = "\nChapter count isn't available while publishing"
                pub_dates = f"\nPublishing since {r['start_date']}"
            else: pub_dates = f"\n{r['start_date']} to {r['end_date']}"
            serialIn = ""
            if 'serialization' in r: 
                try:
                    serialIn = f"\nSerialised in {r['serialization'][0]['node']['name']}"
                except IndexError: None
            msg = [f"{synp} ",f"\n{avg} || {ranga} {creators} {chapters} {pub_dates} {serialIn} {genre} {recom} "]
            emb= nextcord.Embed(title=r['title'], description=msg, color=nextcord.Color(0x2E51A2), 
                                url= f"https://myanimelist.net/manga/{mangaID}")
            emb.set_author(icon_url=mangareader_icon, 
                           name="Read at", url=pirate[reading])
            emb.set_footer(text="Want more info? Tap on the title to open it on MyAnimelist", icon_url=mal_icon)
            emb.set_thumbnail(url=r['main_picture']['large'])
            print(msg)
            butt = Pages(pages=msg, embed=emb, eid=ctx.user.id)
            await ctx.edit_original_message(embed=emb, view=butt)
            await butt.wait()
            butt.backward.disabled = True
            butt.forward.style = ButtonStyle.grey
            butt.no.style = ButtonStyle.grey
            butt.backward.style = ButtonStyle.grey
            butt.forward.disabled = True
            await ctx.edit_original_message(view=butt)
        else:await ctx.response.send_message(content='Not found', ephemeral=True)
        
    animeSl_limit.description='limit of manga'
    animeSl_limit.max_value = 500
    animeSl_limit.default = 20
    mangaSL_ranks=SlashOption(name="type",
    	description='Type of ranking',
    	required=True,
    	choices=list(cho2.keys()))
        
    @manga.subcommand(name='ranking', description='Manga ranking')
    async def ranks(self, ctx: Interaction, tip:str=mangaSL_ranks, limit:int=animeSl_limit):
        global cho2
        _type = cho2[tip]
        ranking = requests.get(f'{mal_url}/manga/ranking?ranking_type={_type}&limit={limit}&nsfw={ctx.channel.nsfw}', headers=auth)
        print(ranking.status_code)
        if ranking.status_code == 200:
            r = ranking.json()['data']
            contents = []
            for i in range(int(len(r)/10)): 
                contents.append("\n".join([f"{((i*10)+j)+1}. {r[(i*10)+j]['node']['title']}" for j in range(10)]))
            emb=nextcord.Embed(description=contents[0], color=nextcord.Color(0x2E51A2))
            emb.set_author(name=tip, url=f'https://myanimelist.net/topmanga.php{_type}', icon_url=mal_icon)
            emb.set_footer(text=f"Want more info? Tap on the title to open MyAnimeList")
            butt = Pages(pages=contents, embed=emb, eid=ctx.user.id)
            await ctx.response.send_message(embed=emb, view=butt)
            await butt.wait()
            butt.forward.style = ButtonStyle.grey
            butt.backward.disabled = True
            butt.no.style = ButtonStyle.grey
            butt.forward.disabled = True
            butt.backward.style = ButtonStyle.grey
            await ctx.edit_original_message(view=butt)            

userName = SlashOption(name='username', description="User's MAL username", required=True)
userStatus = SlashOption(name='status', description="User's anime status in MAL", required=False, choices={"All":"",  "Watching":"&status=watching",  "Completed":"&status=compleyed",  "On-hold":"&status=on_hold",  "Dropped":"&status=dropped", "PTW":"&status=plan_to_watch"}, default="")
class User(commands.Cog):
    def __init__(self, client): self.client = client
    
    @nextcord.slash_command(name="user")
    async def user(self, ctx:Interaction):...
    
    @user.subcommand(name="animelist", description="User's animelist")
    async def animelist(self, ctx:Interaction, username:str=userName, listStat:str=userStatus):
        response = requests.get(url=f"{mal_url}/users/{username}/animelist?limit=1000{listStat}&sort=list_updated_at", headers=headers)
        
def setup(client): 
	client.add_cog(Manga(client))
	client.add_cog(Anime(client))
