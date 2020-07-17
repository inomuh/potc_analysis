#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'potc_analysis_gui.ui'
#
# Created by: PyQt5 UI code generator 5.11.3
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets
#import rospy
import math
import pandas as pd
import os
import sys
import csv
import time
import threading
from datetime import datetime

class POTC_Analysis(object):
    """
        threshold_type:
            True = System POTC Value
            False = System Reliability Value

        load_control:
            True = Failure Rate Calculation Using Operating Load
            False = Only Failure Rate
    """
    def __init__(self):
        self.robot_column_no_dict = {"Yuk": {"Count": 21, "1": 3, "2": 26, "3": 49}, "Mesafe": {"1": 3, "2": 27, "3": 51}, "Hiz": {"1": 81, "2": 149, "3": 217}}
        self.distance_list = list()
        self.robot_main_dict = {"Yuk": dict(), "Mesafe": dict()}

        self.current_workspace = self.get_current_workspace()
        #print(self.current_workspace)

        self.main_read_func()

        self.robot_count = 3
        self.initial_configuration_dict = dict()
        self.load_control = True
        self.threshold_type = True
        self.threshold_value = 0.5
        self.route_count = 0

# ------------------------------------------------------------------------------------------------
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(950, 700)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(MainWindow.sizePolicy().hasHeightForWidth())
        MainWindow.setSizePolicy(sizePolicy)
        MainWindow.setMinimumSize(QtCore.QSize(950, 700))
        MainWindow.setMaximumSize(QtCore.QSize(950, 700))
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.groupBox_selection_analysis = QtWidgets.QGroupBox(self.centralwidget)
        self.groupBox_selection_analysis.setGeometry(QtCore.QRect(20, 20, 570, 330))
        font = QtGui.QFont()
        font.setPointSize(15)
        self.groupBox_selection_analysis.setFont(font)
        self.groupBox_selection_analysis.setObjectName("groupBox_selection_analysis")
        self.comboBox_select_threshold_type = QtWidgets.QComboBox(self.groupBox_selection_analysis)
        self.comboBox_select_threshold_type.setGeometry(QtCore.QRect(275, 150, 150, 35))
        font = QtGui.QFont()
        font.setPointSize(15)
        self.comboBox_select_threshold_type.setFont(font)
        self.comboBox_select_threshold_type.setObjectName("comboBox_select_threshold_type")
        self.label_5 = QtWidgets.QLabel(self.groupBox_selection_analysis)
        self.label_5.setGeometry(QtCore.QRect(0, 150, 250, 35))
        font = QtGui.QFont()
        font.setPointSize(15)
        self.label_5.setFont(font)
        self.label_5.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_5.setObjectName("label_5")
        self.doubleSpinBox_threshold_value = QtWidgets.QDoubleSpinBox(self.groupBox_selection_analysis)
        self.doubleSpinBox_threshold_value.setGeometry(QtCore.QRect(275, 200, 100, 35))
        self.doubleSpinBox_threshold_value.setDecimals(5)
        self.doubleSpinBox_threshold_value.setMaximum(1.0)
        self.doubleSpinBox_threshold_value.setSingleStep(0.05)
        self.doubleSpinBox_threshold_value.setProperty("value", 0.5)
        self.doubleSpinBox_threshold_value.setObjectName("doubleSpinBox_threshold_value")
        self.label_8 = QtWidgets.QLabel(self.groupBox_selection_analysis)
        self.label_8.setGeometry(QtCore.QRect(0, 200, 250, 35))
        font = QtGui.QFont()
        font.setPointSize(15)
        self.label_8.setFont(font)
        self.label_8.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_8.setObjectName("label_8")
        self.label_9 = QtWidgets.QLabel(self.groupBox_selection_analysis)
        self.label_9.setGeometry(QtCore.QRect(0, 250, 250, 35))
        font = QtGui.QFont()
        font.setPointSize(15)
        self.label_9.setFont(font)
        self.label_9.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_9.setObjectName("label_9")
        self.spinBox_route_count = QtWidgets.QSpinBox(self.groupBox_selection_analysis)
        self.spinBox_route_count.setGeometry(QtCore.QRect(275, 250, 100, 35))
        self.spinBox_route_count.setMaximum(100000)
        self.spinBox_route_count.setObjectName("spinBox_route_count")
        self.label_10 = QtWidgets.QLabel(self.groupBox_selection_analysis)
        self.label_10.setGeometry(QtCore.QRect(120, 290, 271, 41))
        font = QtGui.QFont()
        font.setPointSize(8)
        self.label_10.setFont(font)
        self.label_10.setTextFormat(QtCore.Qt.AutoText)
        self.label_10.setScaledContents(False)
        self.label_10.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_10.setWordWrap(True)
        self.label_10.setObjectName("label_10")
        self.label_3 = QtWidgets.QLabel(self.groupBox_selection_analysis)
        self.label_3.setGeometry(QtCore.QRect(0, 100, 250, 35))
        font = QtGui.QFont()
        font.setPointSize(15)
        self.label_3.setFont(font)
        self.label_3.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_3.setObjectName("label_3")
        self.comboBox_load_data = QtWidgets.QComboBox(self.groupBox_selection_analysis)
        self.comboBox_load_data.setGeometry(QtCore.QRect(275, 100, 150, 35))
        font = QtGui.QFont()
        font.setPointSize(15)
        self.comboBox_load_data.setFont(font)
        self.comboBox_load_data.setObjectName("comboBox_load_data")
        self.spinBox_robot_route_count = QtWidgets.QSpinBox(self.groupBox_selection_analysis)
        self.spinBox_robot_route_count.setGeometry(QtCore.QRect(275, 50, 100, 35))
        self.spinBox_robot_route_count.setMinimum(1)
        self.spinBox_robot_route_count.setMaximum(1000)
        self.spinBox_robot_route_count.setObjectName("spinBox_robot_route_count")
        self.pushButton_set_robot_count = QtWidgets.QPushButton(self.groupBox_selection_analysis)
        self.pushButton_set_robot_count.setGeometry(QtCore.QRect(460, 40, 100, 50))
        font = QtGui.QFont()
        font.setPointSize(15)
        self.pushButton_set_robot_count.setFont(font)
        self.pushButton_set_robot_count.setObjectName("pushButton_set_robot_count")
        self.label_11 = QtWidgets.QLabel(self.groupBox_selection_analysis)
        self.label_11.setGeometry(QtCore.QRect(0, 50, 250, 35))
        font = QtGui.QFont()
        font.setPointSize(15)
        self.label_11.setFont(font)
        self.label_11.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_11.setObjectName("label_11")
        self.plainTextEdit_result_view = QtWidgets.QPlainTextEdit(self.centralwidget)
        self.plainTextEdit_result_view.setGeometry(QtCore.QRect(620, 35, 300, 500))
        self.plainTextEdit_result_view.setReadOnly(True)
        self.plainTextEdit_result_view.setPlainText("")
        self.plainTextEdit_result_view.setObjectName("plainTextEdit_result_view")
        self.pushButton_start_analysis = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_start_analysis.setGeometry(QtCore.QRect(690, 550, 150, 75))
        font = QtGui.QFont()
        font.setPointSize(15)
        self.pushButton_start_analysis.setFont(font)
        self.pushButton_start_analysis.setObjectName("pushButton_start_analysis")
        self.groupBox_robot_configuration = QtWidgets.QGroupBox(self.centralwidget)
        self.groupBox_robot_configuration.setEnabled(False)
        self.groupBox_robot_configuration.setGeometry(QtCore.QRect(20, 400, 570, 271))
        font = QtGui.QFont()
        font.setPointSize(15)
        self.groupBox_robot_configuration.setFont(font)
        self.groupBox_robot_configuration.setObjectName("groupBox_robot_configuration")
        self.label_12 = QtWidgets.QLabel(self.groupBox_robot_configuration)
        self.label_12.setGeometry(QtCore.QRect(0, 30, 250, 35))
        font = QtGui.QFont()
        font.setPointSize(15)
        self.label_12.setFont(font)
        self.label_12.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_12.setObjectName("label_12")
        self.comboBox_select_robot = QtWidgets.QComboBox(self.groupBox_robot_configuration)
        self.comboBox_select_robot.setGeometry(QtCore.QRect(275, 30, 150, 35))
        font = QtGui.QFont()
        font.setPointSize(15)
        self.comboBox_select_robot.setFont(font)
        self.comboBox_select_robot.setObjectName("comboBox_select_robot")
        self.label_7 = QtWidgets.QLabel(self.groupBox_robot_configuration)
        self.label_7.setGeometry(QtCore.QRect(400, 230, 71, 35))
        font = QtGui.QFont()
        font.setPointSize(15)
        self.label_7.setFont(font)
        self.label_7.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.label_7.setObjectName("label_7")
        self.label_6 = QtWidgets.QLabel(self.groupBox_robot_configuration)
        self.label_6.setGeometry(QtCore.QRect(400, 180, 71, 35))
        font = QtGui.QFont()
        font.setPointSize(15)
        self.label_6.setFont(font)
        self.label_6.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.label_6.setObjectName("label_6")
        self.doubleSpinBox_nominal_capacity_value = QtWidgets.QDoubleSpinBox(self.groupBox_robot_configuration)
        self.doubleSpinBox_nominal_capacity_value.setGeometry(QtCore.QRect(275, 230, 100, 35))
        self.doubleSpinBox_nominal_capacity_value.setDecimals(1)
        self.doubleSpinBox_nominal_capacity_value.setMaximum(100000.0)
        self.doubleSpinBox_nominal_capacity_value.setSingleStep(0.5)
        self.doubleSpinBox_nominal_capacity_value.setObjectName("doubleSpinBox_nominal_capacity_value")
        self.doubleSpinBox_robot_speed_value = QtWidgets.QDoubleSpinBox(self.groupBox_robot_configuration)
        self.doubleSpinBox_robot_speed_value.setGeometry(QtCore.QRect(275, 180, 100, 35))
        self.doubleSpinBox_robot_speed_value.setDecimals(3)
        self.doubleSpinBox_robot_speed_value.setMaximum(100.0)
        self.doubleSpinBox_robot_speed_value.setObjectName("doubleSpinBox_robot_speed_value")
        self.label_4 = QtWidgets.QLabel(self.groupBox_robot_configuration)
        self.label_4.setGeometry(QtCore.QRect(0, 230, 250, 35))
        font = QtGui.QFont()
        font.setPointSize(15)
        self.label_4.setFont(font)
        self.label_4.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_4.setObjectName("label_4")
        self.lineEdit_hazard_rate_value = QtWidgets.QLineEdit(self.groupBox_robot_configuration)
        self.lineEdit_hazard_rate_value.setGeometry(QtCore.QRect(275, 80, 200, 35))
        self.lineEdit_hazard_rate_value.setObjectName("lineEdit_hazard_rate_value")
        self.label = QtWidgets.QLabel(self.groupBox_robot_configuration)
        self.label.setGeometry(QtCore.QRect(0, 80, 250, 35))
        font = QtGui.QFont()
        font.setPointSize(15)
        self.label.setFont(font)
        self.label.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(self.groupBox_robot_configuration)
        self.label_2.setGeometry(QtCore.QRect(0, 180, 250, 35))
        font = QtGui.QFont()
        font.setPointSize(15)
        self.label_2.setFont(font)
        self.label_2.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_2.setObjectName("label_2")
        self.lineEdit_start_reliability_value = QtWidgets.QLineEdit(self.groupBox_robot_configuration)
        self.lineEdit_start_reliability_value.setGeometry(QtCore.QRect(275, 130, 200, 35))
        self.lineEdit_start_reliability_value.setObjectName("lineEdit_start_reliability_value")
        self.label_13 = QtWidgets.QLabel(self.groupBox_robot_configuration)
        self.label_13.setGeometry(QtCore.QRect(0, 130, 250, 35))
        font = QtGui.QFont()
        font.setPointSize(15)
        self.label_13.setFont(font)
        self.label_13.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_13.setObjectName("label_13")
        MainWindow.setCentralWidget(self.centralwidget)

    # ---------------------------------------------------------------------------------------------------------------

        self.potc_gui_main_func()

    # ---------------------------------------------------------------------------------------------------------------

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Prognostic Aware Multi Robot Route Planning"))
        self.groupBox_selection_analysis.setTitle(_translate("MainWindow", "Analysis Options"))
        self.label_5.setText(_translate("MainWindow", "Select Threshold Type"))
        self.label_8.setText(_translate("MainWindow", "Threshold Value"))
        self.label_9.setText(_translate("MainWindow", "Route Count"))
        self.label_10.setText(_translate("MainWindow", "Note: It refers to the number of routes to be analyzed. If the value is 0, it refers to the maximum value."))
        self.label_3.setText(_translate("MainWindow", "Use Load Data"))
        self.pushButton_set_robot_count.setText(_translate("MainWindow", "Set Count"))
        self.label_11.setText(_translate("MainWindow", "Set Robot Count"))
        self.pushButton_start_analysis.setText(_translate("MainWindow", "Start Analysis"))
        self.groupBox_robot_configuration.setTitle(_translate("MainWindow", "Robot Configuration"))
        self.label_12.setText(_translate("MainWindow", "Select Robot"))
        self.label_7.setText(_translate("MainWindow", "kg"))
        self.label_6.setText(_translate("MainWindow", "km / h"))
        self.label_4.setText(_translate("MainWindow", "Nominal Capacity Value"))
        self.label.setText(_translate("MainWindow", "Hazard Rate Value"))
        self.label_2.setText(_translate("MainWindow", "Robot Speed Value"))
        self.label_13.setText(_translate("MainWindow", "Start Reliability Value"))

