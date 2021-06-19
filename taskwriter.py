import mastersheethelper 
from taskdata import TaskData
from typing import List
import tasksegregator
from concurrent.futures import ThreadPoolExecutor
import gwritersheethelper
import sheetrowtransformer
import gspread_formatting 
from gspread.exceptions import APIError

def write_task(taskrows, gsheet):
    gsheet.append_rows(taskrows)

    
def save_tasks_to_sheets(tasks : List[TaskData]):
    errors = list()
    projtasks, writertasks = tasksegregator.segregate_tasks(tasks)
    with ThreadPoolExecutor(max_workers=__get_max_workers(projtasks, writertasks)) as executor:
        __submit_mainsheet_proj_tasks(projtasks, executor, errors)
        __submit_writer_proj_tasks(writertasks, executor, errors)
    if len(errors) == 0:
        return None
    else:
        return errors

def __submit_mainsheet_proj_tasks(projtasks, executor, errors: List):
    for projname in projtasks:
        tasks = projtasks.get(projname)
        sheet = mastersheethelper.mastersheets.get(projname)
        taskrows = sheetrowtransformer.transform_master_sheet_rows(tasks)
        if sheet is None:
            sheet = mastersheethelper.create_master_sheet(projname)
            taskrows.insert(0,['Date','Topic','Word Count','Writer','Client Pay','Writer Pay','Income'])
            __format_header_row(sheet)
        executor.submit(write_task, taskrows, sheet)

def __submit_writer_proj_tasks(writertasks, executor, errors : List):
    for writer in writertasks:
        writerdetails = mastersheethelper.writerdetails.get(writer)
        projects = writertasks.get(writer)
        for project in projects:
            tasks = projects.get(project)
            taskrows = sheetrowtransformer.transform_writer_sheet_rows(tasks)
            projsheetname = project.split('-')[0]
            sheetvalue = gwritersheethelper.get_writer_book_sheet(writer, projsheetname)
            sheet = sheetvalue.get('GSheet')
            newbook = sheetvalue.get('Book_Created')
            issheetcreated = sheetvalue.get('Sheet_Created')
        
            if issheetcreated:
                taskrows.insert(0, ['Date', 'Topic', 'Word Count', 'Pay', 'Status'])
                __format_header_row(sheet)
            
            if newbook is not None:
                sheet1 = newbook.worksheet('Sheet1')
                newbook.del_worksheet(sheet1)
                try:
                    newbook.share(writerdetails.email, perm_type='user', role='writer')
                except APIError:
                        error =  f"{writer}-Work Log workbook could not shared with {writerdetails.email}"
                        errors.append(error)
            
            executor.submit(write_task, taskrows, sheet)
        
            

def __format_header_row(sheet):
    fmt = gspread_formatting.CellFormat(
                    backgroundColor=gspread_formatting.Color(155, 155, 141),
                    textFormat=gspread_formatting.TextFormat(bold=True, foregroundColor=gspread_formatting.Color(0, 0, 0)),
                    horizontalAlignment='CENTER'
                    )
    gspread_formatting.format_cell_range(sheet,'1:1', fmt)
        

def __get_max_workers(projtasks, writertasks):
    return len(projtasks) * len(writertasks)

