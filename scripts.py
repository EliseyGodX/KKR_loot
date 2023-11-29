from loguru import logger
from guilds import *
import json

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

_color_embed = {
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







# scripts for on_ready

@logger.catch
def language_initialization() -> dict:
    global LANGUAGE

    try:
        LANGUAGE = open_json('localization/content')
        with open('localization/command.json', encoding='utf-8') as f:
            COMMAND = json.load(f)

        logger.debug('---LANGUAGE_INITIALIZATION---')
        return COMMAND
    
    except Exception as exc:
        logger.critical(f'CRITICAL ERROR IN language_initialization: \n{exc}')
        exit()



@logger.catch
def logged() -> None:
    try:
        if (isinstance(_color_embed['success'], int)  # checking for the correctness of colors for Embed
            and isinstance(_color_embed['important_change'], int)
            and isinstance(_color_embed['error'], int)):     logger.debug('---LOGED---')
        else: raise IOError('bad color')

    except Exception as exc:
        logger.critical(f'CRITICAL ERROR IN logged: \n{exc}')






# scripts for on_message

@logger.catch
def admins(log: tuple, language: str, admins: dict) -> tuple:
    try:
        title = LANGUAGE[language]['admins_title']
        content = LANGUAGE[language]['admins_content'] + '\n' + '\n'.join(admins)
        logger.debug(f'{log[0]} --|-- {log[1]} | {log[2]} --|-- {log[3]} | {log[4]} --> SUCCESS')
        return (title, content, _color_embed['success'])
    
    except Exception as exc:
        logger.error(f'ERROR IN admins: {log[0]} --|-- {log[1]} | {log[2]} --|-- {log[3]} | {log[4]}\n{exc}')
        return (LANGUAGE[language]['error_title'],
                LANGUAGE[language]['error_content'], 
                _color_embed['error'], 
                'ERROR -> admins')






# scripts for on_raw_reaction_add

@logger.catch
def start_select_language(LOCALISITION: dict, emoji, log: tuple):
    flag = False

    for lang in LOCALISITION:
        if LOCALISITION[lang] == str(emoji):
            flag = True
            break

    if flag is False:

        logger.debug(f'{log[0]} --|-- {log[1]} | {log[2]} --|-- {log[3]} | {log[4]} --> FAIL (incorrect language)')
        return None, {'title': 'ERROR!', 'description': 'incorrect language', 'colour': _color_embed['error']}

    logger.debug(f'{log[0]} --|-- {log[1]} | {log[2]} --|-- {log[3]} | {log[4]} --> SUCCESS ({lang})')
    return lang, {'title': 'KKR_loot', 
                  'description': LANGUAGE[lang]['Language changed successfully'], 
                  'colour': _color_embed['important_change']}
    






# scripts for on_guild_join

@logger.catch
def new_guild_initialization(log) -> None: 
    logger.debug(f'{log[0]} --|-- {log[1]} | {log[2]} --> SUCCESS')


