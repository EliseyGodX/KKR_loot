import httplib2
from googleapiclient import discovery
from googleapiclient.errors import HttpError
from oauth2client.service_account import ServiceAccountCredentials
import json
from logger import logger


KEY_FILE = 'API\kkr-loot-407512-e26cdf889d4f.json'
SHEET = 'KKR_loot'
P = 'googleSheets.google_scriber'

class GoogleScriber:
    
    def __init__(self) -> None:
        
        try:
            creds_for_service = ServiceAccountCredentials.from_json_keyfile_name(KEY_FILE, 
                                        ['https://www.googleapis.com/auth/spreadsheets'])
            http_auth = creds_for_service.authorize(httplib2.Http())
            self.service = discovery.build('sheets', 'v4', http=http_auth)
            
            logger.debug(f'---{P} initialization---')

        except Exception as exc:
            logger.critical(f'{P} CRITICAL ERROR: \n{exc}')
            exit()


    def trial_for_link(self, trial_link: str) -> bool:
        try: 
            self.service.spreadsheets().get(spreadsheetId=trial_link).execute()
            logger.debug(f'{P} test link (succes) - {trial_link}')
            return True
        except: 
            return False
        

    @logger.catch
    def sheet_parser(self, link: str, x: int, y: int, 
                    orient: str, range_: int) -> dict:
        try:
            result = self.service.spreadsheets().values().get(spreadsheetId=link, range=SHEET).execute()
            values = result.get('values', [])
        except Exception as exc:
            logger.error(f'{P} in sheet_parser {link} - {exc}')
            return False  # Error
        
        
        loot_que = {}
        coord = {}
        if orient == '|':
            for i in range(len(values)):
                for j in range(len(values[i])):
                    if values[i][j].startswith('id='):
                        key = values[i][j].split('=')[1]
                        queue = []
                        having = []
                        coord[int(key)] = {'queue': [], 'having': []}
                        for slot in range(range_):
                            try: queue.append(values[i+y+slot][j+x])
                            except: queue.append('')
                            try: having.append(values[i+y+slot][j+x+1])
                            except: having.append('')
                            coord[int(key)]['queue'].append([j+x+1, i+y+slot+1])
                            coord[int(key)]['having'].append([j+x+1+1, i+y+slot+1])
                        loot_que[int(key)] = {'queue': queue, 'having': having}

        range_colors = []
        for item in coord:
            range_colors.append(SHEET + '!' + convert_coord((coord[item]['queue'][0])) + 
                                ':' + convert_coord((coord[item]['having'][range_-1])))

        request = self.service.spreadsheets().get(spreadsheetId=link, 
                                                  ranges=range_colors, 
                                                  fields='sheets.data.rowData.values.effectiveFormat.backgroundColor', 
                                                  includeGridData=True).execute()
        color = {}
        i = 0
        for item in coord:
            color[item] = {'queue': [], 'having': []}
            item_cells = request['sheets'][0]['data'][i]['rowData']
            for row in range(len(item_cells)):
                color[item]['queue'].append(item_cells[row]['values'][0]['effectiveFormat']['backgroundColor'])
                color[item]['having'].append(item_cells[row]['values'][1]['effectiveFormat']['backgroundColor'])
            i += 1

        return coord, color



    def writing_to_the_sheet(self, link: str, data: dict, x: int, y: int, 
                    orient: str, range_: int) -> bool | str:
        sheet = self.service.spreadsheets().values().get(spreadsheetId=link, 
                                                    range=SHEET).execute().get('values', [])
        execute_data = []
        
        if orient =='|':
            for i in range(len(sheet)):  # y
                for j in range(len(sheet[i])):  # x
                    if sheet[i][j].startswith('id='):
                        key = int(sheet[i][j].split('=')[1])
                        execute_range = f'{convert_coord([j+x, i+y+1])}:{convert_coord([j+x+2, i+y+range_+1])}'
                        values = []
                        for indx in range(range_):
                            values.append([data[key]['queue'][indx],
                                        data[key]['having'][indx]])

                        execute_data.append({
                            "range": f"{SHEET}!{execute_range}",
                            "majorDimension": "ROWS",     
                            "values": values          
                        })
        try:               
            self.service.spreadsheets().values().batchUpdate(spreadsheetId = link, body = {
            "valueInputOption": "USER_ENTERED",
            "data": execute_data
            }).execute()
            logger.debug(f'{P} writing_to_the_sheet (succes) - {link}')
        except HttpError as error:
            error = error.content.decode("utf-8")
            return eval(error)['error']['message']
        else: return True
        


    def class_colour(self, link: str, count: int) -> tuple:
        range_ = convert_coord((1, 1)) + ':' + convert_coord((count+1, 1))
        request = self.service.spreadsheets().get(spreadsheetId=link, ranges=f'{SHEET}!{range_}', includeGridData=True).execute()
        classes_colour = [request['sheets'][0]['data'][0]['rowData'][0]['values'][count]['effectiveFormat']['backgroundColorStyle']['rgbColor']]
        for i in range(count):
            classes_colour.append(request['sheets'][0]['data'][0]['rowData'][0]['values'][i]['effectiveFormat']['backgroundColorStyle']['rgbColor'])
        return classes_colour


    
    




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


