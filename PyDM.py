# PyQt5 Libraries
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.uic import loadUiType

# Python3 Libraries
from os import path
from sys import argv
from urllib import request


FORM_CLASS,_ = loadUiType(path.join(path.dirname(__name__), "main.ui"))

class mainApp(QMainWindow, FORM_CLASS):
    def __init__(self, parent=None):
        super(mainApp, self).__init__(parent)
        QMainWindow.__init__(self)
        self.setupUi(self)
        # CENTER SCREEN
        qtRectangle = self.frameGeometry()
        centerPoint = QDesktopWidget().availableGeometry().center()
        qtRectangle.moveCenter(centerPoint)
        self.move(qtRectangle.topLeft())
        # WINDOW TITLE
        self.setWindowTitle('pyDM')
        self.Handle_ui()
        self.Handle_buttons()

    def Handle_ui(self):
        self.setFixedSize(614, 235)

    def Handle_buttons(self):
        self.btnDownload.clicked.connect(self.Download)
        self.btnBrowse.clicked.connect(self.Handle_browse)

    def Handle_browse(self):
        save_as = QFileDialog.getSaveFileName(self, caption="Save As", directory=".", filter="All Files(*.*)")
        self.txtSaveLocation.setText(save_as[0])

    def size_format(b):
        if b < 1000:
            return '%i' % b + 'B'
        elif 1000 <= b < 1000000:
            return '%.1f' % float(b / 1000) + 'KB'
        elif 1000000 <= b < 1000000000:
            return '%.1f' % float(b / 1000000) + 'MB'
        elif 1000000000 <= b < 1000000000000:
            return '%.1f' % float(b / 1000000000) + 'GB'
        elif 1000000000000 <= b:
            return '%.1f' % float(b / 1000000000000) + 'TB'

    def Handle_progress(self, blocknum, blocksize, totalsize):
        read = blocknum * blocksize

        if read > 0:
            # SIZING
            b = totalsize
            c = read
            if b < 1000:
                T_size = '%i' % b + 'B'
            elif 1000 <= b < 1000000:
                T_size = '%.1f' % float(b / 1000) + 'KB'
            elif 1000000 <= b < 1000000000:
                T_size = '%.1f' % float(b / 1000000) + 'MB'
            elif 1000000000 <= b < 1000000000000:
                T_size = '%.1f' % float(b / 1000000000) + 'GB'
            elif 1000000000000 <= b:
                T_size = '%.1f' % float(b / 1000000000000) + 'TB'

            if c < 1000:
                C_size = '%i' % c + 'B'
            elif 1000 <= c < 1000000:
                C_size = '%.1f' % float(c / 1000) + 'KB'
            elif 1000000 <= c < 1000000000:
                C_size = '%.1f' % float(c / 1000000) + 'MB'
            elif 1000000000 <= c < 1000000000000:
                C_size = '%.1f' % float(c / 1000000000) + 'GB'
            elif 1000000000000 <= c:
                C_size = '%.1f' % float(c / 1000000000000) + 'TB'

            self.lblSize.setText(str(T_size))
            self.lblDownloaded.setText(str(C_size))
            percent = (read * 100) / totalsize
            self.progressBar.setValue(percent)
            QApplication.processEvents()

    def Download(self):
        link = self.txtLink.text()
        saveLocation = self.txtSaveLocation.text()

        self.txtLink.setEnabled(False)
        self.txtSaveLocation.setEnabled(False)
        self.btnBrowse.setEnabled(False)
        self.btnDownload.setEnabled(False)

        try:
            request.urlretrieve(link, saveLocation, self.Handle_progress)
        except Exception:
            QMessageBox.warning(self, "Downloading Error", "Error while downloading")
            self.txtLink.setText('')
            self.txtSaveLocation.setText('')
            self.progressBar.setValue(0)

            self.txtLink.setEnabled(True)
            self.txtSaveLocation.setEnabled(True)
            self.btnBrowse.setEnabled(True)
            self.btnDownload.setEnabled(True)
            return

        
        QMessageBox.information(self, "File Downloaded", "File Downloaded Successfully")

        self.txtLink.setText('')
        self.txtSaveLocation.setText('')
        self.progressBar.setValue(0)

        self.txtLink.setEnabled(True)
        self.txtSaveLocation.setEnabled(True)
        self.btnBrowse.setEnabled(True)
        self.btnDownload.setEnabled(True)

def main():
    app = QApplication(argv)
    window = mainApp()
    window.show()
    app.exec_()

if __name__ == '__main__':
    main()