# ------------------------------------------------------------------------------------------------

    def potc_gui_main_func(self):
        self.gui_default_parameters_func()

        self.potc_gui_events_func()


    def gui_default_parameters_func(self):
        #self.lineEdit_hazard_rate_value.setText("5.07e-04")
        #self.doubleSpinBox_robot_speed_value.setValue(4.32)

        load_data_list = list(["True", "False"])
        self.comboBox_load_data.addItems(load_data_list)

        #self.doubleSpinBox_nominal_capacity_value.setValue(200.0)

        filter_list = list(["POTC Value", "Reliability Value"])
        self.comboBox_select_threshold_type.addItems(filter_list)

        self.doubleSpinBox_threshold_value.setValue(0.5)
        self.spinBox_route_count.setValue(0)

        self.comboBox_select_robot.addItem("None")

        self.pushButton_start_analysis.setEnabled(False)



    def potc_gui_events_func(self):
        self.pushButton_set_robot_count.clicked.connect(self.click_set_robot_count_button_func)
        self.pushButton_start_analysis.clicked.connect(self.click_start_analysis_button_func)
        self.lineEdit_hazard_rate_value.textChanged.connect(self.event_lineEdit_hazard_rate_value_func)
        self.doubleSpinBox_robot_speed_value.valueChanged.connect(self.event_doubleSpinBox_robot_speed_value_func)
        self.comboBox_load_data.currentIndexChanged.connect(self.event_comboBox_load_data_func)
        self.doubleSpinBox_nominal_capacity_value.valueChanged.connect(self.event_doubleSpinBox_nominal_capacity_value_func)
        self.comboBox_select_threshold_type.currentIndexChanged.connect(self.event_comboBox_select_threshold_type_func)
        self.doubleSpinBox_threshold_value.valueChanged.connect(self.event_doubleSpinBox_threshold_value_func)
        self.spinBox_route_count.valueChanged.connect(self.event_spinBox_route_count_func)
        self.comboBox_select_robot.currentIndexChanged.connect(self.event_comboBox_select_robot_func)
        self.lineEdit_start_reliability_value.textChanged.connect(self.event_lineEdit_start_reliability_value_func)

    def click_set_robot_count_button_func(self):
        self.robot_count = self.spinBox_robot_route_count.value()

        if self.robot_count > 3:
            self.robot_count = 3

        self.initial_configuration_dicts_func(self.robot_count)
        print(self.initial_configuration_dict)
        robot_list = list()

        for item in range(len(list(self.initial_configuration_dict.keys()))):
            robot_list.append(str("Robot " + str(item + 1)))

        self.comboBox_select_robot.addItems(robot_list)

        self.label_11.setEnabled(False)
        self.spinBox_robot_route_count.setEnabled(False)
        self.pushButton_set_robot_count.setEnabled(False)
        self.groupBox_robot_configuration.setEnabled(True)
        self.pushButton_start_analysis.setEnabled(True)


    def click_start_analysis_button_func(self):
        try:
            potc_class = CalculatePOTC(self.robot_count, self.robot_main_dict, self.initial_configuration_dict, self.distance_list, self.load_control, self.threshold_type, self.threshold_value, self.route_count)
            #potc_class.calculate_main_potc_func()

            calculate_thread = threading.Thread(target=potc_class.calculate_main_potc_func)
            calculate_thread.start()
            calculate_thread.join()

            now = datetime.now()
            dt_string = now.strftime("%Y_%m_%d_-_%H_%M_%S")

            if self.load_control:
                file_name = str("potc_analysis_loaded_" + str(dt_string))
            else:
                file_name = str("potc_analysis_unloaded_" + str(dt_string))

            self.csv_write(potc_class.write_data_list, file_name)

            print("\n\n\nDosya Yazma islemi Basari ile gerceklesti")

            set_value = potc_class.selected_route_count_list

            self.set_plain_text_edit_result_view_func(set_value)

        except Exception as err:
            print("\n\nError: click_start_analysis_button_func")
            print(err)

    
    def event_lineEdit_hazard_rate_value_func(self):
        try:
            selected_cb_robot = str(self.comboBox_select_robot.currentText())
            selected_robot = selected_cb_robot.split("Robot ")[-1]

            if selected_cb_robot != "None" and selected_cb_robot != "":
                get_value = self.lineEdit_hazard_rate_value.text()

                if get_value != "":
                    self.initial_configuration_dict[str("robot_" + str(selected_robot))]["Hazard Rate"] = float(get_value)

        except Exception as err:
            print("\n\nError: event_lineEdit_hazard_rate_value_func")
            print(err)


    def event_doubleSpinBox_robot_speed_value_func(self):
        try:
            selected_cb_robot = str(self.comboBox_select_robot.currentText())
            selected_robot = selected_cb_robot.split("Robot ")[-1]

            if selected_cb_robot != "None" and selected_cb_robot != "":
                get_value = self.doubleSpinBox_robot_speed_value.value()

                self.initial_configuration_dict[str("robot_" + str(selected_robot))]["Speed"] = float(get_value)

        except Exception as err:
            print("\n\nError: event_doubleSpinBox_robot_speed_value_func")
            print(err)


    def event_comboBox_load_data_func(self):
        try:
            get_value = str(self.comboBox_load_data.currentText())

            if get_value == "True":
                self.load_control = True

            else:
                self.load_control = False

        except Exception as err:
            print("\n\nError: comboBox_load_data")
            print(err)


    def event_doubleSpinBox_nominal_capacity_value_func(self):
        try:
            selected_cb_robot = str(self.comboBox_select_robot.currentText())
            selected_robot = selected_cb_robot.split("Robot ")[-1]

            if selected_cb_robot != "None" and selected_cb_robot != "":
                get_value = self.doubleSpinBox_nominal_capacity_value.value()

                self.initial_configuration_dict[str("robot_" + str(selected_robot))]["Nominal Capacity"] = float(get_value)

        except Exception as err:
            print("\n\nError: event_doubleSpinBox_nominal_capacity_value_func")
            print(err)


    def event_comboBox_select_threshold_type_func(self):
        try:
            get_value = str(self.comboBox_select_threshold_type.currentText())

            if get_value == "POTC Value":
                self.threshold_type = True

            elif get_value == "Reliability Value":
                self.threshold_type = False

        except Exception as err:
            print("\n\nError: event_comboBox_select_threshold_type_func")
            print(err)


    def event_doubleSpinBox_threshold_value_func(self):
        try:
            get_value = self.doubleSpinBox_threshold_value.value()

            self.threshold_value = float(get_value)

        except Exception as err:
            print("\n\nError: event_doubleSpinBox_threshold_value_func")
            print(err)


    def event_spinBox_route_count_func(self):
        try:
            get_value = self.spinBox_route_count.value()

            self.route_count = int(get_value)

        except Exception as err:
            print("\n\nError: event_spinBox_route_count_func")
            print(err)


    def event_comboBox_select_robot_func(self):
        try:
            selected_cb_robot = str(self.comboBox_select_robot.currentText())

            if selected_cb_robot != "None" and selected_cb_robot != "":
                selected_robot = selected_cb_robot.split("Robot ")[-1]
                
                self.set_enable_robot_configuration_group_func(True)
                self.lineEdit_hazard_rate_value.setText(str(self.initial_configuration_dict[str("robot_" + str(selected_robot))]["Hazard Rate"]))
                self.lineEdit_start_reliability_value.setText(str(self.initial_configuration_dict[str("robot_" + str(selected_robot))]["Reliability"]))
                self.doubleSpinBox_robot_speed_value.setValue(float(self.initial_configuration_dict[str("robot_" + str(selected_robot))]["Speed"]))
                self.doubleSpinBox_nominal_capacity_value.setValue(float(self.initial_configuration_dict[str("robot_" + str(selected_robot))]["Nominal Capacity"]))

            else:
                self.lineEdit_hazard_rate_value.setText("")
                self.lineEdit_start_reliability_value.setText("")
                self.doubleSpinBox_robot_speed_value.setValue(0.0)
                self.doubleSpinBox_nominal_capacity_value.setValue(0.0)

                self.set_enable_robot_configuration_group_func(False)



        except Exception as err:
            print("\n\nError: event_comboBox_select_robot_func")
            print(err)


    def event_lineEdit_start_reliability_value_func(self):
        try:
            selected_cb_robot = str(self.comboBox_select_robot.currentText())
            selected_robot = selected_cb_robot.split("Robot ")[-1]

            if selected_cb_robot != "None" and selected_cb_robot != "":
                get_value = self.lineEdit_start_reliability_value.text()

                if get_value != "":
                    self.initial_configuration_dict[str("robot_" + str(selected_robot))]["Reliability"] = float(get_value)

        except Exception as err:
            print("\n\nError: event_lineEdit_start_reliability_value_func")
            print(err)


    def set_plain_text_edit_result_view_func(self, set_value):
        self.plainTextEdit_result_view.clear()
        write_value = ""

        for item in set_value:
            temp = str(item[0]) + "\t-> " + str(item[1])
            write_value = write_value + "\n" + temp


        self.plainTextEdit_result_view.setPlainText(write_value)


