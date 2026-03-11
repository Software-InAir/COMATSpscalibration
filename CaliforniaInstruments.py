import sys

import PyQt6
import pyvisa
from PyQt6.QtCore import pyqtSignal, Qt, QObject, pyqtSlot
from PyQt6.QtWidgets import QMainWindow, QLabel, QWidget, QVBoxLayout, QApplication, QPushButton, QHBoxLayout, \
    QSpacerItem, QLineEdit

from California_InstrumentWorker import CaliforniaInstrumentWorker

USE_INSTRUMENT = False

if USE_INSTRUMENT:
    rm = pyvisa.ResourceManager()

    my_instrument = rm.open_resource('GPIB0::1::INSTR')
    my_instrument.write('INST:COUP NONE')

    #################################### Initialize Phase A ####################
    my_instrument.write('INST:NSEL 1')
    my_instrument.write('SOUR:VOLT 115')
    my_instrument.write('SOUR:CURR 7')

    #################################### Initialize Phase B ####################
    my_instrument.write('INST:NSEL 2')
    my_instrument.write('SOUR:VOLT 115')
    my_instrument.write('SOUR:CURR 7')

    #################################### Initialize Phase C ####################
    my_instrument.write('INST:NSEL 3')
    my_instrument.write('SOUR:VOLT 115')
    my_instrument.write('SOUR:CURR 7')

    ################################### Initialize Frequency ##################
    my_instrument.write('SOUR:FREQ 400')

    my_instrument.write('OUTP ON')


class Worker(QObject):
    finished = pyqtSignal()
    ch1 = pyqtSignal(float)
    ch2 = pyqtSignal(float)
    ch3 = pyqtSignal(float)
    status = pyqtSignal(str)

