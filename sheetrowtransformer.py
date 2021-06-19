from taskdata import TaskData
from typing import List
def __transform_main_sheet_row (task : TaskData):
    return [str(task.date), str(task.topic), str(task.wordcount), str(task.writer), str(task.clientPay), str(task.writerPay), str(task.income)]

def __transform_writer_sheet_row (task : TaskData):
    return [str(task.date), str(task.topic), str(task.wordcount), str(task.writerPay)]

def transform_master_sheet_rows (tasks : List[TaskData]):
    taskrows = []
    for task in tasks:
        taskrow = __transform_main_sheet_row(task)
        taskrows.append(taskrow)
    return taskrows

def transform_writer_sheet_rows (tasks : List[TaskData]):
    taskrows = []
    for task in tasks:
        taskrow = __transform_writer_sheet_row(task)
        taskrows.append(taskrow)
    return taskrows
    