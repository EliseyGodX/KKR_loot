import json
from loguru import logger
from guilds import *

logger.add('debug.log', format='{time} || {level} || {message}', rotation='2 MB')

classes_emoji = {
           'dk': '<:dk:1164567710320050257>', 
           'druid': '<:druid:1164567711775473806>', 
           'hunter': '<:hunter:1164567715462258699>', 
           'mage': '<:mage:1164567718196957306>', 
           'paladin': '<:paladin:1164567719581069453>',             
           'priest': '<:priest:1164567721103605870>', 
           'rogue': '<:rogue:1164567723762794646>', 
           'shaman': '<:shaman:1164567725029466202>', 
           'warlock': '<:warlock:1164567727336329358>', 
           'warrior': '<:warrior:1164567728993083422>'
           }

color_embed = {
            'success': 5763719,
            'error': 15548997,
            'important_change': 3426654

}


def open_json(file: str) -> dict:                              #
    with open(file + '.json', encoding='utf-8') as f:          #
        DICT = json.load(f)                                    # open
    return DICT                                                # and
                                                               # close
def close_json(file: str, DICT: dict) -> None:                 # json
    with open(file + '.json', 'w', encoding='utf-8') as f:     #
        json.dump(DICT, f, indent=3, ensure_ascii=False)       #


@logger.catch
def language_initialization() -> dict:
    global LANGUAGE
    LANGUAGE = open_json('localization/content')
    close_json('localization/content.json', LANGUAGE)
    logger.debug('---LANGUAGE_INITIALIZATION---')



@logger.catch
def logged(): 
    logger.debug('---LOGED---')

@logger.catch
def new_guild_initialization(log): 
    logger.debug(f'{log[0]} --|-- {log[1]} | {log[2]} --> SUCCESS')



@logger.catch
def return_admin(author_name: str, author_id: int):  # /admins
    logger.debug(f'{author_name} | {author_id} --> /admins (success)')
    return ['title', 'content', 1752220]



@logger.catch
def registration(author_name: str, author_id: int, conditions: list): # /registration screen_name char_name char_classes
    MEMBERS = open_json('members') 

    def check_id():
        for name in MEMBERS: 
            if MEMBERS[name]["id"] == author_id: return True

    try: # Condition separation, validation of the class                                                          
        screen_name = conditions[0].lower()                                      
        char_name = conditions[1].lower()                           
        char_classes = conditions[2].lower()  
        print(screen_name)                                   
        if char_classes not in classes_emoji: 0/0     
    except: 
        logger.debug(f'{author_name} | {author_id} --> /registration (fail)')
        close_json('members', MEMBERS)
        return 'Введите корректные значения'                                    

    if screen_name.lower() in MEMBERS or check_id() is True: # Checking for the existence of a member
        logger.debug(f'{author_name} | {author_id} --> /registration (fail)')
        close_json('members', MEMBERS)
        return 'Такой пользователь уже существует'
    
    MEMBERS[screen_name] = {
        "id": author_id,
        "name": author_name,
        "char": char_name,
        "class": char_classes,
        "banloot": 0
    }
    close_json('members', MEMBERS)

    logger.debug(f'{author_name} | {author_id} --> /registration (success)')
    return 'Успешно'



@logger.catch
def return_members(author_name: str, author_id: int): # /members
    MEMBERS = open_json('members')
    close_json('members', MEMBERS)

    list_members = ''
    for class_ in classes_emoji: # sorting by class
        for member in MEMBERS:
            if MEMBERS[member]["class"] == class_:
                list_members += f'{MEMBERS[member]["char"].title()} | {classes_emoji[class_]} | {member} | Банлутов: {MEMBERS[member]["banloot"]} \n'
    
    logger.debug(f'{author_name} | {author_id} --> /members (success)')
    return list_members



