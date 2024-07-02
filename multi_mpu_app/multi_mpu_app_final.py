import sys
import socket
import time
import csv
import os
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QPushButton, QFileDialog, QLabel, QTextEdit, QLineEdit, QWidget
from PyQt5.QtGui import QPixmap, QImage
from PyQt5.QtCore import Qt, QThread, pyqtSignal, QTimer
from pyqtgraph import PlotWidget
from matplotlib.figure import Figure
import pyqtgraph as pg
from ui_form import UIForm

class UDPServer(QThread):
    data_received = pyqtSignal(str)
    data_to_save = pd.DataFrame()

    def __init__(self):
        super().__init__()
        self.server_socket = None
        self.running = False

    def start_server(self):
        self.data_to_save = pd.DataFrame()
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.server_socket.bind(("0.0.0.0", 1234))
        self.running = True

    def stop_server(self):
        self.running = False
        if self.server_socket:
            self.server_socket.close()

    def write_data_to_csv(self, timestamp, data, file_name):
        with open(file_name, mode='a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([timestamp, data])

    def run(self):
        self.start_server()
        #data_to_save = pd.DataFrame()
        initial_time = time.time()
        list_dir = os.listdir(os.getcwd())
        file_name = 'ui_test.csv'
        if file_name in list_dir:
            os.remove(file_name)
        while self.running:
            data, _ = self.server_socket.recvfrom(1024)
            message = data.decode('utf-8')
            timestamp = time.time() - initial_time
            self.data_received.emit(f"{timestamp}:{message}")
            # time.sleep(0.1)  # Adjust sleep time as needed to reduce CPU usage
            # self.write_data_to_csv(timestamp, message, file_name)  # Write data to CSV
            #joint_data = list([timestamp]) + list([message])
            #data_to_save = pd.concat([data_to_save,pd.Series(joint_data)], axis = 1)
            joint_data = [timestamp] + message.split(';')
            self.data_to_save = pd.concat([self.data_to_save, pd.DataFrame(joint_data).T], axis=0, ignore_index=True)
            #if timestamp > 5:
             #   self.data_to_save = data_to_save.T
              #  break

class AppMPU(QMainWindow):
    def __init__(self):
        super().__init__()
        # Create and set up the UI form
        self.ui_form = UIForm()
        self.setCentralWidget(self.ui_form)
        self.setWindowTitle('MPU App')

        #self.init_ui()

        # Widgets for graphs
        self.mpu1_graph = self.ui_form.mpu1_graph
        self.mpu2_graph = self.ui_form.mpu2_graph
        self.mpu3_graph = self.ui_form.mpu3_graph
        self.mpu1_text = self.ui_form.mpu1_text
        self.mpu2_text = self.ui_form.mpu2_text
        self.mpu3_text = self.ui_form.mpu3_text
    
        # Start and Stop button
        self.udp_start_button = self.ui_form.udp_start_button
        self.udp_start_button.clicked.connect(self.start_server)
        self.udp_stop_button = self.ui_form.udp_stop_button
        self.udp_stop_button.clicked.connect(self.stop_server)

        self.udp_server = UDPServer()
        
        #Clear graph
        self.clear_button = self.ui_form.clear_button
        self.clear_button.clicked.connect(self.clear_graph_text)
        
        # Save data to csv
        self.csv_name = self.ui_form.csv_name
        self.status_label = self.ui_form.status_label
        
        self.save_button = self.ui_form.save_button
        self.save_button.clicked.connect(self.save_to_csv)
        
        # Display data in text and plot data
        self.udp_server.data_received.connect(self.update_data_plots)
        self.textEdit = self.ui_form.textEdit
        self.textEdit.setReadOnly(True)
        
        self.x1_curve = self.mpu1_graph.plot(pen='r')
        self.y1_curve = self.mpu1_graph.plot(pen='g')
        self.z1_curve = self.mpu1_graph.plot(pen='b')
        
        self.x2_curve = self.mpu2_graph.plot(pen='r')
        self.y2_curve = self.mpu2_graph.plot(pen='g')
        self.z2_curve = self.mpu2_graph.plot(pen='b')
        
        self.x3_curve = self.mpu3_graph.plot(pen='r')
        self.y3_curve = self.mpu3_graph.plot(pen='g')
        self.z3_curve = self.mpu3_graph.plot(pen='b')
        
        # Save data to csv
        self.csv_name = self.ui_form.csv_name
        self.status_label = self.ui_form.status_label
        
        self.save_button = self.ui_form.save_button
        self.save_button.clicked.connect(self.save_to_csv)
        
        # Load data from csv file and plot
        self.load_csvdata = self.ui_form.load_csvdata
        self.load_csvdata.clicked.connect(self.load_csv)
        
        # Initialize data lists
        self.t_data = []
        self.x1_data = []
        self.y1_data = []
        self.z1_data = []
        
        self.x2_data = []
        self.y2_data = []
        self.z2_data = []
        
        self.x3_data = []
        self.y3_data = []
        self.z3_data = []
        
    def clear_graph_text(self):
        self.udp_server.data_to_save = pd.DataFrame()
        self.textEdit.clear()
        self.clear_graph()
    
    def clear_graph(self):
        # Clear data lists
        self.t_data = []
        self.x1_data = []
        self.y1_data = []
        self.z1_data = []
        self.x2_data = []
        self.y2_data = []
        self.z2_data = []
        self.x3_data = []
        self.y3_data = []
        self.z3_data = []

        # Clear plot data
        self.x1_curve.setData([], [])
        self.y1_curve.setData([], [])
        self.z1_curve.setData([], [])
        self.x2_curve.setData([], [])
        self.y2_curve.setData([], [])
        self.z2_curve.setData([], [])
        self.x3_curve.setData([], [])
        self.y3_curve.setData([], [])
        self.z3_curve.setData([], [])
      
    def start_server(self):
        self.clear_graph_text()
        self.udp_start_button.setEnabled(False)
        self.udp_stop_button.setEnabled(True)
        self.udp_server.start()

    def stop_server(self):
        self.udp_start_button.setEnabled(True)
        self.udp_stop_button.setEnabled(False)
        self.udp_server.stop_server()
        
    def update_text_edit(self, message):
        self.textEdit.append(message)  
        
    def update_data_plots(self, message):
        self.textEdit.append(message)
        try:
            print("Received message:", message)
            parts = message.split(':')
            timestamp = float(parts[0])
            data = parts[1].split(';')
            if all(d.strip() for d in data):
                x1, y1, z1, x2, y2, z2, x3, y3, z3 = map(float, data)
                print("Timestamp:", timestamp)
                print("X1:", x1, "Y1:", y1, "Z1:", z1, "X2:", x2, "Y2:", y2, "Z2:", z2, "X3:", x3, "Y3:", y3, "Z3:", z3)
            # Append data to existing lists
                self.t_data.append(timestamp)
                self.x1_data.append(x1)
                self.y1_data.append(y1)
                self.z1_data.append(z1)
                self.x2_data.append(x2)
                self.y2_data.append(y2)
                self.z2_data.append(z2)
                self.x3_data.append(x3)
                self.y3_data.append(y3)
                self.z3_data.append(z3)
        
            # Update plots
                self.x1_curve.setData(self.t_data, self.x1_data)
                self.y1_curve.setData(self.t_data, self.y1_data)
                self.z1_curve.setData(self.t_data, self.z1_data)
                
                self.x2_curve.setData(self.t_data, self.x2_data)
                self.y2_curve.setData(self.t_data, self.y2_data)
                self.z2_curve.setData(self.t_data, self.z2_data)
                
                self.x3_curve.setData(self.t_data, self.x3_data)
                self.y3_curve.setData(self.t_data, self.y3_data)
                self.z3_curve.setData(self.t_data, self.z3_data)
            
            #self.x_curve.setData(self.t_data[-100:], self.x_data[-100:], clear = True)
            #self.y_curve.setData(self.t_data[-100:], self.y_data[-100:], clear = True)
            #self.z_curve.setData(self.t_data[-100:], self.z_data[-100:], clear = True)
            else:
                print("Invalid data received:", data)
        except Exception as e:
            print(f"Error updating plots: {e}")
            self.status_label.setText(f"Error updating plots")                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                           
        
    def save_to_csv(self):
        filename = self.csv_name.text()
        c1 = self.mpu1_text.text() + " X"
        c2 = self.mpu1_text.text() + " Y"
        c3 = self.mpu1_text.text() + " Z"
        c4 = self.mpu2_text.text() + " X"
        c5 = self.mpu2_text.text() + " Y"
        c6 = self.mpu2_text.text() + " Z"
        c7 = self.mpu3_text.text() + " X"
        c8 = self.mpu3_text.text() + " Y"
        c9 = self.mpu3_text.text() + " Z"
        column_labels = ["Timestamp", c1, c2, c3, c4, c5, c6, c7, c8, c9]
        if not filename:
            self.status_label.setText("Status: Please enter a valid filename.")
            return
        try:
            self.udp_server.data_to_save.columns = column_labels
            print(self.udp_server.data_to_save)
            self.udp_server.data_to_save.to_csv(f"{filename}.csv", index=None, header=True)
            self.status_label.setText(f"Saved to {filename}.csv!")
        except Exception as e:
            self.status_label.setText(f"Status: Error saving data to CSV file")
            print(f"Status: Error saving data to CSV file: {e}")
            
    def display_graph(self):
        self.t_data = self.data.iloc[:, 0].astype(float)
        #mpu_data = self.data.iloc[:, 1].astype(str)
        #self.x_data, self.y_data, self.z_data = zip(*mpu_data.str.split(';').apply(lambda x: [float(i) for i in x]))
        self.x1_data = self.data.iloc[:, 1].astype(float)
        self.y1_data = self.data.iloc[:, 2].astype(float)
        self.z1_data = self.data.iloc[:, 3].astype(float)
        
        self.x2_data = self.data.iloc[:, 4].astype(float)
        self.y2_data = self.data.iloc[:, 5].astype(float)
        self.z2_data = self.data.iloc[:, 6].astype(float)
        
        self.x3_data = self.data.iloc[:, 7].astype(float)
        self.y3_data = self.data.iloc[:, 8].astype(float)
        self.z3_data = self.data.iloc[:, 9].astype(float)
        
        self.x1_curve.setData(self.t_data, self.x1_data, clear=True)
        self.y1_curve.setData(self.t_data, self.y1_data, clear=True)
        self.z1_curve.setData(self.t_data, self.z1_data, clear=True)
        
        self.x2_curve.setData(self.t_data, self.x2_data, clear=True)
        self.y2_curve.setData(self.t_data, self.y2_data, clear=True)
        self.z2_curve.setData(self.t_data, self.z2_data, clear=True)
        
        self.x3_curve.setData(self.t_data, self.x3_data, clear=True)
        self.y3_curve.setData(self.t_data, self.y3_data, clear=True)
        self.z3_curve.setData(self.t_data, self.z3_data, clear=True)
                
    def load_csv(self):
        self.clear_graph()
        options = QFileDialog.Options()
        options |= QFileDialog.ReadOnly
        filePath, _ = QFileDialog.getOpenFileName(self, "Open CSV File", "", "CSV Files (*.csv);;All Files (*)",
                                                  options=options)
        if filePath:
            try:
                with open(filePath, newline='') as csvfile:
                    self.data = pd.read_csv(csvfile)
                    self.display_graph()  # Automatically display the graph when data is loaded
                    self.status_label.setText("Loaded data from CSV!")
            except Exception as e:
                print(f"Error reading CSV file: {e}")
            


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = AppMPU()
    window.setWindowTitle("Motion recording app")
    window.showMaximized()
    sys.exit(app.exec_())

