from PyQt6.QtCore import QDateTime, Qt, QTimer
from PyQt6.QtWidgets import (QApplication, QCheckBox, QComboBox, QDateTimeEdit,
        QDial, QDialog, QGridLayout, QGroupBox, QHBoxLayout, QLabel, QLineEdit,
        QProgressBar, QPushButton, QRadioButton, QScrollBar, QSizePolicy,
        QSlider, QSpinBox, QStyleFactory, QTableWidget, QTabWidget, QTextEdit,
        QVBoxLayout, QWidget)
import numpy as np
import random, json, subprocess, os, easygui
import sys
import json
import pandas as pd

# user interface for generating initial data
# use geojson file to get US state names
# generate initial data for each state randomly or by loading data about factors from external sources (json file)


class WidgetGallery(QDialog):
    def __init__(self, parent=None):
        super(WidgetGallery, self).__init__(parent)


        self.originalPalette = QApplication.palette()
        self.get_city_list("simulation/us_states_name.csv")
        self.range_dict = {'population': [0, 25000], 'csi': [10, 250], 'employment': [-1.5, 5]}
        self.create_data_dict()

        self.cityComboBox = QComboBox()
        self.cityComboBox.addItems(self.list_of_cities)
        self.cityLabel = QLabel("&City:")
        self.cityLabel.setBuddy(self.cityComboBox)

        self.popLabel = QLabel("Population:")
        # popLabel.setBuddy(popComboBox)
        self.popInput = QLineEdit()

        self.csiLabel = QLabel("CSI:")
        # csiLabel.setBuddy(csiComboBox)
        self.csiInput = QLineEdit()

        self.empLabel = QLabel("Employment:")
        # empLabel.setBuddy(homComboBox)
        self.empInput = QLineEdit()

        updateButton = QPushButton("Update")

        randomButton = QPushButton("Randomize")

        saveButton = QPushButton("Save")

        self.fileName = QLineEdit()

        loadButton = QPushButton("Load from JSON")

        self.cityComboBox.textActivated.connect(self.changeCity)
        updateButton.clicked.connect(self.update)
        randomButton.clicked.connect(self.randomize)
        saveButton.clicked.connect(self.save)
        loadButton.clicked.connect(self.load)

        mainLayout = QGridLayout()
        mainLayout.addWidget(self.cityLabel, 0, 0)
        mainLayout.addWidget(self.cityComboBox, 0, 1)
        mainLayout.addWidget(self.popLabel, 1, 0)
        mainLayout.addWidget(self.popInput, 1, 1)
        mainLayout.addWidget(self.csiLabel, 2, 0)
        mainLayout.addWidget(self.csiInput, 2, 1)
        mainLayout.addWidget(self.empLabel, 3, 0)
        mainLayout.addWidget(self.empInput, 3, 1)
        mainLayout.addWidget(updateButton, 4, 1)
        mainLayout.addWidget(randomButton, 4, 0)
        mainLayout.addWidget(self.fileName, 5, 0)
        mainLayout.addWidget(saveButton, 5, 1)
        mainLayout.addWidget(loadButton, 6, 0)
        mainLayout.setRowStretch(1, 1)
        mainLayout.setRowStretch(2, 1)
        mainLayout.setColumnStretch(0, 1)
        mainLayout.setColumnStretch(1, 1)
        self.setLayout(mainLayout)

        self.setWindowTitle("City Selection")


    def get_city_list(self, path):
        df = pd.read_csv(path)
        self.list_of_cities = []
        for index, row in df.iterrows():
            self.list_of_cities.append(row["state"] + ", code: " + row["code"])
    def changeCity(self, city):
        if self.data_dict[city]['population'] != 0 and self.data_dict[city]['population'] != '':
            self.popInput.setText(str(self.data_dict[city]['population']))
        if self.data_dict[city]['csi'] != 0 and self.data_dict[city]['csi'] != '':
            self.csiInput.setText(str(self.data_dict[city]['csi']))
        if self.data_dict[city]['employment'] != 0 and self.data_dict[city]['employment'] != '':
            self.empInput.setText(str(self.data_dict[city]['employment']))

    def randomize(self):
        for city in self.list_of_cities:
            if self.data_dict[city]['population'] == 0 or self.data_dict[city]['population'] == '':
                self.data_dict[city]['population'] = random.uniform(self.range_dict['population'][0], self.range_dict['population'][1])
            if self.data_dict[city]['csi'] == 0 or self.data_dict[city]['csi'] == '':
                self.data_dict[city]['csi'] = random.uniform(self.range_dict['csi'][0], self.range_dict['csi'][1])
            if self.data_dict[city]['employment'] == 0 or self.data_dict[city]['employment'] == '':
                self.data_dict[city]['employment'] = random.uniform(self.range_dict['employment'][0], self.range_dict['employment'][1])
        self.changeCity(self.cityComboBox.currentText())

    def update(self):
        city = self.cityComboBox.currentText()
        self.data_dict[city]['population'] = self.popInput.text()
        self.data_dict[city]['csi'] = self.csiInput.text()
        self.data_dict[city]['employment'] = self.empInput.text()
        print(self.data_dict)


    def create_data_dict(self):
        self.data_dict = {}
        for city in self.list_of_cities:
            self.data_dict[city] = {
                'population': 0,
                'csi': 0,
                'employment': 0
            }

    def save(self):
        fileName = self.fileName.text()
        with open(fileName + ".json", "w") as outfile:
            json.dump(self.data_dict, outfile)

    def load(self):
        path = easygui.fileopenbox()
        with open(path, 'r') as f:
            self.data_dict = json.load(f)
        print(self.data_dict)
        self.changeCity(self.cityComboBox.currentText())

        # directory = os.getcwd()
        # subprocess.Popen(f'explorer {directory}')



if __name__ == '__main__':
    app = QApplication(sys.argv)
    gallery = WidgetGallery()
    gallery.show()
    sys.exit(app.exec())