import requests
import os
import nextcord
from nextcord.ext import commands
weatherapi_key = os.environ['e'].replace("'", "")
url = "http://api.weatherapi.com/v1"

reqs = {"Current weather":"current.json", 
        "Forecast":"forecast.json"}

class Weather(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command()
    async def weather(self, ctx, *,location):
        response = (requests.get(f"{url}/{reqs['Current weather']}?key={weatherapi_key}&q={location}"))
        print(response.status_code, "\n")
        if response.status_code == 200:
                r_dict = response.json()
        
                place = r_dict['location']
                now = r_dict['current']
        
                temperature = f"\ntemperature: {now['temp_c']}℃ {now['temp_f']}℉"
                weather_cond = f"\n{now['condition']['text']} "
                cond_icon = now['condition']['icon'][2:]
                if now['wind_kph'] > 15: wind_kph = f"\nwind speed: {now['wind_kph']} kpmh"
                else:wind_kph=""  
                if now['precip_mm'] > 0:precip = f"\n amount of rain: {now['precip_mm']}mm"
                else:precip = ''
                humidity = f"\nhumidity: {now['humidity']}%"
                cloud = f"\ncloudiness: {now['cloud']}%"
                current_weather = f"{weather_cond}{temperature}{wind_kph}{humidity}{cloud}{precip}"
                embed = nextcord.Embed(
                        title=f"Current weather at `{place['name']}, {place['region']}, {place['country']}`",
                        description=current_weather) 
                embed.set_thumbnail(url="https://"+cond_icon)
                embed.set_author(name=f"{place['localtime'][10:]} in {place['country']}")
                embed.set_footer(text=f"last updated at: `{now['last_updated']}`")
                await ctx.channel.send(embed=embed)

def setup(client): client.add_cog(Weather(client))