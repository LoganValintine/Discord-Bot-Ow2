from discord.ext import commands
import discord
import requests
import CONFIG


bot = commands.Bot(command_prefix="!", intents=discord.Intents.all())


    
@bot.command(name='statcheck', help='format !statcheck <your battle.net tag here> -> includes hashtags + hero + stat.')

async def statcheck(ctx, battledotname='', hero='', stat=''):
    if battledotname == '':
        await ctx.send("Must enter a valid battle.net tag including the # symbol.")
        
    params = {'gamemode' : 'competitive'}
    heroes = ['ashe', 'bastion', 'cassidy', 'echo', 'genji', 'hanzo', 'junkrat', 'mei', 'pharah', 
                  'reaper', 'soldier76', 'sombra', 'symmetra', 'soujourn' 'torbjorn', 'tracer', 'widowmaker', 'freja', 'vendetta', 'venture',
                  'dva', 'orisa', 'ramattra', 'reinhardt', 'roadhog', 'sigma', 'winston', 'wreckingball', 'zarya', 'junkerqueen', 'mauga', 'hazard', 
                  'ana', 'baptiste', 'brigitte', 'lúcio', 'mercy', 'moira', 'zenyatta', 'kiriko', 'lifeweaver', 'juno', 'illari', 'wuyang']
    hero_stats = False
    if hero in heroes:
        hero_stats = True

        username = battledotname.replace('#', '-')
        user_stats = requests.get(url='https://overfast-api.tekrop.fr/players/' + username + '/stats/career', params=params)
        
        if user_stats.status_code != 200:
            await ctx.send("Could not retrieve stats. Please ensure the Battle.net tag is correct. (case sensitive)")
        else:
            user_data = user_stats.json()

            if user_data == {}:
                await ctx.send("account is set to private")
    
            data = 0
            
            for i in range(len(heroes)):
                if hero == heroes[i]:
                    percentage = False
                    match(stat):
                        case "games":
                            try:
                                data = user_data[heroes[i]]['game']['games_played']
                            except:
                                data = 0
                        case "wr":
                            percentage = True
                            try:
                                data = user_data[heroes[i]]['game']['win_percentage']
                            except:
                                data = 0
                               
                        case "wins":
                            try:
                                data = user_data[heroes[i]]['game']['games_won']
                            except:
                                data = 0
                        case "elims":
                            try:
                                data = user_data[heroes[i]]['combat']['eliminations']
                            except:
                                data = 0
                        case "losses":
                            try:
                                data = user_data[heroes[i]]['game']['games_lost']
                            except:
                                data = 0
                                 
                                 
                    if percentage:
                        data = round(data, 2)
                        data = str(data) + "%"
                        
                    await ctx.send(username+ "'s " + stat + " for " + hero + " is: " + str(data))  
                    
@bot.command(name='helpstatcheck', help='Provides information on how to use the statcheck command.')
async def helpstatcheck(ctx):
    help_message = (
        "To use the !statcheck command, use the following format:\n"
        "`!statcheck <Battle.net Tag> <Hero> <Stat>`\n\n"
        "Where:\n"
        "- `<Battle.net Tag>`: Your full Battle.net tag including the # symbol (e.g., Player#1234).\n"
        "- `<Hero>`: The hero you want to check stats for.\n"
        "- `<Stat>`: The specific stat you want to check. Valid stats include:\n"
        "  **games** (total games played), **wr** (win rate percentage), **wins** (total wins), **elims** (total eliminations), **losses** (total losses).\n\n"
        "Example usage:\n"
        "`!statcheck Player#1234 tracer wr` - This will return the win rate for Tracer for the specified player.\n"
        "**PLEASE NOTE: I have not included Console as I am too lazy to accomdate Zay lmao**"
    )
    await ctx.send(help_message)            

@bot.command (name='rankcheck', help='format !rankcheck <your battle.net tag here> -> includes hashtags + role (dps, tank, support).')
async def rankcheck(ctx, battledotname='', role=''):
    if battledotname == '':
        await ctx.send("Must enter a valid battle.net tag including the # symbol.")
    
    if role not in ['dps', 'tank', 'support']:
        await ctx.send("Role must be one of the following: dps, tank, support.")
    
    params = {'gamemode' : 'competitive'}
    
    username = battledotname.replace('#', '-')
    stats_summary = requests.get(url='https://overfast-api.tekrop.fr/players/' + username + '/summary')
        
    if stats_summary.status_code != 200:
        await ctx.send("Could not retrieve stats. Please ensure the Battle.net tag is correct. (case sensitive)")
    else:
        summary_data = stats_summary.json()

        if summary_data == {}:
            await ctx.send("account is set to private")
            
        rank = ''
        tier = 0
        
        
        
        match role:
            case 'tank':
                try:
                    rank = summary_data['competitive']['pc']['tank']['division']
                    tier = summary_data['competitive']['pc']['tank']['tier']
                except:
                    rank = ''
                    tier = 0
                       
            case 'support':
                try:
                    rank = summary_data['competitive']['pc']['support']['division']
                    tier = summary_data['competitive']['pc']['support']['tier']
                except:
                    rank = ''
                    tier = 0
                
            case 'dps':
                try:
                    rank = summary_data['competitive']['pc']['damage']['division']
                    tier = summary_data['competitive']['pc']['damage']['tier']
                except:
                    rank = ''
                    tier = 0
    await ctx.send(username + "'s rank for " + role + " is: " + rank + " " + str(tier))        
        
            
            
        




bot.run(CONFIG.BOT_TOKEN)


