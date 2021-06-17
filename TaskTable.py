from PyQt5 import QtCore
from PyQt5.QtWidgets import QTableWidget, QTableWidgetItem, QHeaderView
from taskdata import TaskData


class TaskTableWidget(QTableWidget):
    def __init__(self):
        super().__init__(0,8)
        self.setHorizontalHeaderLabels(['Date','Project','Topic','Word Count','Writer','Client Pay','Writer Pay','Income'])
        self.verticalHeader().setDefaultSectionSize(1)
        self.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)
        self.horizontalHeader().setDefaultSectionSize(QHeaderView.ResizeToContents)
        self.horizontalHeader().setSectionResizeMode(2, QHeaderView.Stretch)

        self.verticalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)
        self.setColumnWidth(2,300)
        self.resizeRowsToContents()


    def addRow(self, rowdata : TaskData):
        rowcount  = self.rowCount()
        self.insertRow(rowcount)
        self.setItem(rowcount, 0, QTableWidgetItem(rowdata.date))
        self.setItem(rowcount, 1, QTableWidgetItem(rowdata.project))
        self.setItem(rowcount, 2, QTableWidgetItem(rowdata.topic))
        self.setItem(rowcount, 3, QTableWidgetItem(rowdata.wordcount))
        self.setItem(rowcount, 4, QTableWidgetItem(rowdata.writer))
        self.setItem(rowcount, 5, QTableWidgetItem(rowdata.clientPay))
        self.setItem(rowcount, 6, QTableWidgetItem(rowdata.writerPay))
        self.setItem(rowcount, 7, QTableWidgetItem(rowdata.income))

    def keyPressEvent(self, event):
        if event.key() == QtCore.Qt.Key_Delete:
            row = self.currentRow()
            self.removeRow(row)
        else:
            super().keyPressEvent(event)

    def retrieveData(self):
        taskItems = []
        rows = self.rowCount()
        cols = self.columnCount()
        for row in range(rows):
            #date 'Project','Topic','Writer','Client Pay','Writer Pay','Income'
            date = self.item(row, 0).text()
            project = self.item(row, 1).text()
            topic = self.item(row, 2).text()
            wc = self.item(row, 3).text()
            writer = self.item(row, 4).text()
            cp = self.item(row, 5).text()
            wp = self.item(row, 6).text()
            inc = self.item(row, 7).text()

            task = TaskData.TaskData(date, project, topic, wc, writer, cp, wp, inc)
            taskItems.append(task)

        return taskItems