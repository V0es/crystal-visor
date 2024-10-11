# Form implementation generated from reading ui file 'control_panel.ui'
#
# Created by: PyQt6 UI code generator 6.7.1
#
# WARNING: Any manual changes made to this file will be lost when pyuic6 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt6 import QtCore, QtGui, QtWidgets


class Ui_control_panel(object):
    def setupUi(self, control_panel):
        control_panel.setObjectName("control_panel")
        control_panel.resize(300, 410)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(control_panel.sizePolicy().hasHeightForWidth())
        control_panel.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(8)
        control_panel.setFont(font)
        self.verticalLayout = QtWidgets.QVBoxLayout(control_panel)
        self.verticalLayout.setSpacing(9)
        self.verticalLayout.setObjectName("verticalLayout")
        self.set_new_values_label = QtWidgets.QLabel(parent=control_panel)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.set_new_values_label.sizePolicy().hasHeightForWidth())
        self.set_new_values_label.setSizePolicy(sizePolicy)
        self.set_new_values_label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.set_new_values_label.setIndent(0)
        self.set_new_values_label.setObjectName("set_new_values_label")
        self.verticalLayout.addWidget(self.set_new_values_label)
        self.time_label = QtWidgets.QLabel(parent=control_panel)
        font = QtGui.QFont()
        font.setPointSize(11)
        font.setBold(True)
        font.setWeight(75)
        font.setStrikeOut(False)
        self.time_label.setFont(font)
        self.time_label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.time_label.setObjectName("time_label")
        self.verticalLayout.addWidget(self.time_label)
        self.formLayout = QtWidgets.QFormLayout()
        self.formLayout.setVerticalSpacing(4)
        self.formLayout.setObjectName("formLayout")
        self.new_temperature_spinbox = QtWidgets.QSpinBox(parent=control_panel)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.MinimumExpanding, QtWidgets.QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.new_temperature_spinbox.sizePolicy().hasHeightForWidth())
        self.new_temperature_spinbox.setSizePolicy(sizePolicy)
        self.new_temperature_spinbox.setMaximum(5000)
        self.new_temperature_spinbox.setObjectName("new_temperature_spinbox")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.ItemRole.FieldRole, self.new_temperature_spinbox)
        self.new_point_position_spinbox = QtWidgets.QSpinBox(parent=control_panel)
        self.new_point_position_spinbox.setMaximum(5000)
        self.new_point_position_spinbox.setObjectName("new_point_position_spinbox")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.ItemRole.FieldRole, self.new_point_position_spinbox)
        self.new_raising_time_spinbox = QtWidgets.QSpinBox(parent=control_panel)
        self.new_raising_time_spinbox.setMaximum(5000)
        self.new_raising_time_spinbox.setObjectName("new_raising_time_spinbox")
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.ItemRole.FieldRole, self.new_raising_time_spinbox)
        self.new_holding_time_spinbox = QtWidgets.QSpinBox(parent=control_panel)
        self.new_holding_time_spinbox.setMaximum(5000)
        self.new_holding_time_spinbox.setObjectName("new_holding_time_spinbox")
        self.formLayout.setWidget(3, QtWidgets.QFormLayout.ItemRole.FieldRole, self.new_holding_time_spinbox)
        self.new_temp_label = QtWidgets.QLabel(parent=control_panel)
        self.new_temp_label.setObjectName("new_temp_label")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.ItemRole.LabelRole, self.new_temp_label)
        self.new_point_position_label = QtWidgets.QLabel(parent=control_panel)
        self.new_point_position_label.setObjectName("new_point_position_label")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.ItemRole.LabelRole, self.new_point_position_label)
        self.new_raising_time_label = QtWidgets.QLabel(parent=control_panel)
        self.new_raising_time_label.setObjectName("new_raising_time_label")
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.ItemRole.LabelRole, self.new_raising_time_label)
        self.new_holding_time_label = QtWidgets.QLabel(parent=control_panel)
        self.new_holding_time_label.setObjectName("new_holding_time_label")
        self.formLayout.setWidget(3, QtWidgets.QFormLayout.ItemRole.LabelRole, self.new_holding_time_label)
        self.verticalLayout.addLayout(self.formLayout)
        self.auto_temp_adjustment_checkbox = QtWidgets.QCheckBox(parent=control_panel)
        self.auto_temp_adjustment_checkbox.setObjectName("auto_temp_adjustment_checkbox")
        self.verticalLayout.addWidget(self.auto_temp_adjustment_checkbox)
        self.verticalLayout_2 = QtWidgets.QVBoxLayout()
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.delta_adjustment_label = QtWidgets.QLabel(parent=control_panel)
        self.delta_adjustment_label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.delta_adjustment_label.setObjectName("delta_adjustment_label")
        self.verticalLayout_2.addWidget(self.delta_adjustment_label)
        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout.setObjectName("gridLayout")
        self.delta_temperature_label = QtWidgets.QLabel(parent=control_panel)
        self.delta_temperature_label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.delta_temperature_label.setObjectName("delta_temperature_label")
        self.gridLayout.addWidget(self.delta_temperature_label, 0, 0, 1, 1)
        self.delta_temperature_dspinbox = QtWidgets.QDoubleSpinBox(parent=control_panel)
        self.delta_temperature_dspinbox.setMaximum(5000.0)
        self.delta_temperature_dspinbox.setObjectName("delta_temperature_dspinbox")
        self.gridLayout.addWidget(self.delta_temperature_dspinbox, 0, 1, 1, 1)
        self.verticalLayout_2.addLayout(self.gridLayout)
        self.verticalLayout.addLayout(self.verticalLayout_2)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.start_process_btn = QtWidgets.QPushButton(parent=control_panel)
        self.start_process_btn.setObjectName("start_process_btn")
        self.horizontalLayout.addWidget(self.start_process_btn)
        self.pause_process_btn = QtWidgets.QPushButton(parent=control_panel)
        self.pause_process_btn.setObjectName("pause_process_btn")
        self.horizontalLayout.addWidget(self.pause_process_btn)
        self.stop_process_btn = QtWidgets.QPushButton(parent=control_panel)
        self.stop_process_btn.setObjectName("stop_process_btn")
        self.horizontalLayout.addWidget(self.stop_process_btn)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.set_new_values_btn = QtWidgets.QPushButton(parent=control_panel)
        self.set_new_values_btn.setObjectName("set_new_values_btn")
        self.verticalLayout.addWidget(self.set_new_values_btn)
        self.start_preheat_btn = QtWidgets.QPushButton(parent=control_panel)
        self.start_preheat_btn.setObjectName("start_preheat_btn")
        self.verticalLayout.addWidget(self.start_preheat_btn)

        self.retranslateUi(control_panel)
        QtCore.QMetaObject.connectSlotsByName(control_panel)

    def retranslateUi(self, control_panel):
        _translate = QtCore.QCoreApplication.translate
        control_panel.setWindowTitle(_translate("control_panel", "Form"))
        self.set_new_values_label.setText(_translate("control_panel", "Записать значения"))
        self.time_label.setText(_translate("control_panel", "00:00:00"))
        self.new_temp_label.setText(_translate("control_panel", "Температура, °С"))
        self.new_point_position_label.setText(_translate("control_panel", "Дес. точка"))
        self.new_raising_time_label.setText(_translate("control_panel", "Время роста, с"))
        self.new_holding_time_label.setText(_translate("control_panel", "Время выдержки, с"))
        self.auto_temp_adjustment_checkbox.setText(_translate("control_panel", "Автоматически регулировать температуру"))
        self.delta_adjustment_label.setText(_translate("control_panel", "Регулирование"))
        self.delta_temperature_label.setText(_translate("control_panel", "Δ, °С"))
        self.start_process_btn.setText(_translate("control_panel", "Старт"))
        self.pause_process_btn.setText(_translate("control_panel", "Пауза"))
        self.stop_process_btn.setText(_translate("control_panel", "Стоп"))
        self.set_new_values_btn.setText(_translate("control_panel", "Записать"))
        self.start_preheat_btn.setText(_translate("control_panel", "Преднагрев"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    control_panel = QtWidgets.QWidget()
    ui = Ui_control_panel()
    ui.setupUi(control_panel)
    control_panel.show()
    sys.exit(app.exec())
