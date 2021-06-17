from datetime import datetime
import gspread
from gspread_formatting.batch_update_requests import format_cell_range
import TaskData
from typing import List
from gspread_formatting import CellFormat, Color, TextFormat
from gspread_formatting import *
import os
import win32api, win32con
import GSheetClient

def get_master_url():
    mainconfigfile = os.path.join(os.environ["APPDATA"], 'gspread', 'main_config.properties')
    if os.path.exists(mainconfigfile):
        with open(mainconfigfile, 'r') as f:
            url = f.readline()
    else:
        win32api.MessageBox(0, 'Missing File: ' +  mainconfigfile, 'File Missing!', win32con.MB_ICONWARNING) 
        exit(-1)
    url = url.strip()
    return url
    
MASTER_URL = get_master_url()
gclient = GSheetClient.gclient
masterbook = gclient.open_by_url(MASTER_URL)

writerworkbooks = {}

def getSheets():
    worksheets = masterbook.worksheets()
    sheetnames = []
    for worksheet in worksheets:
        sheetname = worksheet.title
        sheetnames.append(sheetname)
    return sheetnames

mastersheets = getSheets()



def getWriters():
    wmap = {}
    global masterbook
    sheet = masterbook.worksheet('Writers')
    recs = sheet.get_all_records()
    for rec in recs:
        name = rec['Name']
        email = rec['Email']
        sheeturl = rec['Sheet']
        values = {'Name': name, 'Email' : email, 'Sheet' : sheeturl}
        wmap[name] = values
    
    return wmap


writerdetails = getWriters()

def getProjects():
    global masterbook
    sheet = masterbook.worksheet('Projects')
    rec = sheet.get_all_records()
    return rec


def saveTasks(tasks : List[TaskData.TaskData]):
    projtasks = dict()
    writertasks = dict()
    for task in tasks:
        writer = task.writer
        proj = task.project
        
        #saving to master projects map
        if(proj in projtasks):
            ts = projtasks.get(proj)
        else:
            ts = list()
        ts.append(task)
        projtasks[proj] = ts

        #saving to writer specific project map
        # writer contains projects. each project contains tasks.
        if writer in writertasks:
            writerprojs = writertasks.get(writer)
            if proj in writerprojs:
                wpts = writerprojs.get(proj)
            else:
                wpts = list()
            wpts.append(task)
            writerprojs[proj] = wpts
        else:
            wpts = list()
            wpts.append(task)
            wpmap = dict()
            wpmap[proj] = wpts
            writertasks[writer] = wpmap

    #saving to main worksheet
    saveToMasterWorksheet(projtasks)

    #saving to projects worksheet
    val = saveToWriterWorksheet(writertasks)
    return val
def saveToMasterWorksheet(projtasks):
    for projname in projtasks:
        tasks = projtasks.get(projname)
        taskRows = transformTasks(tasks)
        if projname in mastersheets:
            projsheet = masterbook.worksheet(projname)
            projsheet.append_rows(taskRows)
        else:
            projsheet = masterbook.add_worksheet(projname,100,15)
            taskRows.insert(0,['Date','Project','Topic','Writer','Client Pay','Writer Pay','Income'])
            
            fmt = CellFormat(
                backgroundColor=Color(155, 155, 141),
                textFormat=TextFormat(bold=True, foregroundColor=Color(0, 0, 0)),
                horizontalAlignment='CENTER'
                )
            projsheet.append_rows(taskRows)
            format_cell_range(projsheet,'1:1', fmt)
            mastersheets.append(projname)

def saveToWriterWorksheet(writertasks):
    for writer in writertasks:
        writerbook = None
        
        #get the workbook for the writer
        newworkbook = False
        if writer in writerworkbooks:
            writerbook = writerworkbooks.get(writer)
        else:
            url = writerdetails.get(writer).get('Sheet')
            email = writerdetails.get(writer).get('Email')
            writerbook = None
            try:
                writerbook = gclient.open_by_url(url)
            except gspread.exceptions.NoValidUrlKeyFound:
                newworkbook = True
                writerbook = gclient.create(writer+'-Work Log')
                url = writerbook.url
                writerdet = writerdetails.get(writer)
                writerdet['Sheet'] = url
                writerdetails[writer] = writerdet
                newworkbook = True

                masterWritersSheet = masterbook.worksheet('Writers')
                cell = masterWritersSheet.find(writer)
                row = cell.row
                masterWritersSheet.update_cell(row, 3, url)

            writerworkbooks[writer] = writerbook
        projects = writertasks.get(writer)
        for project in projects:
            tasks = projects.get(project)            
            taskRows = transformTaskToWriterRows(tasks)
            writersheet = None
            headerRequired = False
            projsheetname = project.split('-')[0]
            try:
                writersheet = writerbook.worksheet(projsheetname)
            except gspread.exceptions.WorksheetNotFound:
                writersheet = writerbook.add_worksheet(projsheetname,100,10)   
                headerRequired = True
            if headerRequired:
                taskRows.insert(0, ['Date', 'Topic', 'Word Count', 'Pay', 'Status'])
                
            writersheet.append_rows(taskRows)
            if headerRequired:
                fmt = CellFormat(
                backgroundColor=Color(155, 155, 141),
                textFormat=TextFormat(bold=True, foregroundColor=Color(0, 0, 0)),
                horizontalAlignment='CENTER'
                )
                format_cell_range(writersheet,'1:1', fmt)
                headerRequired = False
        
        if newworkbook:
            sheet1 = writerbook.worksheet('Sheet1')
            writerbook.del_worksheet(sheet1)
            try:
                writerbook.share(email, perm_type='user', role='writer')
            except gspread.exceptions.APIError:
                    return f"{writer}-Work Log workbook could not shared with {email}"

def transformTaskToRow(task :TaskData.TaskData):
    return [str(task.date), str(task.project), str(task.topic), str(task.writer), str(task.clientPay), str(task.writerPay), str(task.income)]
 
def transformTasks(taskList : List[TaskData.TaskData]):
    rows = []
    for task in taskList:
        row = transformTaskToRow(task)
        rows.append(row)
    return rows

def transformTaskToWriterRows(taskList : List[TaskData.TaskData]):
    rows = []
    for task in taskList:
        date = task.date
        topic = task.topic
        wordcount = task.wordcount
        pay = task.writerPay
        row = [date, topic, wordcount, pay]
        rows.append(row)
    return rows