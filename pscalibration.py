import sys

from PyQt6.QtCore import Qt, QThread
from PyQt6.QtGui import QPixmap

from PyQt6.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QLabel, QApplication, QSpacerItem, QRadioButton, QHBoxLayout, QPushButton

from CaliforniaInstruments import California
from California_InstrumentWorker import CaliforniaInstrumentWorker
from Pacific_InstrumentWorker import PacificInstrumentWorker
from PacificPowerSupply import Pacific

import instruments

USE_INSTRUMENT = True
PS_ONE = True
PS_TWO = False





class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()



        try:
            self.setWindowTitle("COMATS Power Supply Calibration")
            self.setFixedSize(1280, 635)

            self.welcome = QWidget()
            self.setCentralWidget(self.welcome)

            self.welcomeLayout = QVBoxLayout()

            self.california = None
            self.pacific = None

            logoimage = "InAir"
            self.Logo = QPixmap(f"Images\\InAir.png")
            self.logoLabel = QLabel(self)
            self.logoLabel.setPixmap(self.Logo)
            self.logoLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
            self.logoLabel.setContentsMargins(100, 0, 100, 40)
            self.welcomeLayout.addWidget(self.logoLabel)



            self.welcomeLabel = QLabel("InAir COMATs Power Supply Calibration")
            self.welcomeLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
            self.welcomeLabel.setContentsMargins(100, 0, 100, 40)
            self.welcomeLayout.addWidget(self.welcomeLabel)
            self.welcomeLayout.setAlignment(Qt.AlignmentFlag.AlignCenter)

            spacer1 = QSpacerItem(0, 30)
            self.welcomeLayout.addSpacerItem(spacer1)

            self.bodyPrompt = QVBoxLayout()

            self.bodyLayout = QHBoxLayout()

            self.bodyButtons = QVBoxLayout()

            self.PSselectionPrompt = QLabel("Please select the corresponding power supply "
                                           "unit associated with the test bench from the following options: ")
            self.PSselectionPrompt.setAlignment(Qt.AlignmentFlag.AlignCenter)
            self.PSselectionPrompt.setContentsMargins(100, 0, 100, 40)
            self.bodyPrompt.addWidget(self.PSselectionPrompt)
            self.bodyPrompt.setAlignment(Qt.AlignmentFlag.AlignCenter)

            self.welcomeLayout.addLayout(self.bodyPrompt)

            spacer2 = QSpacerItem(0, 10)
            self.welcomeLayout.addSpacerItem(spacer2)


            self.PSselectionLabel = QLabel("Power Supply")
            self.PSselectionLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
            #self.PSselectionLabel.setContentsMargins(100, 0, 100, 40)
            self.bodyLayout.addWidget(self.PSselectionLabel)

            self.PSone = QRadioButton("California Instruments LX3000")
            self.PSone.setChecked(True)
            self.bodyButtons.addWidget(self.PSone)

            self.PStwo = QRadioButton("Pacific Power Supply model #")
            self.PStwo.setChecked(False)
            self.bodyButtons.addWidget(self.PStwo)

            self.bodyLayout.addLayout(self.bodyButtons)
            self.welcomeLayout.addLayout(self.bodyLayout)

            spacer3 = QSpacerItem(0, 60)
            self.welcomeLayout.addSpacerItem(spacer3)

            self.confirmbutton = QPushButton("Begin")
            self.confirmbutton.setFixedWidth(200)
            self.confirmbutton.setFixedHeight(200)
            self.confirmbutton.setStyleSheet(""
                                             "background-color: rgb(0, 200, 50);"
                                             "color: rgb(255, 255, 255);")
            self.confirmbutton.clicked.connect(self.confirmButtonClicked)
            self.welcomeLayout.addWidget(self.confirmbutton, alignment=Qt.AlignmentFlag.AlignCenter)

            spacer4 = QSpacerItem(0, 60)
            self.welcomeLayout.addSpacerItem(spacer4)

            self.welcome.setLayout(self.welcomeLayout)

            if USE_INSTRUMENT and self.PSone.isChecked():
                self.inst_thread = QThread(self)
                self.inst_worker = CaliforniaInstrumentWorker("GPIB0::1::INSTR", poll_ms=200)
                self.inst_worker.moveToThread(self.inst_thread)

                # lifecycle
                self.inst_thread.started.connect(
                    lambda: print("THREAD STARTED", flush=True))

                self.inst_thread.started.connect(
                    self.inst_worker.start
                )
                self.inst_worker.finished.connect(self.inst_thread.quit)
                self.inst_worker.finished.connect(self.inst_worker.deleteLater)
                self.inst_thread.finished.connect(self.inst_thread.deleteLater)
                self.inst_worker.status.connect(
                    lambda msg: print(f"Worker: {msg}", flush=True)
                )
                self.inst_worker.status.connect(print)
                self.inst_thread.start()

                # when app quits, close instrument
                QApplication.instance().aboutToQuit.connect(self.inst_worker.shutdown)

            if USE_INSTRUMENT and self.isChecked():
                self.inst_thread = QThread(self)
                self.inst_worker = PacificInstrumentWorker("GPIB0::3::INSTR", poll_ms=200)
                self.inst_worker.moveToThread(self.inst_thread)

                # lifecycle
                self.inst_thread.started.connect(self.inst_worker.start)
                self.inst_worker.finished.connect(self.inst_thread.quit)
                self.inst_worker.finished.connect(self.inst_worker.deleteLater)
                self.inst_thread.finished.connect(self.inst_thread.deleteLater)
                self.inst_thread.start()

                # when app quits, close instrument
                QApplication.instance().aboutToQuit.connect(self.inst_worker.shutdown)

            else:
                self.inst_thread = None
                self.inst_worker = None

        except Exception as e:
            print(f"Error: {e}")

    def confirmButtonClicked(self):
        try:

            if self.PSone.isChecked():
                print("You picked this one.")
                PS_ONE = True
                instruments.USE_INSTRUMENT2 = True
                instruments.USE_INSTRUMENT3 = True
                print("ACTIVE WORKER:", type(self.inst_worker).__name__, flush=True)
                self.california = California(instrument_worker=self.inst_worker)
                self.california.show()
            if self.PStwo.isChecked():
                print("You picked thatta one.")
                PS_TWO = True
                instruments.USE_INSTRUMENT2 = True
                instruments.USE_INSTRUMENT3 = True
                self.pacific = Pacific(instrument_worker=self.inst_worker)
                self.pacific.show()

        except Exception as e:
            print(f"Error: {e}")



if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())