# ------------------------------------------------------------------------------------------------

    @classmethod
    def get_current_workspace(cls):
        """
            Get Current Workspace Function
        """
        file_full_path = os.path.dirname(os.path.realpath(__file__))
        directory_name = sys.argv[0].split('/')[-2]
        workspace_name = file_full_path.split(str(directory_name))[0]

        return workspace_name


    def read_distance_file_func(self):
        df = pd.read_csv(str(self.current_workspace) + 'potc_analysis/params/distances.csv', sep=',', header=None)
        self.distance_list = df.values


    def read_route_loads_func(self, robot_no):
        with open(str(self.current_workspace) + 'potc_analysis/params/1003_routeLoads.csv', 'r') as csvfile:
            read_data = csv.reader(csvfile, delimiter=',')
            next(read_data)

            robot_load_dict = dict()
            for row in read_data:
                robot_load_list = list()

                for row_count in range(self.robot_column_no_dict["Yuk"]["Count"]):
                    robot_load_list.append(float(row[int(self.robot_column_no_dict["Yuk"][str(robot_no)] + row_count)]))

                robot_load_dict[str(row[0])] = robot_load_list

        self.robot_main_dict["Yuk"][str("robot_" + str(robot_no))] = robot_load_dict


    def read_route_func(self, robot_no):
        with open(str(self.current_workspace) + 'potc_analysis/params/1003_routeSet.csv', 'r') as csvfile:
            read_data = csv.reader(csvfile, delimiter=',')
            next(read_data)

            robot_route_dict = dict()
            for row in read_data:
                robot_route_list = list()

                for row_count in range(int(row[int(self.robot_column_no_dict["Mesafe"][str(robot_no)] - 1)])):
                    robot_route_list.append(float(row[int(self.robot_column_no_dict["Mesafe"][str(robot_no)] + row_count)]))

                robot_route_dict[str(row[0])] = robot_route_list

        self.robot_main_dict["Mesafe"][str("robot_" + str(robot_no))] = robot_route_dict


    def read_speed_func(self, robot_no):
        with open(str(self.current_workspace) + 'potc_analysis/params/1003_routeSet.csv', 'r') as csvfile:
            read_data = csv.reader(csvfile, delimiter=',')
            next(read_data)

            robot_speed_dict = dict()
            for row in read_data:
                robot_speed_list = list()

                for row_count in range(int(row[int(self.robot_column_no_dict["Mesafe"][str(robot_no)] - 1)]) - 1):
                    robot_speed_list.append(float(row[int(self.robot_column_no_dict["Hiz"][str(robot_no)] + row_count)]))

                robot_speed_dict[str(row[0])] = robot_speed_list

        self.robot_main_dict["Hiz"][str("robot_" + str(robot_no))] = robot_speed_dict


    def main_read_func(self):
        self.read_distance_file_func()

        self.read_route_loads_func(1)
        self.read_route_loads_func(2)
        self.read_route_loads_func(3)

        self.read_route_func(1)
        self.read_route_func(2)
        self.read_route_func(3)

        #self.read_speed_func(1)
        #self.read_speed_func(2)
        #self.read_speed_func(3)


    def csv_write(self, write_data_list, file_name):
        with open(str(self.current_workspace) + 'potc_analysis/params/write_data/'+ str(file_name) + '.csv','w+') as csvFile:
            writer = csv.writer(csvFile)
            writer.writerows(write_data_list)
        csvFile.close()

