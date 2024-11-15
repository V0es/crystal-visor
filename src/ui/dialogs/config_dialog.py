from PyQt6.QtWidgets import QDialog

from .resource.config_dialog.config_dialog_ui import Ui_config_dialog
from src.core.image_analysis import AnalysisSettings
from src.modbus.utils.dataframes.modbus_params import PollingSettings


class ConfigDialog(QDialog, Ui_config_dialog):
    def __init__(self,
                 current_analysis_settings: AnalysisSettings = AnalysisSettings(),
                 current_polling_settings: PollingSettings = PollingSettings(),
                 parent=None):
        super(ConfigDialog, self).__init__(parent)
        self.analysis_settings = current_analysis_settings
        self.polling_settings = current_polling_settings

        self.init_ui()

    def init_ui(self):
        self.setupUi(self)
        self.setWindowTitle('Настройки')
        self.load_settings()

    def load_settings(self):
        self.low_red_spinbox.setValue(self.analysis_settings.red_start)
        self.up_red_spinbox.setValue(self.analysis_settings.red_end)
        self.step_red_spinbox.setValue(self.analysis_settings.red_speed)

        self.low_green_spinbox.setValue(self.analysis_settings.green_start)
        self.up_green_spinbox.setValue(self.analysis_settings.green_end)
        self.step_green_spinbox.setValue(self.analysis_settings.green_speed)

        self.low_blue_spinbox.setValue(self.analysis_settings.blue_start)
        self.up_blue_spinbox.setValue(self.analysis_settings.blue_end)
        self.step_blue_spinbox.setValue(self.analysis_settings.blue_speed)

        self.cutoff_spinbox.setValue(self.analysis_settings.cut_off)
        self.scaling_coeff_spinbox.setValue(self.analysis_settings.scaling)
        self.base_height_dspinbox.setValue(self.analysis_settings.base_height)
        self.height_gap_dspinbox.setValue(self.analysis_settings.height_gap)

        self.trm_polling_spinbox.setValue(self.polling_settings.modbus_polling_rate // 60)
        self.camera_polling_spinbox.setValue(self.polling_settings.camera_polling_rate // 60)

    def get_data(self):
        analysis_settings = AnalysisSettings(
            self.low_red_spinbox.value(),
            self.up_red_spinbox.value(),
            self.step_red_spinbox.value(),

            self.low_green_spinbox.value(),
            self.up_green_spinbox.value(),
            self.step_green_spinbox.value(),

            self.low_blue_spinbox.value(),
            self.up_blue_spinbox.value(),
            self.step_blue_spinbox.value(),

            self.cutoff_spinbox.value(),
            self.scaling_coeff_spinbox.value(),
            self.base_height_dspinbox.value(),
            self.height_gap_dspinbox.value()

        )

        polling_settings = PollingSettings(
            self.trm_polling_spinbox.value() * 60,
            self.camera_polling_spinbox.value() * 60
        )

        return analysis_settings, polling_settings





