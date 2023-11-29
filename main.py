import discord
from scripts import *
from guilds import *
from loguru import logger

intents = discord.Intents.all()
intents.message_content = True
client = discord.Client(intents=intents)

ID = 1121511632019923076
OWNER = 710395621688737892
keyword = 'kkr_loot'
startswith = '/'

GUILDS = {}

LOCALISITION = {'eng': '🇺🇲', 
                'ru': '🇷🇺'}

###
GUILDS[1164886134137045022] = Guilds(1164886134137045022, [710395621688737892])
GUILDS[1164886134137045022].guild_language = 'eng'


@client.event
async def on_ready():
    global GUILDS, LOCALISITION, ID, COMMAND, OWNER, client
    COMMAND = language_initialization()
    logged()


@logger.catch
@client.event
async def on_message(message):
    if (message.content.startswith(startswith) 
        and message.author.bot != True 
        and message.channel.name == keyword
        and message.content.split(' ')[0].lower() 
                    in COMMAND[(GUILDS[message.guild.id]).guild_language]  # existing command
        and GUILDS[message.guild.id].guild_language != None):

        async def send_Embed(data_list):
            if len(data_list) == 4: 
                owner = client.get_user(OWNER)
                print(owner, OWNER)
                await owner.send(data_list[3])
            await message.channel.send(embed = discord.Embed(
                title=data_list[0],
                description=data_list[1],
                colour=data_list[2]))
        
        list_message = message.content.split(' ')
        command = list_message[0].lower()  # command in the original language
        list_message.pop(0)

        try: conditions = list_message
        except: conditions = None

        author_name = message.author.name
        author_id = message.author.id
        guild_id = message.guild.id

        log = (command, 
               await client.fetch_guild(guild_id), guild_id,
               author_name, author_id)

        command = COMMAND[GUILDS[guild_id].guild_language][command]
        print(command)  # command in english
        language = GUILDS[guild_id].guild_language
        
        match command:
            case 'admins': await send_Embed(
                admins(log, language, 
                       admins=[(await client.fetch_user(GUILDS[guild_id].admins[_])).name for _ in range(len(GUILDS[guild_id].admins))]))
            
        

            



@client.event
async def on_raw_reaction_add(payload):

    if (payload.user_id in GUILDS[payload.guild_id].admins   # Change language
          and payload.user_id != ID
          and GUILDS[payload.guild_id].guild_language is None):
        
        log = ('start_select_language', 
               await client.fetch_guild(payload.guild_id), payload.guild_id, 
               await client.fetch_user(payload.user_id), payload.user_id)
        
        GUILDS[payload.guild_id].guild_language, dict_embed = start_select_language(
            LOCALISITION, payload.emoji, log)
        
        await client.get_channel(payload.channel_id).send(embed = discord.Embed(
                title=dict_embed['title'],
                description=dict_embed['description'],
                colour=dict_embed['colour']))
        


@client.event
async def on_guild_join(guild):
    kkr_loot = discord.utils.get(guild.channels, name='kkr_loot')
    if kkr_loot is not None:
        msg = await kkr_loot.send(embed = discord.Embed(
                title='Hi!',
                description='Please select the language below',
                colour=1752220))
        GUILDS[guild.id] = Guilds(guild.id, [guild.owner_id])
        for lang in LOCALISITION: await msg.add_reaction(LOCALISITION[lang])
        new_guild_initialization(['NEW_GUILD', await client.fetch_guild(guild.id), guild.id])
        
        

@client.event
async def path_settings(guild_id):
    pass



if __name__ == "__main__":
    client.run(input('token: '))