from PySide2.QtCore import QObject, Signal, Slot
from collections import OrderedDict as Od
import logging

logger = logging.getLogger(__name__)


class UiSettingsPreferencesTab(QObject):
    """Class dedicated to UI <--> Settings interactions on Settings/Preferences Tab. """

    ask_status_report_s = Signal()
    load_gcoder_cfg_s = Signal()
    save_all_settings_s = Signal()

    def __init__(self, ui, control_worker, settings):
        """
        Initialize ui elements of Settings/Preferences tab.

        Parameters
        ----------
        ui: Ui_MainWindow
            User interface object. Contains all user interface's children objects.
        control_worker: ControllerWorker
            Control thread worker object.
        settings: SettingsHandler
            Handler object that allows the access all the settings.
        """
        super(UiSettingsPreferencesTab, self).__init__()
        self.ui = ui
        self.control_wo = control_worker
        self.settings = settings
        self.machine_settings = settings.machine_settings

        self.get_tool_change_flag = False
        self.get_tool_probe_flag = False

        self.ui.tool_probe_wm_pos_chb.setChecked(self.machine_settings.tool_probe_rel_flag)
        self.tool_probe_wm_pos_checked()

        self.ui.tool_probe_wm_pos_chb.clicked.connect(self.tool_probe_wm_pos_checked)
        self.ui.get_tool_probe_pb.clicked.connect(self.ask_tool_probe_position)
        self.ask_status_report_s.connect(self.control_wo.report_status_report)
        self.control_wo.report_status_report_s.connect(self.get_and_manage_status_report)
        self.ui.get_tool_change_pb.clicked.connect(self.ask_tool_change_position)
        self.load_gcoder_cfg_s.connect(self.control_wo.update_gerber_cfg)
        self.ui.save_settings_preferences_pb.clicked.connect(self.save_settings_preferences)

        self.ui_tool_probe_set_enabling(enable=False)
        self.ui_tool_change_set_enabling(enable=False)

        self.set_tool_machine_initial_settings()

    def set_tool_machine_initial_settings(self):
        """Initialize ui value from initial machine settings."""
        self.ui.tool_probe_x_mpos_dsb.setValue(self.machine_settings.tool_probe_offset_x_mpos)
        self.ui.tool_probe_y_mpos_dsb.setValue(self.machine_settings.tool_probe_offset_y_mpos)
        self.ui.tool_probe_z_mpos_dsb.setValue(self.machine_settings.tool_probe_offset_z_mpos)
        self.ui.tool_probe_x_wpos_dsb.setValue(self.machine_settings.tool_probe_offset_x_wpos)
        self.ui.tool_probe_y_wpos_dsb.setValue(self.machine_settings.tool_probe_offset_y_wpos)
        self.ui.tool_probe_z_wpos_dsb.setValue(self.machine_settings.tool_probe_offset_z_wpos)

        self.ui.tool_change_x_mpos_dsb.setValue(self.machine_settings.tool_change_offset_x_mpos)
        self.ui.tool_change_y_mpos_dsb.setValue(self.machine_settings.tool_change_offset_y_mpos)
        self.ui.tool_change_z_mpos_dsb.setValue(self.machine_settings.tool_change_offset_z_mpos)

        self.ui.tool_probe_z_limit_dsb.setValue(self.machine_settings.tool_probe_z_limit)

        self.ui.feedrate_xy_dsb.setValue(self.machine_settings.feedrate_xy)
        self.ui.feedrate_z_dsb.setValue(self.machine_settings.feedrate_z)
        self.ui.feedrate_probe_dsb.setValue(self.machine_settings.feedrate_probe)

    def ui_tool_probe_set_enabling(self, enable=False):
        """Enable or disable tool probe get button. """
        self.ui.get_tool_probe_pb.setEnabled(enable)

    def ui_tool_change_set_enabling(self, enable=False):
        """Enable or disable tool change get button. """
        self.ui.get_tool_change_pb.setEnabled(enable)

    @Slot()
    def tool_probe_wm_pos_checked(self):
        """Update tool probe field passing from relative to absolute position and vice-versa. """
        wpos_flag = self.ui.tool_probe_wm_pos_chb.isChecked()
        if wpos_flag:
            self.ui.tool_probe_x_mpos_dsb.setEnabled(False)
            self.ui.tool_probe_y_mpos_dsb.setEnabled(False)
            self.ui.tool_probe_z_mpos_dsb.setEnabled(False)
            self.ui.tool_probe_x_wpos_dsb.setEnabled(True)
            self.ui.tool_probe_y_wpos_dsb.setEnabled(True)
            self.ui.tool_probe_z_wpos_dsb.setEnabled(True)
        else:
            self.ui.tool_probe_x_mpos_dsb.setEnabled(True)
            self.ui.tool_probe_y_mpos_dsb.setEnabled(True)
            self.ui.tool_probe_z_mpos_dsb.setEnabled(True)
            self.ui.tool_probe_x_wpos_dsb.setEnabled(False)
            self.ui.tool_probe_y_wpos_dsb.setEnabled(False)
            self.ui.tool_probe_z_wpos_dsb.setEnabled(False)

    def ask_status_report(self):
        """ Emit a signal asking asynchronously the controller status report. """
        self.ask_status_report_s.emit()

    @Slot(Od)
    def get_and_manage_status_report(self, actual_status_report):
        """ Asynchronously get status report and call function relative to function that asked for it. """
        if self.get_tool_probe_flag:
            self.get_tool_probe_flag = False
            self.get_tool_probe_position(actual_status_report)
        elif self.get_tool_change_flag:
            self.get_tool_change_flag = False
            self.get_tool_change_position(actual_status_report)

    def ask_tool_probe_position(self):
        """ Set get_tool_probe_flag at true and ask controller status report. """
        self.get_tool_probe_flag = True
        self.ask_status_report()

    def ask_tool_change_position(self):
        """ Set get_tool_probe_flag at true and ask controller status report. """
        self.get_tool_change_flag = True
        self.ask_status_report()

    def get_tool_probe_position(self, actual_status_report):
        """ Get tool offset mpos and wpos and update corresponding ui fields. """
        wpos_flag = self.ui.tool_probe_wm_pos_chb.isChecked()
        if wpos_flag:
            tool_probe_wpos = actual_status_report["wpos"]
            self.ui.tool_probe_x_wpos_dsb.setValue(tool_probe_wpos[0])
            self.ui.tool_probe_y_wpos_dsb.setValue(tool_probe_wpos[1])
            self.ui.tool_probe_z_wpos_dsb.setValue(tool_probe_wpos[2])
        else:
            tool_probe_mpos = actual_status_report["mpos"]
            self.ui.tool_probe_x_mpos_dsb.setValue(tool_probe_mpos[0])
            self.ui.tool_probe_y_mpos_dsb.setValue(tool_probe_mpos[1])
            self.ui.tool_probe_z_mpos_dsb.setValue(tool_probe_mpos[2])

    def get_tool_change_position(self, actual_status_report):
        """ Get tool change mpos and wpos and update corresponding ui fields. """
        tool_change_mpos = actual_status_report["mpos"]
        self.ui.tool_change_x_mpos_dsb.setValue(tool_change_mpos[0])
        self.ui.tool_change_y_mpos_dsb.setValue(tool_change_mpos[1])
        self.ui.tool_change_z_mpos_dsb.setValue(tool_change_mpos[2])

        self.load_gcoder_cfg_s.emit()

    def save_settings_preferences(self):
        """Save settings preferences from UI to settings."""
        self.machine_settings.tool_probe_rel_flag = self.ui.tool_probe_wm_pos_chb.isChecked()

        self.machine_settings.tool_probe_offset_x_mpos = self.ui.tool_probe_x_mpos_dsb.value()
        self.machine_settings.tool_probe_offset_y_mpos = self.ui.tool_probe_y_mpos_dsb.value()
        self.machine_settings.tool_probe_offset_z_mpos = self.ui.tool_probe_z_mpos_dsb.value()

        self.machine_settings.tool_probe_offset_x_wpos = self.ui.tool_probe_x_wpos_dsb.value()
        self.machine_settings.tool_probe_offset_y_wpos = self.ui.tool_probe_y_wpos_dsb.value()
        self.machine_settings.tool_probe_offset_z_wpos = self.ui.tool_probe_z_wpos_dsb.value()

        self.machine_settings.tool_change_offset_x_mpos = self.ui.tool_change_x_mpos_dsb.value()
        self.machine_settings.tool_change_offset_y_mpos = self.ui.tool_change_y_mpos_dsb.value()
        self.machine_settings.tool_change_offset_z_mpos = self.ui.tool_change_z_mpos_dsb.value()

        self.machine_settings.tool_probe_z_limit = self.ui.tool_probe_z_limit_dsb.value()

        self.machine_settings.feedrate_xy = self.ui.feedrate_xy_dsb.value()
        self.machine_settings.feedrate_z = self.ui.feedrate_z_dsb.value()
        self.machine_settings.feedrate_probe = self.ui.feedrate_probe_dsb.value()

        self.load_gcoder_cfg_s.emit()

        # Emit a signal to write all settings
        self.save_all_settings_s.emit()
