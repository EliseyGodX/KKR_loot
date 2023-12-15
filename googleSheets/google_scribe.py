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
        logger.debug(f'{P} test link (succes) - {trial_link}')
        return True
    except: 
        return False
    


def sheet_parser(link: str, x: int, y: int, 
                 orient: str, range_: int) -> dict:
    try:
        result = service.spreadsheets().values().get(spreadsheetId=link, range=SHEET).execute()
        values = result.get('values', [])
    except Exception as exc:
        logger.error(f'{P} in sheet_parser {link}')
        return False  # Error
    
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



def writing_to_the_sheet(link: str, data: dict, x: int, y: int, 
                  orient: str, range_: int) -> bool:
    sheet = service.spreadsheets().values().get(spreadsheetId=link, 
                                                range=SHEET).execute().get('values', [])
    execute_data = []
    if orient =='|':
        for i in range(len(sheet)):  # y
            for j in range(len(sheet[i])):  # x
                if sheet[i][j].startswith('id='):
                    key = int(sheet[i][j].split('=')[1])
                    execute_range = f'{convert_coord([j+x+1, i+y+1])}:{convert_coord([j+x+2, i+y+range_+1])}'
                    values = []
                    for indx in range(range_):
                        values.append([data[key]['queue'][indx],
                                       data[key]['having'][indx]])

                    execute_data.append({
                        "range": f"{SHEET}!{execute_range}",
                        "majorDimension": "ROWS",     
                        "values": values          
                    })


    service.spreadsheets().values().batchUpdate(spreadsheetId = link, body = {
    "valueInputOption": "USER_ENTERED",
    "data": execute_data
    }).execute()
    
    




def convert_coord(coord: list | tuple) -> str:
    column_index = ''
    row_index = ''
    if coord[0] <= 26:
        column_index = chr(ord('A') + coord[0] - 1)
    else:
        first_letter_index = (coord[0] - 1) // 26
        second_letter_index = (coord[0] - 1) % 26 + 1
        column_index += chr(ord('A') + first_letter_index - 1) + chr(ord('A') + second_letter_index - 1)
    row_index = str(coord[1])
    return column_index + row_index


