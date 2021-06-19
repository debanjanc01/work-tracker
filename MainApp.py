import sys
from PyQt5.QtWidgets import QApplication, QDesktopWidget, QDockWidget, QGridLayout, QLabel, QLineEdit, QWidget, QDateEdit, QComboBox, QVBoxLayout, QPushButton, QMessageBox
from PyQt5.QtGui import QMovie
from PyQt5 import QtCore
import TaskTable
import mastersheethelper
import taskwriter as tw
import taskdata
import logging

class TaskApp(QWidget):
    def __init__(self):
        super().__init__()
        self.resize(1600, 600)

        mainLayout = QGridLayout()
        
        #date entry box
        dateEntryLayout = QVBoxLayout()
        label = QLabel("Date")
        self.dateEdit = QDateEdit(calendarPopup=True)
        self.dateEdit.setDate(QtCore.QDate.currentDate())
        self.dateEdit.setDisplayFormat('dd-MM-yyyy')
        dateEntryLayout.addWidget(label)
        dateEntryLayout.addWidget(self.dateEdit) 
        #adding date entry to layout
        mainLayout.addLayout(dateEntryLayout,0,0)
        
        #project entry
        prjEntryLayout = QVBoxLayout()
        label = QLabel("Project")
        self.project_box = QComboBox()
        prjEntryLayout.addWidget(label)
        prjEntryLayout.addWidget(self.project_box) 
        #adding project entry to layout
        mainLayout.addLayout(prjEntryLayout, 0, 1)

        #writer entry
        writerLayout = QVBoxLayout()
        label = QLabel("Writer")
        self.writer_box = QComboBox()
        writerLayout.addWidget(label)
        writerLayout.addWidget(self.writer_box) 
        #adding writer entry to layout
        mainLayout.addLayout(writerLayout, 0 , 2)

        #topic entry
        topicLayout = QVBoxLayout()
        label = QLabel("Topic")
        self.topic = QLineEdit()
        topicLayout.addWidget(label)
        topicLayout.addWidget(self.topic)
        #adding topic to main layout
        mainLayout.addLayout(topicLayout,1,0,1,2)

        #wordcount entry
        wclayout = QVBoxLayout()
        label = QLabel("Word Count")
        self.wordcount = QLineEdit()
        wclayout.addWidget(label)
        wclayout.addWidget(self.wordcount)
        #adding topic to main layout
        mainLayout.addLayout(wclayout,1,2)

        #client pay entry
        clientPayLayout = QVBoxLayout()
        label = QLabel("Client Pay")
        self.clientPay = QLineEdit()
        self.clientPay.textChanged.connect(self.calculateIncome)
        clientPayLayout.addWidget(label)
        clientPayLayout.addWidget(self.clientPay)
        #adding topic to main layout
        mainLayout.addLayout(clientPayLayout,2,0)

        #writer pay entry
        writerPayLayout = QVBoxLayout()
        label = QLabel("Writer Pay")
        self.writerPay = QLineEdit()
        self.writerPay.textChanged.connect(self.calculateIncome)
        writerPayLayout.addWidget(label)
        writerPayLayout.addWidget(self.writerPay)
        #adding topic to main layout
        mainLayout.addLayout(writerPayLayout,2,1)

        #income details
        incomeLayout = QVBoxLayout()
        label = QLabel("Income")
        self.income = QLineEdit()
        self.income.setReadOnly(True)
        incomeLayout.addWidget(label)
        incomeLayout.addWidget(self.income)
        #adding topic to main layout
        mainLayout.addLayout(incomeLayout,2,2)

        button = QPushButton('Add Task')
        button.clicked.connect(self.addTableRow)
        mainLayout.addWidget(button,3,0,2,3)

        #table display
        self.table = TaskTable.TaskTableWidget()
        mainLayout.addWidget(self.table,5,0,1,3)

        #final submit button
        submit = QPushButton('Save Task to Google Sheet')
        submit.clicked.connect(self.saveToSheets)
        mainLayout.addWidget(submit,6,0,2,3)

        
        self.setLayout(mainLayout)

        for i in range(mainLayout.rowCount()):
            mainLayout.rowStretch(i)

        for i in range(mainLayout.columnCount()):
            mainLayout.columnStretch(i)

    def addTableRow(self):
        date = self.dateEdit.date().toString('dd-MM-yyyy')
        if str(date) == '':
            QMessageBox.warning(self, 'Warning', 'Date is required!')
            return
        project = self.project_box.currentText().strip()
        if str(project) == '':
            QMessageBox.warning(self, 'Warning', 'Project is required!')
            return
        writer = self.writer_box.currentText().strip()
        if str(writer) == '':
            QMessageBox.warning(self, 'Warning', 'Writer is required!')
            return
        topic = self.topic.text().strip()
        if str(topic) == '':
            QMessageBox.warning(self, 'Warning', 'Topic is required!')
            return
        wordcount = self.wordcount.text().strip()
        clientPay = self.clientPay.text().strip()
        if str(clientPay) == '':
            QMessageBox.warning(self, 'Warning', 'Client Pay is required!')
            return
        writerPay = self.writerPay.text().strip()
        if str(writerPay) == '':
            QMessageBox.warning(self, 'Warning', 'Writer Pay is required!')
            return
        income = self.income.text().strip()
        taskData = taskdata.TaskData(date, project, topic, wordcount, writer, clientPay, writerPay, income)
        self.table.addRow(taskData)
        clearContents(self)

    def calculateIncome(self):
        clientPay = self.clientPay.text().strip()
        if clientPay != '' and not clientPay.isnumeric():
            QMessageBox.warning(self, "Warning", "Client Pay has to be a number!")
            return
        writerPay = self.writerPay.text().strip() 
        if writerPay != '' and not writerPay.isnumeric():
            QMessageBox.about(self, "Warning", "Writer Pay has to be a number!")
            return
        if clientPay.isnumeric() and writerPay.isnumeric():
            cp = int(clientPay)
            wp = int(writerPay)
            profit = cp - wp
            self.income.setText(str(profit))

        
    def saveToSheets(self):
        tasks = self.table.retrieveData()
        ret = tw.save_tasks_to_sheets(tasks)
        if ret is not None:
            QMessageBox.warning(self, 'Warning', ret)
        else:
            QMessageBox.information(self, 'Information', 'Tasks have been saved to Google Sheets!')
        self.table.clearContents()
        self.table.setRowCount(0)

def setDropDownValues(taskApp : TaskApp):
    writers = mastersheethelper.writerdetails
    for writername in writers:
        taskApp.writer_box.addItem(writername)

    projects = mastersheethelper.get_projects()
    for project in projects:
        id = project['Project ID']
        name = project['Project Name']
        val = id + '-' + name
        taskApp.project_box.addItem(val)

def clearContents(taskApp : TaskApp):
    taskApp.dateEdit.setDate(QtCore.QDate.currentDate())
    taskApp.project_box.setCurrentIndex(0)
    taskApp.writer_box.setCurrentIndex(0)
    taskApp.topic.setText('')
    taskApp.wordcount.setText('')
    taskApp.clientPay.setText('')
    taskApp.writerPay.setText('')
    taskApp.income.setText('')

if __name__ == '__main__':
    try:
        logging.basicConfig(filename='myapp.log', level=logging.INFO, format='%(asctime)s - [%(filename)s:%(lineno)d] - %(levelname)s - %(message)s')
        logging.info('App started')
        app = QApplication(sys.argv)
        taskapp = TaskApp()
        setDropDownValues(taskapp)
        taskapp.show()
        app.exit(app.exec_())
    except Exception as Argument:
        logging.exception('Something wicked happened!')