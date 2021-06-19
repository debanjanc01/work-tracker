from mastersheethelper import writerdetails, mastersheets
from gsheetclient import gclient
from gspread.exceptions import NoValidUrlKeyFound, WorksheetNotFound

books = {}


class Sheet:
    def __init__(self, sheetname, sheet):
        self.sheetname = sheetname
        self.sheet = sheet


class Book:
    def __init__(self, writername, book):
        self.writername = writername
        self.book = book
        self.sheets = dict()

    def add_sheet(self, sheet: Sheet):
        self.sheets[sheet.sheetname] = sheet

    def get_sheet(self, sheetname):
        self.sheets.get(sheetname)

                 
def get_writer_book_sheet(writername, sheetname):
    """  returns dictionary of following key-values: \n
    Gsheet -> Acual google sheet object \n
    Book_Created = True/False based on if a new book has been created \n
    Sheet_Created = True/False based on if a new sheet has been created  """

    book = books.get(writername)
    sheetvalues = dict()
    if book is None:
        book = __add_book(writername, sheetvalues)
        
    sheet = book.get_sheet(sheetname)
    if sheet is None:
        try:
            writersheet = book.book.worksheet(sheetname)
        except WorksheetNotFound:
            writersheet = book.book.add_worksheet(sheetname, 100, 10)
        # add this sheet to the book
        sheet = Sheet(sheetname, writersheet)
        book.add_sheet(sheet)
        sheetvalues['Sheet_Created'] = True
    sheetvalues['GSheet'] = sheet.sheet
    return sheetvalues


def __add_book(writername, sheetvalues):
    writer = writerdetails.get(writername)
    url = writer.sheeturl
    try:
        writerbook = gclient.open_by_url(url)

    except NoValidUrlKeyFound:
        writerbook = __create_google_book(writer)
        sheetvalues['Book_Created'] = writerbook
        # add to the book dictionary against the writername
    book = Book(writername, writerbook)
    books[writername] = book
    return book


def __create_google_book(writer):
    writerbook = gclient.create(writer.name+'-Work Log')
    # update the sheeturl in the Writer
    url = writerbook.url
    writer.sheeturl = url
    # update the url in the actual masterbook
    masterWritersSheet = mastersheets.get('Writers')
    cell = masterWritersSheet.find(writer.name)
    masterWritersSheet.update_cell(cell.row, 3, url)
    return writerbook