@logger.catch
def change(author_name: str, author_id: int, conditions: list): # /change old_name new_screen_name new_char_name new_char_classes
    MEMBERS = open_json('members')

    try: # Separation of conditions, verification of id and validity of conditions
        old_screen_name = conditions[0]                                                           
        screen_name = conditions[1]                                      
        char_name = conditions[2]                                        
        char_classes = conditions[3]                                     
        if char_classes not in classes_emoji or author_id != MEMBERS[old_screen_name]["id"]: 0/0    
    except: 
        logger.debug(f'{author_name} | {author_id} --> /change (fail)')
        close_json('members', MEMBERS)
        return 'Введите корректные значения'                                    

    banloot = MEMBERS[old_screen_name]["banloot"]
    MEMBERS.pop(old_screen_name)

    MEMBERS[screen_name.lower()] = {
        "id": author_id,
        "name": author_name,
        "char": char_name,
        "class": char_classes,
        "banloot": banloot
    }
    close_json('members', MEMBERS)

    logger.debug(f'{author_name} | {author_id} --> /change (success)')
    return 'Успешно'



@logger.catch
def return_object(author_name: str, author_id: int, conditions: list, message_id): # /object

    def lootban_object(looter):
        if MEMBERS[looter]["banloot"] != 0:
            return f':warning:ЛУТБАН:warning: - {MEMBERS[looter]["banloot"]} кд'
        else: return ''
    
    def return_count(looter, lst):
        count = 0
        while lst[count] != looter:
            count += 1
        return count + 1 
        
    LOOT = open_json('loot')
    MEMBERS = open_json('members')
    close_json('members', MEMBERS)

    try:
        for count in range(len(conditions)): conditions[count] = conditions[count].lower()
        conditions = ' '.join(conditions)
        np = '\n'
        loot = f'''==={conditions}===
слот: {LOOT[conditions]["slot"]}
ilvl: {LOOT[conditions]["ilvl"]}
каста: {LOOT[conditions]["caste"]}
{LOOT[conditions]["description"]}

Очередь: {np}{np.join(f'{return_count(looter, LOOT[conditions]["queue"])}. {classes_emoji[MEMBERS[looter]["class"]]} {MEMBERS[looter]["char"].title()} {lootban_object(looter)}' for looter in LOOT[conditions]["queue"])}

Полутавшие: {np}{np.join(f'{classes_emoji[MEMBERS[looter]["class"]]} {MEMBERS[looter]["char"].title()}' for looter in LOOT[conditions]["have"])}'''
        close_json('loot', LOOT)
        logger.debug(f'{author_name} | {author_id} --> /object (success)')

        SUPPORIVE = open_json('supportive')
        SUPPORIVE["temporary_conditions"] = conditions
        close_json('supportive', SUPPORIVE)
        return loot

    except:
        close_json('loot', LOOT)
        logger.debug(f'{author_name} | {author_id} --> /object (fail)')
        return 'Пиксель не найден'



@logger.catch
def give_object(author_name: str, author_id: int, conditions: list): #/give looter object 
    LOOT = open_json('loot')
    MEMBERS = open_json('members')
    ADMINS = open_json('admins')

    if author_id not in ADMINS["admins"]:
        close_json('loot', LOOT)
        close_json('members', MEMBERS)
        close_json('admins', ADMINS)
        logger.debug(f'{author_name} | {author_id} --> /give (fail)')
        return 'Вы не админ'
    
    looter = conditions[0].lower()
    if looter not in MEMBERS: 
        close_json('loot', LOOT)
        close_json('members', MEMBERS)
        close_json('admins', ADMINS)
        logger.debug(f'{author_name} | {author_id} --> /give (fail)')
        return 'Пользователь не найден'
    
    try:
        for count in range(len(conditions)): conditions[count] = conditions[count].lower()
        conditions.pop(0)
        conditions = ' '.join(conditions)
        LOOT[conditions]["queue"]

        try: LOOT[conditions]["queue"].remove(looter)
        except:
            close_json('loot', LOOT)
            close_json('members', MEMBERS)
            close_json('admins', ADMINS)
            logger.debug(f'{author_name} | {author_id} --> /give (fail)')
            return f'{looter} не стоит в очереди на этот пиксель'
        
        LOOT[conditions]["have"].append(looter)
        close_json('loot', LOOT)
        close_json('members', MEMBERS)
        close_json('admins', ADMINS)
        logger.debug(f'{author_name} | {author_id} --> /give (success)')
        return 'Успешно'
    
    except:
        close_json('loot', LOOT)
        close_json('members', MEMBERS)
        close_json('admins', ADMINS)
        logger.debug(f'{author_name} | {author_id} --> /give (fail)')
        return 'Пиксель не найден'
    


