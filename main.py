import discord
from methods import *
from guilds import *

intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)

GUILDS = {}

LOCALISITION = {'🇺🇲': ':flag_um:', 
                '🇷🇺': ':flag_ru:'}


@client.event
async def on_ready():
    with open('localization/command.json', encoding='utf-8') as f:
        COMMAND = json.load(f)
    logged()

@client.event
async def on_message(message):

    if (message.content.startswith('/') 
        and message.author.bot != True 
        and message.channel.name == 'kkr_loot'
        and GUILDS[message.guild.id].guild_language != None):

        def send_Embed(data_list):
            return message.channel.send(embed = discord.Embed(
                title=data_list[0],
                description=data_list[1],
                colour=data_list[2]))
        
        list_message = message.content.split(' ')
        command = list_message[0].lower()
        list_message.pop(0)
        try: conditions = list_message
        except: conditions = None
        author_name = message.author.name
        author_id = message.author.id
        msg = None

        match command:
            
            case '/админы'      | '/admins'      : await send_Embed(return_admin(author_name, author_id))
            case '/регистрация' | '/registration': await send_Embed(registration(author_name, author_id, conditions))
            case '/участники'   | '/members'     : await send_Embed(return_members(author_name, author_id))
            case '/изменить'    | '/change'      : await send_Embed(change(author_name, author_id, conditions))
            case '/пиксель'     | '/object'      : 
                msg = await send_Embed(return_object(author_name, author_id, conditions, message.id))
                emojis = ['1️⃣', '2️⃣', '3️⃣', '4️⃣', '5️⃣', '6️⃣', '7️⃣', '8️⃣', '9️⃣', '🔟'] 
                for emoji in emojis: await msg.add_reaction(emoji)
            case '/отдать'      | '/give'        : await send_Embed(give_object(author_name, author_id, conditions))
            case '/лутбан'      | '/lootban'     : await send_Embed(lootban(author_name, author_id, conditions))

        if msg != None: supportive_add_GiveObject.give_object(msg.id)



@client.event
async def on_raw_reaction_add(payload):

    if payload.user_id in return_admins_id() and str(payload.message_id) in supportive("give_object"):
        msg = loot_by_reaction(payload.member, payload.user_id, payload.emoji, str(payload.message_id))
        await client.get_channel(payload.channel_id).send(msg)

    elif payload.user_id in Guilds[payload.guild_id].admins and payload.message_id in supportive("empty_guilds"):
        msg 
        


@client.event
async def on_guild_join(guild):
    kkr_loot = discord.utils.get(guild.channels, name='kkr_loot')
    if kkr_loot is not None:
        msg = await kkr_loot.send(embed = discord.Embed(
                title='Hi!',
                description='Please select the language below',
                colour=1752220))
        for lang in LOCALISITION: await msg.add_reaction(LOCALISITION[lang])
        supportive_add_EmptyGuilds(msg.id)
        GUILDS[guild.id] = Guilds(guild.id, msg.author.id)

        
if __name__ == "__main__":
    client.run('MTEyMTUxMTYzMjAxOTkyMzA3Ng.Gy_7ab.eZDOkA-Z3yjb1Vs7a0PihwVa8cA2UGZfVCFkBM')
