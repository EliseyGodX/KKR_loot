import httplib2
from googleapiclient import discovery
from oauth2client.service_account import ServiceAccountCredentials
from logger import logger


KEY_FILE = 'API\kkr-loot-407512-e26cdf889d4f.json'
SHEET = 'KKR_loot'
P = 'googleSheets.google_scriber'


def googleSheets_initialization() -> None:
    global KEY_FILE, SHEET, creds, service
    
    try:
        creds = ServiceAccountCredentials.from_json_keyfile_name(KEY_FILE, ['https://www.googleapis.com/auth/spreadsheets'])
        http_auth = creds.authorize(httplib2.Http())
        service = discovery.build('sheets', 'v4', http=http_auth)
        
        logger.debug(f'---{P} initialization---')

    except Exception as exc:
        logger.critical(f'{P} CRITICAL ERROR: \n{exc}')
        exit()


def trial_for_link(trial_link: str) -> bool:
    try: 
        service.spreadsheets().get(spreadsheetId=trial_link).execute()
        return True
    except: 
        return False
    

@logger.catch
def sheet_parser(link: str, x: int, y: int, 
                 orient: str, range_: int) -> dict:
    try:
        result = service.spreadsheets().values().get(spreadsheetId=link, range=SHEET).execute()
        values = result.get('values', [])
    except Exception as exc:
        logger.error(f'{P} in sheet_parser {link}')
        return False  # Error
    for _ in values: print(len(_), _)
    loot_que = {}
    for i in range(len(values)):
        for j in range(len(values[i])):
            if values[i][j].startswith('id='):
                key = values[i][j].split('=')[1]
                queue = []
                having = []
                if orient == '|':
                    for slot in range(range_):
                        try: queue.append(values[i+y+slot][j+x])
                        except: queue.append('')
                        try: having.append(values[i+y+slot][j+x+1])
                        except: having.append('')
                loot_que[int(key)] = {'queue': queue, 'having': having}
    return loot_que