# Form implementation generated from reading ui file 'display_panel.ui'
#
# Created by: PyQt6 UI code generator 6.7.1
#
# WARNING: Any manual changes made to this file will be lost when pyuic6 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt6 import QtCore, QtGui, QtWidgets


class Ui_display_panel(object):
    def setupUi(self, display_panel):
        display_panel.setObjectName("display_panel")
        display_panel.resize(342, 397)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.MinimumExpanding, QtWidgets.QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(display_panel.sizePolicy().hasHeightForWidth())
        display_panel.setSizePolicy(sizePolicy)
        self.verticalLayout = QtWidgets.QVBoxLayout(display_panel)
        self.verticalLayout.setObjectName("verticalLayout")
        self.title_label = QtWidgets.QLabel(parent=display_panel)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.MinimumExpanding, QtWidgets.QSizePolicy.Policy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.title_label.sizePolicy().hasHeightForWidth())
        self.title_label.setSizePolicy(sizePolicy)
        self.title_label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.title_label.setObjectName("title_label")
        self.verticalLayout.addWidget(self.title_label)
        self.display_layout = QtWidgets.QFormLayout()
        self.display_layout.setContentsMargins(-1, 101, -1, 0)
        self.display_layout.setObjectName("display_layout")
        self.target_temperature_label = QtWidgets.QLabel(parent=display_panel)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.MinimumExpanding, QtWidgets.QSizePolicy.Policy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.target_temperature_label.sizePolicy().hasHeightForWidth())
        self.target_temperature_label.setSizePolicy(sizePolicy)
        self.target_temperature_label.setObjectName("target_temperature_label")
        self.display_layout.setWidget(2, QtWidgets.QFormLayout.ItemRole.LabelRole, self.target_temperature_label)
        self.target_temp_lcd = QtWidgets.QLCDNumber(parent=display_panel)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.MinimumExpanding, QtWidgets.QSizePolicy.Policy.MinimumExpanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.target_temp_lcd.sizePolicy().hasHeightForWidth())
        self.target_temp_lcd.setSizePolicy(sizePolicy)
        self.target_temp_lcd.setFrameShape(QtWidgets.QFrame.Shape.Box)
        self.target_temp_lcd.setFrameShadow(QtWidgets.QFrame.Shadow.Plain)
        self.target_temp_lcd.setSegmentStyle(QtWidgets.QLCDNumber.SegmentStyle.Flat)
        self.target_temp_lcd.setProperty("intValue", 0)
        self.target_temp_lcd.setObjectName("target_temp_lcd")
        self.display_layout.setWidget(2, QtWidgets.QFormLayout.ItemRole.FieldRole, self.target_temp_lcd)
        self.point_position_label = QtWidgets.QLabel(parent=display_panel)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.MinimumExpanding, QtWidgets.QSizePolicy.Policy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.point_position_label.sizePolicy().hasHeightForWidth())
        self.point_position_label.setSizePolicy(sizePolicy)
        self.point_position_label.setObjectName("point_position_label")
        self.display_layout.setWidget(3, QtWidgets.QFormLayout.ItemRole.LabelRole, self.point_position_label)
        self.point_position_lcd = QtWidgets.QLCDNumber(parent=display_panel)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.MinimumExpanding, QtWidgets.QSizePolicy.Policy.MinimumExpanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.point_position_lcd.sizePolicy().hasHeightForWidth())
        self.point_position_lcd.setSizePolicy(sizePolicy)
        self.point_position_lcd.setFrameShadow(QtWidgets.QFrame.Shadow.Plain)
        self.point_position_lcd.setSegmentStyle(QtWidgets.QLCDNumber.SegmentStyle.Flat)
        self.point_position_lcd.setObjectName("point_position_lcd")
        self.display_layout.setWidget(3, QtWidgets.QFormLayout.ItemRole.FieldRole, self.point_position_lcd)
        self.raising_time_label = QtWidgets.QLabel(parent=display_panel)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.MinimumExpanding, QtWidgets.QSizePolicy.Policy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.raising_time_label.sizePolicy().hasHeightForWidth())
        self.raising_time_label.setSizePolicy(sizePolicy)
        self.raising_time_label.setObjectName("raising_time_label")
        self.display_layout.setWidget(4, QtWidgets.QFormLayout.ItemRole.LabelRole, self.raising_time_label)
        self.raising_time_lcd = QtWidgets.QLCDNumber(parent=display_panel)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.MinimumExpanding, QtWidgets.QSizePolicy.Policy.MinimumExpanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.raising_time_lcd.sizePolicy().hasHeightForWidth())
        self.raising_time_lcd.setSizePolicy(sizePolicy)
        self.raising_time_lcd.setFrameShadow(QtWidgets.QFrame.Shadow.Plain)
        self.raising_time_lcd.setSegmentStyle(QtWidgets.QLCDNumber.SegmentStyle.Flat)
        self.raising_time_lcd.setObjectName("raising_time_lcd")
        self.display_layout.setWidget(4, QtWidgets.QFormLayout.ItemRole.FieldRole, self.raising_time_lcd)
        self.holding_time_label = QtWidgets.QLabel(parent=display_panel)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.MinimumExpanding, QtWidgets.QSizePolicy.Policy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.holding_time_label.sizePolicy().hasHeightForWidth())
        self.holding_time_label.setSizePolicy(sizePolicy)
        self.holding_time_label.setObjectName("holding_time_label")
        self.display_layout.setWidget(5, QtWidgets.QFormLayout.ItemRole.LabelRole, self.holding_time_label)
        self.holding_temp_lcd = QtWidgets.QLCDNumber(parent=display_panel)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.MinimumExpanding, QtWidgets.QSizePolicy.Policy.MinimumExpanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.holding_temp_lcd.sizePolicy().hasHeightForWidth())
        self.holding_temp_lcd.setSizePolicy(sizePolicy)
        self.holding_temp_lcd.setFrameShadow(QtWidgets.QFrame.Shadow.Plain)
        self.holding_temp_lcd.setSegmentStyle(QtWidgets.QLCDNumber.SegmentStyle.Flat)
        self.holding_temp_lcd.setObjectName("holding_temp_lcd")
        self.display_layout.setWidget(5, QtWidgets.QFormLayout.ItemRole.FieldRole, self.holding_temp_lcd)
        self.current_temperature_label = QtWidgets.QLabel(parent=display_panel)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.MinimumExpanding, QtWidgets.QSizePolicy.Policy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.current_temperature_label.sizePolicy().hasHeightForWidth())
        self.current_temperature_label.setSizePolicy(sizePolicy)
        self.current_temperature_label.setObjectName("current_temperature_label")
        self.display_layout.setWidget(6, QtWidgets.QFormLayout.ItemRole.LabelRole, self.current_temperature_label)
        self.current_temperature_lcd = QtWidgets.QLCDNumber(parent=display_panel)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.MinimumExpanding, QtWidgets.QSizePolicy.Policy.MinimumExpanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.current_temperature_lcd.sizePolicy().hasHeightForWidth())
        self.current_temperature_lcd.setSizePolicy(sizePolicy)
        self.current_temperature_lcd.setFrameShape(QtWidgets.QFrame.Shape.Box)
        self.current_temperature_lcd.setFrameShadow(QtWidgets.QFrame.Shadow.Plain)
        self.current_temperature_lcd.setSegmentStyle(QtWidgets.QLCDNumber.SegmentStyle.Flat)
        self.current_temperature_lcd.setObjectName("current_temperature_lcd")
        self.display_layout.setWidget(6, QtWidgets.QFormLayout.ItemRole.FieldRole, self.current_temperature_lcd)
        self.device_state_label = QtWidgets.QLabel(parent=display_panel)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.MinimumExpanding, QtWidgets.QSizePolicy.Policy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.device_state_label.sizePolicy().hasHeightForWidth())
        self.device_state_label.setSizePolicy(sizePolicy)
        self.device_state_label.setObjectName("device_state_label")
        self.display_layout.setWidget(7, QtWidgets.QFormLayout.ItemRole.LabelRole, self.device_state_label)
        self.device_state_lcd = QtWidgets.QLCDNumber(parent=display_panel)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.MinimumExpanding, QtWidgets.QSizePolicy.Policy.MinimumExpanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.device_state_lcd.sizePolicy().hasHeightForWidth())
        self.device_state_lcd.setSizePolicy(sizePolicy)
        self.device_state_lcd.setFrameShadow(QtWidgets.QFrame.Shadow.Plain)
        self.device_state_lcd.setSegmentStyle(QtWidgets.QLCDNumber.SegmentStyle.Flat)
        self.device_state_lcd.setObjectName("device_state_lcd")
        self.display_layout.setWidget(7, QtWidgets.QFormLayout.ItemRole.FieldRole, self.device_state_lcd)
        self.verticalLayout.addLayout(self.display_layout)

        self.retranslateUi(display_panel)
        QtCore.QMetaObject.connectSlotsByName(display_panel)

    def retranslateUi(self, display_panel):
        _translate = QtCore.QCoreApplication.translate
        display_panel.setWindowTitle(_translate("display_panel", "Form"))
        self.title_label.setText(_translate("display_panel", "Текущие значения"))
        self.target_temperature_label.setText(_translate("display_panel", "Уставка, °С"))
        self.point_position_label.setText(_translate("display_panel", "Положение дес. точки"))
        self.raising_time_label.setText(_translate("display_panel", "Время роста, с"))
        self.holding_time_label.setText(_translate("display_panel", "Время выдержки, с"))
        self.current_temperature_label.setText(_translate("display_panel", "Текущая температура, °C"))
        self.device_state_label.setText(_translate("display_panel", "Состояние прибора"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    display_panel = QtWidgets.QWidget()
    ui = Ui_display_panel()
    ui.setupUi(display_panel)
    display_panel.show()
    sys.exit(app.exec())
