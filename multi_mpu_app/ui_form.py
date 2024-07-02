from PyQt5.QtWidgets import QWidget, QPushButton, QLabel, QLineEdit, QComboBox, QTextEdit, QFrame
from PyQt5.QtCore import Qt
import pyqtgraph as pg

class UIForm(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        # Create widget
        self.mpu1_graph = pg.PlotWidget(self)  # MPU 1
        self.mpu1_graph.setGeometry(975, 50, 900, 375)
        self.mpu1_graph.setBackground('w')
        self.mpu2_graph = pg.PlotWidget(self)  # MPU 2
        self.mpu2_graph.setGeometry(50, 500, 900, 375)
        self.mpu2_graph.setBackground('w')
        self.mpu3_graph = pg.PlotWidget(self)  # MPU 3
        self.mpu3_graph.setGeometry(975, 500, 900, 375)
        self.mpu3_graph.setBackground('w')

        self.mpu1_label = QLabel('MPU 1', self)
        self.mpu1_label.setGeometry(1420, 300, 300, 300)
        self.mpu1_text = QLineEdit(self)
        self.mpu1_text.setGeometry(1485, 435, 180, 30)
        self.mpu2_label = QLabel('MPU 2', self)
        self.mpu2_label.setGeometry(450, 750, 300, 300)
        self.mpu2_text = QLineEdit(self)
        self.mpu2_text.setGeometry(515, 885, 180, 30)
        self.mpu3_label = QLabel('MPU 3', self)
        self.mpu3_label.setGeometry(1420, 750, 300, 300)
        self.mpu3_text = QLineEdit(self)
        self.mpu3_text.setGeometry(1485, 885, 180, 30)
        
        # Graph note
        self.note_frame = QLabel('Red line: X angle\nGreen lime: Y angle\nBlue line: Z graph',self)  #Frame for note
        self.note_frame.setGeometry(760, 340, 180, 100)

        # UDP widget
        self.udp_start_button = QPushButton('Start', self)
        self.udp_start_button.setGeometry(580, 100, 150, 30)
        self.udp_stop_button = QPushButton('Stop', self)
        self.udp_stop_button.setGeometry(740, 100, 150, 30)

        # Display received data
        self.textEdit = QTextEdit(self)
        self.textEdit.setGeometry(50, 100, 480, 300)
        
        self.load_csvdata = QPushButton('Load CSV', self)
        self.load_csvdata.setGeometry(580, 140, 150, 30)
        
        #Clear the graph
        self.clear_button = QPushButton('Clear', self)
        self.clear_button.setGeometry(740, 140, 150, 30)

        # Save data to CSV
        self.save_button = QPushButton('Save', self)
        self.save_button.setGeometry(775, 220, 110, 30)
        self.csv_name = QLineEdit(self)
        self.csv_name.setGeometry(580, 220, 180, 30)
        self.csv_label = QLabel('Enter file name:', self)
        self.csv_label.setGeometry(580, 180, 220, 50)
        self.status_label = QLabel(self)
        self.status_label.setGeometry(580, 260, 300, 30)

        

        
        