from PySide2 import QtWidgets,QtCore,QtGui

import sys
import runtimeTimer
import datetime
import csv
import os
import database

headers = ['Date', 'Time','Status']
path = r'runtime.csv'
file_exists = os.path.isfile(path)

def write_to_csv(paths,data):
    with open(paths, 'a+', encoding='utf-8') as output_file:
        csv_writer = csv.writer(output_file, delimiter=',',quoting=csv.QUOTE_ALL)
        if not file_exists:
            csv_writer.writerow(headers)
        csv_writer.writerow(data)

class RuntimeTimer(runtimeTimer.Ui_Timer,QtWidgets.QMainWindow):

    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.db = database.Database()
        self.timer = QtCore.QTimer()
        self.time = QtCore.QTime(0, 0, 0)

        self.min15_timer = QtCore.QTimer()
        self.min15_time = QtCore.QTime(0, 0, 0)

        self.now = datetime.datetime.now()
        self.today = self.now.strftime("%Y-%m-%d")
        self.db.setData(self.now.strftime("%Y-%m-%d %H:%M:%S"),0,'starttime')
        self.set_date()
        self.timerStart()


    def set_date(self):

        self.DateText.setText(str(self.today))

    def timerEvent(self):
        self.time = self.time.addSecs(1)
        # print(self.time.toString("hh:mm:ss"))
        self.showTime(self.time)

    def after_15min(self):
        self.min15_time = self.min15_time.addSecs(60)
        print(self.min15_time.toString("hh:mm:ss"))
        self.db.setData(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),5,'mid')

    def timerStart(self):
        self.timer.timeout.connect(self.timerEvent)
        self.timer.start(1000)
        self.min15_timer.timeout.connect(self.after_15min)
        self.min15_timer.start(300000)

    def showTime(self,time):
        text = time.toString('hh:mm:ss')
        # if (time.second() % 2) == 0:
        #     text = text[:2] + ' ' + text[3:5]+' '+text[6:]
        self.lcdNumber.display(text)

if __name__ == '__main__':

    app = QtWidgets.QApplication(sys.argv)
    app.setStyle(QtWidgets.QStyleFactory.create("Fusion"))
    qu = RuntimeTimer()
    qu.show()
    sys.exit(app.exec_())