@logger.catch
def lootban(author_name: str, author_id: int, conditions: list): # /lootban name num
    MEMBERS = open_json('members')
    ADMINS = open_json('admins')

    if author_id not in ADMINS["admins"]:
        close_json('members', MEMBERS)
        close_json('admins', ADMINS)
        logger.debug(f'{author_name} | {author_id} --> /lootban (fail)')
        return 'Вы не админ'
    
    try:
        MEMBERS[conditions[0].lower()]["banloot"] += int(conditions[1])
        close_json('members', MEMBERS)
        close_json('admins', ADMINS)
        logger.debug(f'{author_name} | {author_id} --> /lootban (success)')
        return 'Успешно'
    except:
        close_json('members', MEMBERS)
        close_json('admins', ADMINS)
        logger.debug(f'{author_name} | {author_id} --> /lootban (fail)')
        return 'Ошибка в игроке/кд лутбанов'



@logger.catch
def loot_by_reaction(author_name, author_id, emoji, supportive_id):
    try:
        LOOT = open_json('loot')  
        SUPPORTIVE = open_json('supportive')

        object_ = SUPPORTIVE["give_object"][supportive_id]
        emoji_to_num = {'1️⃣': 0,
                        '2️⃣': 1, 
                        '3️⃣': 2,
                        '4️⃣': 3, 
                        '5️⃣': 4, 
                        '6️⃣': 5, 
                        '7️⃣': 6, 
                        '8️⃣': 7, 
                        '9️⃣': 8, 
                        '🔟': 9}
        looter = LOOT[object_]["queue"][emoji_to_num[str(emoji)]]

        LOOT[object_]["queue"].remove(looter)

        
        LOOT[object_]["have"].append(looter)
        close_json('loot', LOOT)
        close_json('supportive', SUPPORTIVE)
        logger.debug(f'{author_name} | {author_id} --> /loot_by_reaction ({object_} -> {looter})')
        return f'{object_} -> {looter}'
    except: return 'Что-то пошло не так'


@logger.catch
def new_guild(LOCALISITION: dict, emoji, log: dict):
    flag = False
    print(LOCALISITION)
    for lang in LOCALISITION:
        print(lang, emoji, LOCALISITION[lang])
        if LOCALISITION[lang] == str(emoji):
            flag = True
            break

    if flag is False: 
        print('.')
        logger.debug(f'{log[0]} --|-- {log[1]} | {log[2]} --|-- {log[3]} | {log[4]} --> FAIL (incorrect language)')
        return 'empty', {'title': 'ERROR!', 'description': 'incorrect language', 'colour': color_embed['error']}

    logger.debug(f'{log[0]} --|-- {log[1]} | {log[2]} --|-- {log[3]} | {log[4]} --> SUCCESS ({lang})')
    return lang, {'title': 'KKR_loot', 
                  'description': LANGUAGE[lang]['Language changed successfully'], 
                  'colour': color_embed['important_change']}
    




def supportive_add_GiveObject(id_):
    SUPPORTIVE = open_json('supportive')
    SUPPORTIVE["give_object"][id_] = SUPPORTIVE["temporary_conditions"]
    SUPPORTIVE["temporary_conditions"] = None
    close_json('supportive', SUPPORTIVE)

def supportive(key):
    SUPPORTIVE = open_json('supportive')
    close_json('supportive', SUPPORTIVE)
    return SUPPORTIVE[key]

def return_admins_id():
    ADMINS = open_json('admins')
    close_json('admins', ADMINS)
    return ADMINS["admins"]

def supportive_add_EmptyGuilds(id_):
    SUPPORTIVE = open_json('supportive')
    SUPPORTIVE["empty_guilds"].append(id_)
    close_json('supportive', SUPPORTIVE)

def return_empty_guilds():
    SUPPORTIVE = open_json('supportive')
    close_json('supportive', SUPPORTIVE)
    return SUPPORTIVE["empty_guilds"]

def delete_EmptyGuild(id_):
    SUPPORTIVE = open_json('supportive')
    SUPPORTIVE["empty_guilds"].pop(id_)
    close_json('supportive', SUPPORTIVE)

def supportive_add_SettingsLanguage(id_):
    SUPPORTIVE = open_json('supportive')
    SUPPORTIVE["settings_language"].append(id_)
    close_json('supportive', SUPPORTIVE)