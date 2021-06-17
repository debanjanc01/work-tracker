from taskdata import TaskData

def transform_main_sheet_row (task : TaskData):
    return [str(task.date), str(task.topic), str(task.wordcount), str(task.writer), str(task.clientPay), str(task.writerPay), str(task.income)]

def transform_writer_sheet_row (task : TaskData):
    return [str(task.date), str(task.topic), str(task.wordcount), str(task.writerPay)]
    