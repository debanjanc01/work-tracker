from gsheetclient import gclient, MASTER_URL
from typing import List, Dict

masterbook = gclient.open_by_url(MASTER_URL)

class Writer:
    def __init__(self, name, email, sheeturl):
        self.name = name
        self.email = email
        self.sheeturl = sheeturl

def __get_writers() -> Dict[str, Writer]:
    writers = dict()
    global masterbook
    sheet = masterbook.worksheet('Writers')
    recs = sheet.get_all_records()
    for rec in recs:
        name = rec['Name']
        email = rec['Email']
        sheeturl = rec['Sheet']
        writer = Writer(name, email, sheeturl)
        writers[name] = writer
    
    return writers

# A dictionary with writername -> Writer{Name, Email, Sheet}
writerdetails = __get_writers()

def __get_sheets():
    worksheets = masterbook.worksheets()
    sheets = dict()
    for worksheet in worksheets:
        sheetname = worksheet.title
        sheets[sheetname] = worksheet
    return sheets

mastersheets = __get_sheets()

def create_master_sheet(sheetname):
    sheet  = masterbook.add_worksheet(sheetname, 100, 15)
    mastersheets[sheetname] = sheet
    return sheet

def get_projects():
    sheet = masterbook.worksheet('Projects')
    rec = sheet.get_all_records()
    return rec
