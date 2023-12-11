import googleSheets as GS
import DB
import json
from logger import logger


P = 'discordModules.scripts'

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







# scripts for on_ready

@logger.catch
def language_initialization() -> dict:
    global LANGUAGE

    try:
        LANGUAGE = open_json('localization/content')
        with open('localization/command.json', encoding='utf-8') as f:
            COMMAND = json.load(f)

        logger.debug(f'{P}: ---language initialization---')
        return COMMAND
    
    except Exception as exc:
        logger.critical(f'{P} CRITICAL ERROR: \n{exc}')
        exit()



@logger.catch
def logged() -> None:
    try:
        if (isinstance(color_embed['success'], int)  # checking for the correctness of colors for Embed
            and isinstance(color_embed['important_change'], int)     
            and isinstance(color_embed['error'], int)):     logger.debug('---logged---')
        else: raise IOError('bad color')

    except Exception as exc:
        logger.critical(f'{P} CRITICAL ERROR (in logged): \n{exc}')
        exit()






# scripts for on_message

@logger.catch
def admins(log: tuple, lang: str, admins: dict) -> tuple:
    try:
        title = LANGUAGE[lang]['admins_title']
        content = LANGUAGE[lang]['admins_content'] + '\n' + '\n'.join(admins)
        logger.debug(f'{P} {log[0]} --|-- {log[1]} | {log[2]} --|-- {log[3]} | {log[4]} --> SUCCESS')
        return (title, content, color_embed['success'])
    
    except Exception as exc:
        logger.error(f'{P} ERROR: {log[0]} --|-- {log[1]} | {log[2]} --|-- {log[3]} | {log[4]}\n{exc}')
        return (LANGUAGE[lang]['error_title'],
                LANGUAGE[lang]['error_content'], 
                color_embed['error'], 
                'ERROR -> admins')



@logger.catch
def link(log: tuple, lang: str, sheet_id: str) -> tuple:
    try:
        sheet_id = GS.trial_for_link(sheet_id)

        if sheet_id is False:
            logger.debug(f'{P} {log[0]} --|-- {log[1]} | {log[2]} --|-- {log[3]} | {log[4]} --> FAIL (invalid ID)')
            return (LANGUAGE[lang]['error_title'],
                LANGUAGE[lang]['link_bad_content'], 
                color_embed['error']), True
        
        title = LANGUAGE[lang]['link_title']
        content = LANGUAGE[lang]['link_content']
        color = color_embed['success']
        logger.debug(f'{P} {log[0]} --|-- {log[1]} | {log[2]} --|-- {log[3]} | {log[4]} --> SUCCESS')
        
        return (title, content, color), True

    except Exception as exc:
        logger.error(f'{P} ERROR: {log[0]} --|-- {log[1]} | {log[2]} --|-- {log[3]} | {log[4]}\n{exc}')
        return (LANGUAGE[lang]['error_title'],
                LANGUAGE[lang]['error_content'], 
                color_embed['error'], 
                'ERROR -> admins'), False



@logger.catch
def link_second(lang: str) -> tuple:
    try:
        title = LANGUAGE[lang]['link_second_title']
        content = LANGUAGE[lang]['link_second_content']
        return (title, content, color_embed['important_change'])
    
    except Exception as exc:
        logger.error(f'{P} ERROR (in link_second): \n{exc}')
        return (LANGUAGE[lang]['error_title'],
                LANGUAGE[lang]['error_content'], 
                color_embed['error'], 
                'ERROR -> admins')





# scripts for on_raw_reaction_add

@logger.catch
def start_select_language(LOCALISITION: dict, emoji, log: tuple) -> dict:
    flag = False

    for lang in LOCALISITION:
        if LOCALISITION[lang] == str(emoji):
            flag = True
            break

    if flag is False:

        logger.debug(f'{P} {log[0]} --|-- {log[1]} | {log[2]} --|-- {log[3]} | {log[4]} --> FAIL (incorrect language)')
        return None, {'title': 'ERROR!', 'description': 'incorrect language', 'colour': color_embed['error']}

    logger.debug(f'{P} {log[0]} --|-- {log[1]} | {log[2]} --|-- {log[3]} | {log[4]} --> SUCCESS ({lang})')
    return lang, {'title': 'KKR_loot', 
                  'description': LANGUAGE[lang]['start_select_language'], 
                  'colour': color_embed['important_change']}
    


@logger.catch
def start_select_language_second(lang: str, log: tuple) -> dict:
    try:
        title = 'KKR_loot'
        content = LANGUAGE[lang]['admins_content']
        logger.debug(f'{P} {log[0]} --|-- {log[1]} | {log[2]} --|-- {log[3]} | {log[4]} --> SUCCESS')
        return (title, content, color_embed['important_change'])
    
    except Exception as exc:
        logger.error(f'{P} ERROR: {log[0]} --|-- {log[1]} | {log[2]} --|-- {log[3]} | {log[4]}\n{exc}')
        return (LANGUAGE[lang]['error_title'],
                LANGUAGE[lang]['error_content'], 
                color_embed['error'])






# scripts for on_guild_join

@logger.catch
def new_guild_initialization(log) -> None: 
    logger.debug(f'{P} {log[0]} --|-- {log[1]} | {log[2]} --> SUCCESS')


