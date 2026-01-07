from discord.ext import commands
import discord
import requests
import CONFIG


bot = commands.Bot(command_prefix="!", intents=discord.Intents.all())


    
@bot.command(name='statcheck', help='format !statcheck <your battle.net tag here> -> includes hashtags + hero.')

async def statcheck(ctx, battledotname='', hero=''):
    if battledotname == '':
        await ctx.send("Must enter a valid battle.net tag including the # symbol.")
        
    params = {'gamemode' : 'competitive'}
    dps_heroes = ['ashe', 'bastion', 'cassidy', 'echo', 'genji', 'hanzo', 'junkrat', 'mei', 'pharah', 
                  'reaper', 'soldier76', 'sombra', 'symmetra', 'soujourn' 'torbjorn', 'tracer', 'widowmaker', 'freja', 'vendetta', 'venture']
    tank_heroes = ['dva', 'orisa', 'ramattra', 'reinhardt', 'roadhog', 'sigma', 'winston', 'wreckingball', 'zarya', 'junkerqueen', 'mauga', 'hazard' ]
    sup_heroes = ['ana', 'baptiste', 'brigitte', 'lúcio', 'mercy', 'moira', 'zenyatta', 'kiriko', 'lifeweaver', 'juno', 'illari', 'wuyang']
    hero_stats = False
    if hero in dps_heroes or hero in tank_heroes or hero in sup_heroes:
        hero_stats = True

        username = battledotname.replace('#', '-')
        user_stats = requests.get(url='https://overfast-api.tekrop.fr/players/' + username + '/stats/career', params=params)
        stats_summary = requests.get(url='https://overfast-api.tekrop.fr/players/' + username + '/stats/summary', params=params)
        
        if user_stats.status_code != 200 or stats_summary.status_code != 200:
            await ctx.send("Could not retrieve stats. Please ensure the Battle.net tag is correct. (case sensitive)")
        else:
            user_data = user_stats.json()
            summary_data = stats_summary.json()

            if user_data == {} or summary_data == {}:
                await ctx.send("account is set to private")
    
    
            for i in range(len(dps_heroes)):
                dps_data = {}
                dps_data['hero'] = dps_heroes[i]
                try:
                    dps_data['games_played'] = user_data[dps_heroes[i]]['game']['games_played']
                except:
                    dps_data['games_played'] = 0

                if hero == dps_heroes[i]:
                    await ctx.send(hero + ' stats in comp:\n'
                                   + 'Games Played: ' + str(dps_data['games_played']))
                    
            

bot.run(CONFIG.BOT_TOKEN)


