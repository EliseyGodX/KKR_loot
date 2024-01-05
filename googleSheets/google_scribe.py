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
        

    def sheet_parser(self, link: str, x: int, y: int, 
                    orient: str, range_: int, classes_count: int) -> dict and dict and dict:
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
                        coord[int(key)] = []
                        for slot in range(range_):
                            try: queue.append(values[i+y+slot][j+x])
                            except: queue.append('')
                            try: having.append(values[i+y+slot][j+x+1])
                            except: having.append('')
                            if slot == 0:
                                coord[int(key)].append([j+x+1, i+y+slot+1])
                            elif slot == range_-1:    
                                coord[int(key)].append([j+x+1+1, i+y+slot+1])
                        loot_que[int(key)] = {'queue': queue, 'having': having}

            range_colors = []
            for item in coord:
                range_colors.append(SHEET + '!' + convert_coord((coord[item][0])) + 
                                    ':' + convert_coord((coord[item][1])))

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
            
        range_ = convert_coord((1, 1)) + ':' + convert_coord((classes_count+1, 1))
        request = self.service.spreadsheets().get(spreadsheetId=link, ranges=f'{SHEET}!{range_}', includeGridData=True).execute()
        classes_color = [request['sheets'][0]['data'][0]['rowData'][0]['values'][classes_count]['effectiveFormat']['backgroundColorStyle']['rgbColor']]
        for i in range(classes_count):
            classes_color.append(request['sheets'][0]['data'][0]['rowData'][0]['values'][i]['effectiveFormat']['backgroundColorStyle']['rgbColor'])

        return loot_que, coord, color, classes_color



    def writing_to_the_sheet(self, link: str, data: dict, data_color: dict, 
                             orient: str, ranges: int) -> bool:
        if orient == '|':
            requests = []
            for key in ranges:
                cell_range = key
                start_row = ranges[key][0][1] - 1
                start_col = ranges[key][0][0] - 1
                end_row = ranges[key][1][1] - 1
                end_col = ranges[key][1][0] - 1

                if key in data:
                    for cell_num in range(start_row, end_row + 1):
                        cell_text_queue = data[key].get("queue", [])[cell_num - start_row]
                        cell_text_having = data[key].get("having", [])[cell_num - start_row]

                        request = {
                            'repeatCell': {
                                'range': {
                                    'sheetId': 0,
                                    'startRowIndex': cell_num,
                                    'endRowIndex': cell_num + 1,
                                    'startColumnIndex': start_col,
                                    'endColumnIndex': end_col
                                },
                                'cell': {
                                    'userEnteredValue': {
                                        'stringValue': cell_text_queue
                                    }
                                },
                                'fields': 'userEnteredValue'
                            }
                        }
                        requests.append(request)

                        
                        request = {
                            'repeatCell': {
                                'range': {
                                    'sheetId': 0,
                                    'startRowIndex': cell_num,
                                    'endRowIndex': cell_num + 1,
                                    'startColumnIndex': start_col + 1,
                                    'endColumnIndex': end_col + 1
                                },
                                'cell': {
                                    'userEnteredValue': {
                                        'stringValue': cell_text_having
                                    }
                                },
                                'fields': 'userEnteredValue'
                            }
                        }
                        requests.append(request)
                
                        
                if key in data_color:
                    for cell_num in range(start_row, end_row + 1):
                        cell_color_queue = data_color[key].get("queue", [])[cell_num - start_row]
                        cell_color_having = data_color[key].get("having", [])[cell_num - start_row]

                        request = {
                            'repeatCell': {
                                'range': {
                                    'sheetId': 0,
                                    'startRowIndex': cell_num,
                                    'endRowIndex': cell_num + 1,
                                    'startColumnIndex': start_col,
                                    'endColumnIndex': end_col
                                },
                                'cell': {
                                    'userEnteredFormat': {
                                        'backgroundColor': cell_color_queue
                                    }
                                },
                                'fields': 'userEnteredFormat.backgroundColor'
                            }
                        }
                        requests.append(request)

                        request = {
                            'repeatCell': {
                                'range': {
                                    'sheetId': 0,
                                    'startRowIndex': cell_num,
                                    'endRowIndex': cell_num + 1,
                                    'startColumnIndex': start_col + 1,
                                    'endColumnIndex': end_col + 1
                                },
                                'cell': {
                                    'userEnteredFormat': {
                                        'backgroundColor': cell_color_having
                                    }
                                },
                                'fields': 'userEnteredFormat.backgroundColor'
                            }
                        }
                        requests.append(request)

            batch_update_request = self.service.spreadsheets().batchUpdate(spreadsheetId=link, body={'requests': requests})
            try:
                response = batch_update_request.execute()
                logger.debug(f'{P} writing to the sheet (sucess) - {link}')
                return True
            except HttpError as e:
                logger.critical(f'{P} ERROR writing to the sheet - {link}: \n{e}')
                return False

    
    




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