# -------------------------------------------------------------------

    def initial_configuration_dicts_func(self, robot_count):
        for item in range(robot_count):
            self.initial_configuration_dict[str("robot_" + str(item + 1))] = {"Hazard Rate": float(5.07e-04), "Reliability": float(1), "Nominal Capacity": float(200), "Speed": float(4.32)}


    def set_enable_robot_configuration_group_func(self, status):
        self.lineEdit_hazard_rate_value.setEnabled(status)
        self.lineEdit_start_reliability_value.setEnabled(status)
        self.doubleSpinBox_robot_speed_value.setEnabled(status)
        self.doubleSpinBox_nominal_capacity_value.setEnabled(status)
        self.label.setEnabled(status)
        self.label_13.setEnabled(status)
        self.label_2.setEnabled(status)
        self.label_4.setEnabled(status)
        self.label_6.setEnabled(status)
        self.label_7.setEnabled(status)

# -------------------------------------------------------------------

class CalculatePOTC:
    """
        km / h
    """
    def __init__(self, robot_count, robot_main_dict, initial_configuration_dict, distance_list, load_control, threshold_type, threshold_value, route_count):
        self.robot_count = robot_count
        self.initial_configuration_dict = initial_configuration_dict
        self.robot_main_dict = robot_main_dict
        self.distance_list = distance_list
        self.load_control = load_control
        self.threshold_type = threshold_type
        self.threshold_value = threshold_value

        if route_count == 0:
            self.robot_main_dict_count = len(list(self.robot_main_dict["Mesafe"][str("robot_" + str(self.robot_count))].keys()))
            self.route_count = self.robot_main_dict_count

        else:
            self.route_count = route_count

        self.write_data_list = list()
        self.selected_route_count_list = list()

        self.system_main_dict = dict()
        self.system_main_dict["0"] = {"POTC": 1, "Reliability": 1, "Secili Rota": 0, "Robot Reliability": list(), "Robot Time": list(), "Robot Distance": list()}
        self.initial_system_main_dict_func()


    @classmethod
    def failure_rate_calculation_using_operating_load_func(cls, failure_rate, p_value, p_0):
        """
            λ = λ0 * ((P + P0) / P0) ^ 3
        """
        result = float(failure_rate * pow(((float(p_value) + float(p_0)) / float(p_0)), 3))

        return result


    @classmethod
    def probability_of_task_completion_formula(cls, reliability, distance):
        potc_result = float(pow(float(reliability), float(distance)))

        return potc_result


    @classmethod
    def calculate_time_func(cls, distance, speed):
        time = float(distance / speed)

        return time


    @classmethod
    def reliability_exponential_func(cls, reliability_time, failure_rate):
        """
            Reliability Model = Exponential Distribution

            R = e ^ -(λt)
        """
        return float(math.exp(float(-1) * float(reliability_time) * float(failure_rate)))

    @classmethod
    def time_convert_function(cls, time_value):
        seconds = float(time_value)*60*60
        minutes, seconds = divmod(seconds, 60)
        hours, minutes = divmod(minutes, 60)

        result = "%02d:%02d:%02d"%(hours,minutes,seconds)
        return result


    def initial_system_main_dict_func(self):
        robot_reliability_list = list()
        robot_time_list = list()
        robot_distance_list = list()

        for item in range(self.robot_count):
            robot_reliability_list.append(self.initial_configuration_dict[str("robot_" + str(item + 1))]["Reliability"])
            robot_time_list.append(float(0.0))
            robot_distance_list.append(float(0.0))

        self.system_main_dict["0"]["Robot Reliability"] = robot_reliability_list
        self.system_main_dict["0"]["Robot Time"] = robot_time_list
        self.system_main_dict["0"]["Robot Distance"] = robot_distance_list


    def set_write_data_list_func(self):
        key_count = len(list(self.system_main_dict.keys()))

        # Headers
        temp_list = list()
        temp_list.append("Count")
        temp_list.append(str(""))
        temp_list.append("Secili Rota")
        temp_list.append(str(""))
        temp_list.append("POTC")
        temp_list.append(str(""))
        temp_list.append("Reliability")
        temp_list.append(str(""))
        temp_list.append("Robot Reliability ->")
        temp_list.append("Robot 1")
        temp_list.append("Robot 2")
        temp_list.append("Robot 3")
        temp_list.append(str(""))
        temp_list.append("Robot Zaman ->")
        temp_list.append("Robot 1")
        temp_list.append("Robot 2")
        temp_list.append("Robot 3")
        temp_list.append(str(""))
        temp_list.append("Robot Mesafe ->")
        temp_list.append("Robot 1")
        temp_list.append("Robot 2")
        temp_list.append("Robot 3")
        temp_list.append(str(""))
        temp_list.append("Ortalama Zaman")
        temp_list.append(str(""))
        temp_list.append("Ortalama Mesafe")
        temp_list.append(str(""))
        temp_list.append("Rota Secilme Miktari ->")
        temp_list.append("Rota Numarasi")
        temp_list.append("Secilme Miktari")

        self.write_data_list.append(temp_list)
        filter_list = list()

        for item in range(key_count):
            temp_list = list()
            time_list = list()
            distance_list = list()

            temp_list.append(str(item))
            temp_list.append(str(""))

            temp_list.append(self.system_main_dict[str(item)]["Secili Rota"])
            filter_list.append(self.system_main_dict[str(item)]["Secili Rota"])
            temp_list.append(str(""))

            temp_list.append(self.system_main_dict[str(item)]["POTC"])
            temp_list.append(str(""))

            temp_list.append(self.system_main_dict[str(item)]["Reliability"])
            temp_list.append(str(""))

            temp_list.append(str(""))
            temp_list.append(self.system_main_dict[str(item)]["Robot Reliability"][0])
            temp_list.append(self.system_main_dict[str(item)]["Robot Reliability"][1])
            temp_list.append(self.system_main_dict[str(item)]["Robot Reliability"][2])
            temp_list.append(str(""))

            temp_list.append(str(""))
            temp_list.append(self.time_convert_function(self.system_main_dict[str(item)]["Robot Time"][0]))
            temp_list.append(self.time_convert_function(self.system_main_dict[str(item)]["Robot Time"][1]))
            temp_list.append(self.time_convert_function(self.system_main_dict[str(item)]["Robot Time"][2]))
            temp_list.append(str(""))

            time_list.append(self.system_main_dict[str(item)]["Robot Time"][0])             # Time Average
            time_list.append(self.system_main_dict[str(item)]["Robot Time"][1])             # Time Average
            time_list.append(self.system_main_dict[str(item)]["Robot Time"][2])             # Time Average
            

            temp_list.append(str(""))
            temp_list.append(self.system_main_dict[str(item)]["Robot Distance"][0])
            temp_list.append(self.system_main_dict[str(item)]["Robot Distance"][1])
            temp_list.append(self.system_main_dict[str(item)]["Robot Distance"][2])
            temp_list.append(str(""))

            distance_list.append(self.system_main_dict[str(item)]["Robot Distance"][0])     # Distance Average
            distance_list.append(self.system_main_dict[str(item)]["Robot Distance"][1])     # Distance Average
            distance_list.append(self.system_main_dict[str(item)]["Robot Distance"][2])     # Distance Average

            time_average = self.average_list_func(time_list)
            temp_list.append(self.time_convert_function(time_average))

            temp_list.append(str(""))

            distance_average = self.average_list_func(distance_list)
            temp_list.append(distance_average)


            self.write_data_list.append(temp_list)

        uniq_filter_list = list(dict.fromkeys(filter_list))

        for item in uniq_filter_list:
            if item != 0:
                temp = [item, filter_list.count(item)]
                self.selected_route_count_list.append(temp)

        for i in range(len(self.selected_route_count_list)):
            self.write_data_list[(i+1)].append(str(""))
            self.write_data_list[(i+1)].append(str(""))
            self.write_data_list[(i+1)].append(self.selected_route_count_list[i][0])
            self.write_data_list[(i+1)].append(self.selected_route_count_list[i][1])


    def average_list_func(self, temp_list):
        result = 0.0

        for item in temp_list:
            result += float(item)

        list_count = len(temp_list)
        average_result = float(result / list_count)

        return average_result


    def calculate_system_reliability_func(self, robot_reliability_list):
        system_reliability = 1
        for rlblty in robot_reliability_list:
            system_reliability *= rlblty

        return system_reliability


    def get_mesafe_and_zaman_list_func(self, temp_mesafe_list, robot_cnt):
        list_count = len(temp_mesafe_list)
        mesafe_list = list()
        zaman_list = list()

        for count in range(list_count - 1):
            mesafe = float(self.distance_list[int(temp_mesafe_list[count])][int(temp_mesafe_list[count + 1])]) / 1000
            robot_speed_value = float(self.initial_configuration_dict[str("robot_" + str(robot_cnt))]["Speed"])
            zaman = self.calculate_time_func(mesafe, robot_speed_value)
            mesafe_list.append(mesafe)
            zaman_list.append(zaman)

        return mesafe_list, zaman_list


    def calculate_potc_and_reliability_func(self, process_count, mesafe_list, zaman_list, route_cnt, robot_cnt):
        time_value = 0
        distance_value = 0
        reliability_value = self.system_main_dict[str(process_count - 1)]["Robot Reliability"][robot_cnt - 1]
        potc_value = 0

        for item_count in range(len(mesafe_list)):
            selected_robot_hazard_rate = float(self.initial_configuration_dict[str("robot_" + str(robot_cnt))]["Hazard Rate"])
            selected_robot_nominal_capacity = float(self.initial_configuration_dict[str("robot_" + str(robot_cnt))]["Nominal Capacity"])

            if self.load_control:
                p_value = self.robot_main_dict["Yuk"][str("robot_" + str(robot_cnt))][str(route_cnt)][item_count]
                hazard_rate = self.failure_rate_calculation_using_operating_load_func(selected_robot_hazard_rate, p_value, selected_robot_nominal_capacity)

            else:
                hazard_rate = selected_robot_hazard_rate

            time_value += zaman_list[item_count]
            distance_value += mesafe_list[item_count]
            new_reliability = self.reliability_exponential_func(zaman_list[item_count], hazard_rate)
            reliability_value = reliability_value * new_reliability

            potc_value = self.probability_of_task_completion_formula(reliability_value, mesafe_list[item_count])

        return potc_value, reliability_value, time_value, distance_value


    def calculate_robot_potc_and_reliability_func(self, process_count, route_cnt):
        robot_potc_value = 1
        robot_reliability_value_list = list()
        robot_distance_list = list()
        robot_time_list = list()

        for j in range(self.robot_count):
            robot_cnt = int(j + 1)

            mesafe_list = list()
            zaman_list = list()
            temp_mesafe_list = list(self.robot_main_dict["Mesafe"][str("robot_" + str(robot_cnt))][str(route_cnt)])
            mesafe_list, zaman_list = self.get_mesafe_and_zaman_list_func(temp_mesafe_list, robot_cnt)

            potc_value, reliability_value, time_value, distance_value = self.calculate_potc_and_reliability_func(process_count, mesafe_list, zaman_list, route_cnt, robot_cnt)

            robot_potc_value *= potc_value
            robot_reliability_value_list.append(reliability_value)
            robot_time_list.append(time_value)
            robot_distance_list.append(distance_value)

        return robot_potc_value, robot_reliability_value_list, robot_time_list, robot_distance_list


    def calculate_main_potc_func(self):
        loop_control = False
        process_count = 0

        while not loop_control:
            process_count += 1

            self.system_main_dict[str(process_count)] = {"POTC": 1, "Reliability": 1, "Secili Rota": 0, "Robot Reliability": list()}
            potc_list = list([0])
            robot_reliability_list = list([0])
            system_reliability_list = list([0])
            time_list = list([0])
            distance_list = list([0])

            for i in range(self.route_count):
                route_cnt = int(i + 1)
                robot_potc_value, robot_reliability_value_list, robot_time_list, robot_distance_list = self.calculate_robot_potc_and_reliability_func(process_count, route_cnt)

                potc_list.append(float(robot_potc_value))
                robot_reliability_list.append(robot_reliability_value_list)
                system_reliability_value = self.calculate_system_reliability_func(robot_reliability_value_list)
                system_reliability_list.append(float(system_reliability_value))
                time_list.append(robot_time_list)
                distance_list.append(robot_distance_list)


            if self.threshold_type:
                best_value_index = potc_list.index(max(potc_list))

                if potc_list[best_value_index] < self.threshold_value:
                    loop_control = True

            else:
                best_value_index = system_reliability_list.index(max(system_reliability_list))

                if system_reliability_list[best_value_index] < self.threshold_value:
                    loop_control = True

            self.system_main_dict[str(process_count)]["POTC"] = potc_list[best_value_index]
            self.system_main_dict[str(process_count)]["Reliability"] = system_reliability_list[best_value_index]
            self.system_main_dict[str(process_count)]["Secili Rota"] = best_value_index
            self.system_main_dict[str(process_count)]["Robot Reliability"] = robot_reliability_list[best_value_index]
            self.system_main_dict[str(process_count)]["Robot Time"] = time_list[best_value_index]
            self.system_main_dict[str(process_count)]["Robot Distance"] = distance_list[best_value_index]

            print("Process Count -> " + str(process_count) + "   Selected Route -> " + str(best_value_index))

        self.set_write_data_list_func()    


if __name__ == '__main__':
    #try:
    #rospy.init_node('start_potc_analysis')

    app = QtWidgets.QApplication(sys.argv)
    MAIN_WINDOW = QtWidgets.QMainWindow()
    POTC_Gui = POTC_Analysis()
    POTC_Gui.setupUi(MAIN_WINDOW)
    MAIN_WINDOW.show()
    sys.exit(app.exec_())

    """
    except Exception as err:
        print(err)
    """
