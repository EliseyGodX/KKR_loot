import httplib2
from googleapiclient import discovery
from oauth2client.service_account import ServiceAccountCredentials
from logger import logger


KEY_FILE = 'API\kkr-loot-407512-e26cdf889d4f.json'
SHEET = 'KKR_loot'
P = 'googleSheets.google_scriber'


# result = service.spreadsheets().values().get(spreadsheetId=SPREADSHEET_ID, range=SHEET).execute()
# values = result.get('values', [])
@logger.catch
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


@logger.catch
def trial_for_link(trial_link: str) -> bool:
    try: 
        service.spreadsheets().get(spreadsheetId=trial_link).execute()
        return True
    except: 
        return False
        