class California(QMainWindow):


    def __init__(self, instrument_worker: CaliforniaInstrumentWorker):
        super().__init__()



        self.instrument = instrument_worker
        self.setWindowTitle("California Instruments")
        self.setFixedSize(1280, 635)


        self.california = QWidget()
        self.setCentralWidget(self.california)

        self.californiaLayout = QVBoxLayout()

        self.californiaLayout.addStretch(1)

        # self.calibrationLayout.setSpacing(0)
        self.readingLayout = QHBoxLayout()
        self.bodyLayout = QHBoxLayout()
        self.leftLayout = QVBoxLayout()
        self.middleLayout = QVBoxLayout()
        self.rightLayout = QVBoxLayout()



        self.label = QLabel("California Instruments LS3000")
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.californiaLayout.addWidget(self.label)

        headerspacer = QSpacerItem(0, 60)
        self.californiaLayout.addSpacerItem(headerspacer)

        ############################ BEGIN READING ###############################

        ########################### CURRENT READING ###############################

        self.californiaLayout.addLayout(self.readingLayout)

        self.leftReadingLayout = QVBoxLayout()
        self.rightReadingLayout = QVBoxLayout()
        self.readingLayout.addStretch(1)
        self.readingLayout.addLayout(self.leftReadingLayout)
        readingspacer = QSpacerItem(100, 0)
        self.readingLayout.addSpacerItem(readingspacer)
        self.readingLayout.addLayout(self.rightReadingLayout)
        self.readingLayout.addStretch(1)

        self.currentReadingLabel = QLabel("Current Readings")
        self.currentReadingLabel.setStyleSheet("QLabel { font-size: 18px; }")
        self.currentReadingLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.leftReadingLayout.addWidget(self.currentReadingLabel)

        currentspacer = QSpacerItem(0, 30)
        self.leftReadingLayout.addSpacerItem(currentspacer)

        self.currentReadingLayout = QVBoxLayout()



        self.phaseACurrentReading = QLabel(f"Phase A Current: 0 A   ")
        self.phaseACurrentReading.setStyleSheet("QLabel { font-size: 24px; }")
        self.phaseACurrentReading.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.currentReadingLayout.addWidget(self.phaseACurrentReading)

        self.phaseBCurrentReading = QLabel(f"Phase B Current: 0 A   ")
        self.phaseBCurrentReading.setStyleSheet("QLabel { font-size: 24px; }")
        self.phaseBCurrentReading.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.currentReadingLayout.addWidget(self.phaseBCurrentReading)

        self.phaseCCurrentReading = QLabel(f"Phase C Current: 0 A   ")
        self.phaseCCurrentReading.setStyleSheet("QLabel { font-size: 24px; }")
        self.phaseCCurrentReading.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.currentReadingLayout.addWidget(self.phaseCCurrentReading)

        self.leftReadingLayout.addLayout(self.currentReadingLayout)

        self.VoltageReadingLabel = QLabel("Voltage Readings")
        self.VoltageReadingLabel.setStyleSheet("QLabel { font-size: 18px; }")
        self.VoltageReadingLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.rightReadingLayout.addWidget(self.VoltageReadingLabel)

        voltagespacer = QSpacerItem(0, 30)
        self.rightReadingLayout.addSpacerItem(voltagespacer)

        self.voltageReadingLayout = QVBoxLayout()

        self.voltageA = 0
        self.voltageB = 0
        self.voltageC = 0

        self.phaseAVoltageReading = QLabel(f"Phase A Voltage: {self.voltageA} V   ")
        self.phaseAVoltageReading.setStyleSheet("QLabel { font-size: 24px; }")
        self.phaseAVoltageReading.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.voltageReadingLayout.addWidget(self.phaseAVoltageReading)

        self.phaseBVoltageReading = QLabel(f"Phase B Voltage: {self.voltageB} V   ")
        self.phaseBVoltageReading.setStyleSheet("QLabel { font-size: 24px; }")
        self.phaseBVoltageReading.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.voltageReadingLayout.addWidget(self.phaseBVoltageReading)

        self.phaseCVoltageReading = QLabel(f"Phase C Voltage: {self.voltageC} V   ")
        self.phaseCVoltageReading.setStyleSheet("QLabel { font-size: 24px; }")
        self.phaseCVoltageReading.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.voltageReadingLayout.addWidget(self.phaseCVoltageReading)

        self.rightReadingLayout.addLayout(self.voltageReadingLayout)

        readingspacer2 = QSpacerItem(0, 70)
        self.californiaLayout.addSpacerItem(readingspacer2)


        self.californiaLayout.addLayout(self.bodyLayout)

        self.californiaLayout.addStretch(1)



        ############################ CURRENT SET ##################################

        self.bodyLayout.addStretch(1)

        self.aCurrent = 0
        self.bCurrent = 0
        self.cCurrent = 0

        self.leftLabel = QLabel("Set Phase Currents")
        self.leftLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.leftLayout.addWidget(self.leftLabel)

        self.currentLayout = QVBoxLayout()

        self.currentALayout = QHBoxLayout()

        self.phaseACurrent = QLabel(f"Phase A Current: {self.aCurrent} A")
        self.phaseACurrent.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.currentALayout.addWidget(self.phaseACurrent)

        self.setPhaseACurrentInput = QLineEdit()
        self.setPhaseACurrentInput.setPlaceholderText("...Set value for Phase A")
        self.currentALayout.addWidget(self.setPhaseACurrentInput)

        self.confirmPhaseACurrent = QPushButton("Set")
        self.confirmPhaseACurrent.setStyleSheet(""
                                         "background-color: rgb(0, 200, 50);"
                                         "color: rgb(255, 255, 255);")
        self.confirmPhaseACurrent.clicked.connect(self.PhaseACurrentSet)
        self.currentALayout.addWidget(self.confirmPhaseACurrent)

        self.currentLayout.addLayout(self.currentALayout)

        self.currentBLayout = QHBoxLayout()

        self.phaseBCurrent = QLabel(f"Phase B Current: {self.bCurrent} A")
        self.phaseBCurrent.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.currentBLayout.addWidget(self.phaseBCurrent)

        self.setPhaseBCurrentInput = QLineEdit()
        self.setPhaseBCurrentInput.setPlaceholderText("...Set value for Phase B")
        self.currentBLayout.addWidget(self.setPhaseBCurrentInput)

        self.confirmPhaseBCurrent = QPushButton("Set")
        self.confirmPhaseBCurrent.setStyleSheet(""
                                         "background-color: rgb(0, 200, 50);"
                                         "color: rgb(255, 255, 255);")
        self.confirmPhaseBCurrent.clicked.connect(self.PhaseBCurrentSet)
        self.currentBLayout.addWidget(self.confirmPhaseBCurrent)

        self.currentLayout.addLayout(self.currentBLayout)

        self.currentCLayout = QHBoxLayout()

        self.phaseCCurrent = QLabel(f"Phase C Current: {self.cCurrent} A")
        self.phaseCCurrent.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.currentCLayout.addWidget(self.phaseCCurrent)

        self.setPhaseCCurrentInput = QLineEdit()
        self.setPhaseCCurrentInput.setPlaceholderText("...Set value for Phase B")
        self.currentCLayout.addWidget(self.setPhaseCCurrentInput)

        self.confirmPhaseCCurrent = QPushButton("Set")
        self.confirmPhaseCCurrent.setStyleSheet(""
                                         "background-color: rgb(0, 200, 50);"
                                         "color: rgb(255, 255, 255);")
        self.confirmPhaseCCurrent.clicked.connect(self.PhaseCCurrentSet)
        self.currentCLayout.addWidget(self.confirmPhaseCCurrent)

        self.currentLayout.addLayout(self.currentCLayout)

        self.bodyLayout.addLayout(self.leftLayout)

        self.leftLayout.addLayout(self.currentLayout)

        ############################################### End CURRENT SET ######

        bodyspacer1 = QSpacerItem(100, 0)
        self.bodyLayout.addSpacerItem(bodyspacer1)

        ################################### VOLTAGE SET ########################

        self.aVoltage = 0
        self.bVoltage = 0
        self.cVoltage = 0

        self.middleLabel = QLabel("Set Phase Voltages")
        self.middleLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.middleLayout.addWidget(self.middleLabel)


        self.voltageLayout = QVBoxLayout()

        self.voltageALayout = QHBoxLayout()

        self.phaseAVoltage = QLabel(f"Phase A: {self.aVoltage} V")
        self.phaseAVoltage.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.voltageALayout.addWidget(self.phaseAVoltage)

        self.setPhaseAInput = QLineEdit()
        self.setPhaseAInput.setPlaceholderText("...Set value for Phase A")
        self.voltageALayout.addWidget(self.setPhaseAInput)

        self.confirmPhaseA = QPushButton("Set")
        self.confirmPhaseA.setStyleSheet(""
                                         "background-color: rgb(0, 200, 50);"
                                         "color: rgb(255, 255, 255);")
        self.confirmPhaseA.clicked.connect(self.PhaseASet)
        self.voltageALayout.addWidget(self.confirmPhaseA)

        self.voltageLayout.addLayout(self.voltageALayout)

        self.voltageBLayout = QHBoxLayout()

        self.phaseBVoltage = QLabel(f"Phase B: {self.aVoltage} V")
        self.phaseBVoltage.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.voltageBLayout.addWidget(self.phaseBVoltage)

        self.setPhaseBInput = QLineEdit()
        self.setPhaseBInput.setPlaceholderText("...Set value for Phase B")
        self.voltageBLayout.addWidget(self.setPhaseBInput)

        self.confirmPhaseB = QPushButton("Set")
        self.confirmPhaseB.setStyleSheet(""
                                         "background-color: rgb(0, 200, 50);"
                                         "color: rgb(255, 255, 255);")
        self.confirmPhaseB.clicked.connect(self.PhaseBSet)
        self.voltageBLayout.addWidget(self.confirmPhaseB)

        self.voltageLayout.addLayout(self.voltageBLayout)

        self.voltageCLayout = QHBoxLayout()

        self.phaseCVoltage = QLabel(f"Phase C: {self.aVoltage} V")
        self.phaseCVoltage.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.voltageCLayout.addWidget(self.phaseCVoltage)

        self.setPhaseCInput = QLineEdit()
        self.setPhaseCInput.setPlaceholderText("...Set value for Phase B")
        self.voltageCLayout.addWidget(self.setPhaseCInput)

        self.confirmPhaseC = QPushButton("Set")
        self.confirmPhaseC.setStyleSheet(""
                                         "background-color: rgb(0, 200, 50);"
                                         "color: rgb(255, 255, 255);")
        self.confirmPhaseC.clicked.connect(self.PhaseCSet)
        self.voltageCLayout.addWidget(self.confirmPhaseC)

        self.voltageLayout.addLayout(self.voltageCLayout)

        self.bodyLayout.addLayout(self.middleLayout)

        self.middleLayout.addLayout(self.voltageLayout)

