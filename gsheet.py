from mastersheethelper import writerdetails, masterbook
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

    def add_sheet(self, sheet : Sheet):
        self.sheets[sheet.sheetname] = sheet

    def get_sheet(self, sheetname):
        self.sheets.get(sheetname)

def get_writer_book_sheet(writername, sheetname):
    book = books.get(writername)
    if book is None:
        book = __add_book(writername)

    sheet = book.get_sheet(sheetname)
    if sheet is None:
        try:
            writersheet = book.book.worksheet(sheetname)
        except WorksheetNotFound:
            writersheet = book.book.add_worksheet(sheetname,100,10)   
        # add this sheet to the book
        sheet = Sheet(sheetname, writersheet)
        book.add_sheet(sheet)

       

def __add_book(writername):
    writer = writerdetails.get(writername)
    url = writer.sheeturl
    try:
        writerbook = gclient.open_by_url(url)
        
    except NoValidUrlKeyFound:
        writerbook = gclient.create(writer+'-Work Log')
            # update the sheeturl in the Writer
        url = writerbook.url
        writer.sheeturl = url
            # update the url in the actual masterbook
        masterWritersSheet = masterbook.worksheet('Writers')
        cell = masterWritersSheet.find(writer)
        masterWritersSheet.update_cell(cell.row, 3, url)
        # add to the book dictionary against the writername
    book = Book(writername, writerbook)
    books[writername] = book
    return book