################################################ END OF VOLTAGE SET ##################

        bodyspacer2 = QSpacerItem(100, 0)
        self.bodyLayout.addSpacerItem(bodyspacer2)

################################################ FREQUENCY SET ##############

        self.frequencyLabel = QLabel("Set Frequency")
        self.frequencyLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.rightLayout.addWidget(self.frequencyLabel)

        self.frequency = 0

        self.frequencyLayout = QHBoxLayout()

        self.currentFrequency = QLabel(f"Frequency: {self.frequency} Hz   ")
        self.frequencyLayout.addWidget(self.currentFrequency)

        self.setFrequencyInput = QLineEdit()
        self.setFrequencyInput.setPlaceholderText("...Set value for Frequency")
        self.frequencyLayout.addWidget(self.setFrequencyInput)

        self.confirmFrequency = QPushButton("Set")
        self.confirmFrequency.setStyleSheet(""
                                         "background-color: rgb(0, 200, 50);"
                                         "color: rgb(255, 255, 255);")
        self.confirmFrequency.clicked.connect(self.FrequencySet)
        self.frequencyLayout.addWidget(self.confirmFrequency)

        self.rightLayout.addLayout(self.frequencyLayout)
        self.rightLayout.addStretch(1)
        self.bodyLayout.addLayout(self.rightLayout)

        self.bodyLayout.addStretch(1)

        ############################################### END OF FREQUENCY SET ################

        self.storeVoltages = QPushButton("Store Voltages")
        self.storeVoltages.setFixedWidth(200)
        self.storeVoltages.setFixedHeight(50)
        self.storeVoltages.setStyleSheet(""
                                         "background-color: rgb(0, 150, 0);"
                                         "color: rgb(255, 255, 255);")

        self.storeVoltages.clicked.connect(self.WriteVoltages)
        self.californiaLayout.addWidget(self.storeVoltages, alignment=Qt.AlignmentFlag.AlignCenter)

        self.californiaLayout.addStretch(1)


        self.californiaLayout.addStretch(1)

        self.backButton = QPushButton("Back")
        self.backButton.setStyleSheet(""
                           "background-color: rgb(255, 0, 0);"
                           "color: rgb(255, 255, 255);"
                                      "")
        self.backButton.setFixedWidth(400)
        self.backButton.clicked.connect(self.backPressed)
        self.californiaLayout.addWidget(self.backButton, alignment=Qt.AlignmentFlag.AlignCenter)

        self.california.setLayout(self.californiaLayout)

        if self.instrument is not None:
            self.instrument.ch1.connect(self.show_current1)
            self.instrument.ch2.connect(self.show_current2)
            self.instrument.ch3.connect(self.show_current3)

    def PhaseACurrentSet(self):
        self.aCurrent = self.setPhaseACurrentInput.text()
        self.phaseACurrent.setText(f"Phase A Current: {self.aCurrent} A")
        if USE_INSTRUMENT:
            my_instrument.write('INST:NSEL 1')
            my_instrument.write(f'SOUR:CURR {self.setPhaseACurrentInput.text()}')

    def PhaseBCurrentSet(self):
        self.bCurrent = self.setPhaseBCurrentInput.text()
        self.phaseBCurrent.setText(f"Phase B Current: {self.bCurrent} A")
        if USE_INSTRUMENT:
            my_instrument.write('INST:NSEL 2')
            my_instrument.write(f'SOUR:CURR {self.setPhaseBCurrentInput.text()}')

    def PhaseCCurrentSet(self):
        self.cCurrent = self.setPhaseCCurrentInput.text()
        self.phaseCCurrent.setText(f"Phase C Current: {self.cCurrent} A")
        if USE_INSTRUMENT:
            my_instrument.write('INST:NSEL 3')
            my_instrument.write(f'SOUR:CURR {self.setPhaseCCurrentInput.text()}')


    def PhaseASet(self):
        self.aVoltage = self.setPhaseAInput.text()
        self.phaseAVoltage.setText(f"Phase A: {self.aVoltage} V   ")
        if USE_INSTRUMENT:
            my_instrument.write('INST:NSEL 1')
            my_instrument.write(f'SOUR:VOLT {self.setPhaseAInput.text()}')

    def PhaseBSet(self):
        self.bVoltage = self.setPhaseBInput.text()
        self.phaseBVoltage.setText(f"Phase B: {self.bVoltage} V   ")
        if USE_INSTRUMENT:
            my_instrument.write('INST:NSEL 2')
            my_instrument.write(f'SOUR:VOLT {self.setPhaseBInput.text()}')

    def PhaseCSet(self):
        self.cVoltage = self.setPhaseCInput.text()
        self.phaseCVoltage.setText(f"Phase C: {self.cVoltage} V   ")
        if USE_INSTRUMENT:
            my_instrument.write('INST:NSEL 3')
            my_instrument.write(f'SOUR:VOLT {self.setPhaseCInput.text()}')

    def FrequencySet(self):
        try:
            self.frequency = self.setFrequencyInput.text()
            self.currentFrequency.setText(f"Frequency: {self.frequency} Hz   ")
            if USE_INSTRUMENT:
                my_instrument.write(f'SOUR:FREQ {self.setFrequencyInput.text()}')
        except Exception as e:
            print(f"error: {e}")

    def WriteVoltages(self):
        try:
            text = f"Phase A: {self.aVoltage}\nPhase B: {self.bVoltage}\nPhase C: {self.cVoltage}"
            self.write_log("voltages.txt", text)
        except Exception as e:
            print(f"error: {e}")

    def write_log(self, filename, text):
        try:
            with open(filename, "w") as f:
                f.write(text + "\n")
        except Exception as e:
            print(f"error: {e}")

    @pyqtSlot(float)
    def show_current1(self, amps):
        self.phaseACurrentReading.setText(f"Phase A Current:{amps:.3f} A   ")

    @pyqtSlot(float)
    def show_current2(self, amps):
        self.phaseBCurrentReading.setText(f"Phase B Current:{amps:.3f} A   ")

    @pyqtSlot(float)
    def show_current3(self, amps):
        self.phaseCCurrentReading.setText(f"Phase C Current:{amps:.3f} A   ")


    def backPressed(self):
        self.hide()  # Hide this window


if __name__ == "__main__":
    from PyQt6.QtWidgets import QApplication
    app = QApplication(sys.argv)
    window = California()
    window.show()
    sys.exit(app.exec())