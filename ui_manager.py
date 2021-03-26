import os
from PySide2.QtWidgets import QFileDialog
from PySide2.QtCore import Signal, Slot, QObject
from PySide2.QtGui import QPixmap
from shape_core.visual_manager import VisualLayer
from collections import OrderedDict as Od
import logging

logger = logging.getLogger(__name__)


class UiManager(QObject):
    """Manage UI objects, signals and slots"""
    L_TAGS = ["top", "bottom", "profile", "drill"]
    L_COLORS = ["red", "blue", "black", "green"]
    LOG_COLORS = {
        logging.DEBUG:    'white',
        logging.INFO:     'light blue',
        logging.WARNING:  'orange',
        logging.ERROR:    'red',
        logging.CRITICAL: 'purple',
    }
    load_layer_s = Signal(str, str)
    change_visibility_s = Signal(str, bool)
    align_active_s = Signal(bool)
    update_threshold_s = Signal(int)
    serial_send_s = Signal(str)

    def __init__(self, main_win, ui, control_worker, serial_worker, settings):
        super(UiManager, self).__init__()
        self.main_win = main_win
        self.ui = ui
        self.controlWo = control_worker
        self.serialWo = serial_worker
        self.settings = settings

        self.connection_status = False
        self.vis_layer = VisualLayer(self.ui.viewCanvasWidget)
        self.layer_colors = Od([(k, v) for k, v in zip(self.L_TAGS, self.L_COLORS)])
        self.L_TEXT = [self.ui.topFileLineEdit, self.ui.bottomFileLineEdit,
                       self.ui.profileFileLineEdit, self.ui.drillFileLineEdit]
        self.layers_te = Od([(k, t) for k, t in zip(self.L_TAGS, self.L_TEXT)])
        self.L_CHECKBOX = [self.ui.topViewCheckBox, self.ui.bottomViewCheckBox,
                           self.ui.profileViewCheckBox, self.ui.drillViewCheckBox]
        self.layers_cb = Od([(k, t) for k, t in zip(self.L_TAGS, self.L_CHECKBOX)])

        self.ui.send_text_edit.setPlaceholderText('input here')
        self.ui.send_text_edit.hide()
        self.ui.send_push_button.hide()

        # Connect Widgets signals and slots
        # From UI to UI Manager
        self.ui.refreshButton.clicked.connect(self.handle_refresh_button)
        self.ui.connectButton.clicked.connect(self.handle_connect_button)
        self.ui.clearTerminalButton.clicked.connect(self.handle_clear_terminal)
        self.ui.send_push_button.clicked.connect(self.send_input)
        self.ui.send_text_edit.returnPressed.connect(self.send_input)
        self.ui.unlockButton.clicked.connect(self.handle_unlock)
        self.ui.homingButton.clicked.connect(self.handle_homing)
        self.ui.xMinusButton.clicked.connect(self.handle_x_minus)
        self.ui.tabWidget.currentChanged.connect(self.check_align_is_active)
        self.ui.verticalSlider.valueChanged.connect(self.update_threshold)
        self.ui.actionHide_Show_Console.triggered.connect(self.hide_show_console)
        self.ui.clear_views_push_button.clicked.connect(self.remove_all_vis_layers)

        # From UI Manager to Controller
        self.align_active_s.connect(self.controlWo.set_align_is_active)
        self.load_layer_s.connect(self.controlWo.load_new_layer)
        self.update_threshold_s.connect(self.controlWo.update_threshold_value)
        self.ui.topLoadButton.clicked.connect(
            lambda: self.load_gerber_file(self.L_TAGS[0], "Load Top Gerber File", "Gerber (*.gbr *.GBR)"))
        self.ui.bottomLoadButton.clicked.connect(
            lambda: self.load_gerber_file(self.L_TAGS[1], "Load Bottom Gerber File", "Gerber (*.gbr *.GBR)"))
        self.ui.profileLoadButton.clicked.connect(
            lambda: self.load_gerber_file(self.L_TAGS[2], "Load Profile Gerber File", "Gerber (*.gbr *.GBR)"))
        self.ui.drillLoadButton.clicked.connect(
            lambda: self.load_gerber_file(self.L_TAGS[3], "Load Drill Excellon File", "Excellon (*.xln *.XLN)"))
        self.ui.topViewCheckBox.stateChanged.connect(
            lambda: self.set_layer_visible("top", self.ui.topViewCheckBox.isChecked()))
        self.ui.bottomViewCheckBox.stateChanged.connect(
            lambda: self.set_layer_visible("bottom", self.ui.bottomViewCheckBox.isChecked()))
        self.ui.profileViewCheckBox.stateChanged.connect(
            lambda: self.set_layer_visible("profile", self.ui.profileViewCheckBox.isChecked()))
        self.ui.drillViewCheckBox.stateChanged.connect(
            lambda: self.set_layer_visible("drill", self.ui.drillViewCheckBox.isChecked()))
        self.ui.all_view_checkbox.stateChanged.connect(lambda: self.hide_show_layers(self.ui.all_view_checkbox.isChecked()))

        # From UI Manager to Serial Manager
        self.serial_send_s.connect(self.serialWo.send)

        # From Controller Manager to UI Manager
        self.controlWo.update_layer_s.connect(self.visualize_new_layer)
        self.controlWo.update_camera_image_s.connect(self.update_camera_image)
        self.controlWo.update_status_s.connect(self.update_status)
        self.controlWo.update_console_text_s.connect(self.update_console_text)

        # From Controller Manager to Serial Manager
        self.controlWo.serial_send_s.connect(self.serialWo.send)

        # From Serial Manager to UI Manager
        self.serialWo.update_console_text_s.connect(self.update_console_text)

        # From Serial Manager to Control Manager
        self.serialWo.rx_queue_not_empty_s.connect(self.controlWo.parse_rx_queue)

    def load_gerber_file(self, layer="top", load_text="Load File", extensions=""):
        filters = extensions + ";;All files (*.*)"
        load_file_path = QFileDialog.getOpenFileName(self.main_win, load_text, self.settings.layer_last_dir, filters)
        if load_file_path[0]:
            self.vis_layer.remove_layer(layer)
            self.settings.layer_last_dir = os.path.dirname(load_file_path[0])
            logging.info("Loading " + load_file_path[0])
            self.load_layer_s.emit(layer, load_file_path[0])

    def remove_all_vis_layers(self):
        loaded_views = list(self.vis_layer.get_layers_tag())
        for view in loaded_views:
            self.vis_layer.remove_layer(view)

    def hide_show_layers(self, checked):
        for cb in self.layers_cb:
            self.layers_cb[cb].setChecked(checked)

    @Slot(str, bool)
    def set_layer_visible(self, tag, visible):
        self.vis_layer.set_layer_visible(tag, visible)

    @Slot(Od, str, str, bool)
    def visualize_new_layer(self, loaded_layer, layer, layer_path, holes):
        self.vis_layer.add_layer(layer, loaded_layer[0], self.layer_colors[layer], holes)
        self.layers_te[layer].setText(layer_path)

    @Slot(str, logging.LogRecord)
    def update_logging_status(self, status, record):
        color = self.LOG_COLORS.get(record.levelno, 'black')
        s = '<pre><font color="%s">%s</font></pre>' % (color, status)
        self.ui.logging_plain_text_edit.appendHtml(s)

    @Slot(QPixmap)
    def update_camera_image(self, pixmap):
        self.ui.label_2.setPixmap(pixmap)

    @Slot(list)
    def update_status(self, status_l):
        self.ui.statusLabel.setText(status_l[0])
        self.ui.mpos_x_label.setText(status_l[1][0])
        self.ui.mpos_y_label.setText(status_l[1][1])
        self.ui.mpos_z_label.setText(status_l[1][2])

    @Slot(str)
    def update_console_text(self, new_text):
        self.ui.textEdit.append(new_text)

    def check_align_is_active(self):
        self.align_active_s.emit(self.ui.tabWidget.currentWidget().objectName() == "alignTab")

    def update_threshold(self):
        self.update_threshold_s.emit(self.ui.verticalSlider.value())

    def send_input(self):
        """Send input to the serial port."""
        # self.serialTxQu.put(self.ui.send_text_edit.text() + "\n")
        self.serial_send_s.emit(self.ui.send_text_edit.text() + "\n")
        self.ui.send_text_edit.clear()

    def handle_refresh_button(self):
        """Get list of serial ports available."""
        ls = self.serialWo.get_port_list()
        if ls:
            logger.debug("Available ports: " + str(ls))
            self.ui.serialPortsComboBox.clear()
            self.ui.serialPortsComboBox.addItems(ls)
        else:
            logger.info('No serial ports available.')
            self.ui.textEdit.append('No serial ports available.')
            self.ui.serialPortsComboBox.clear()

    def handle_connect_button(self):
        """Connect/Disconnect button opens/closes the selected serial port and
           creates the serial worker thread. If the thread was
           already created previously and paused, it revives it."""
        if not self.connection_status:
            if self.serialWo.open_port(self.ui.serialPortsComboBox.currentText()):
                self.connection_status = True
                self.ui.connectButton.setText("Disconnect")
                self.ui.serialPortsComboBox.hide()
                self.ui.refreshButton.hide()
                self.ui.send_text_edit.show()
                self.ui.send_push_button.show()
        else:
            self.serialWo.close_port()
            self.connection_status = False
            self.ui.connectButton.setText("Connect")
            self.ui.serialPortsComboBox.show()
            self.ui.refreshButton.show()
            self.ui.send_text_edit.hide()
            self.ui.send_push_button.hide()
            self.ui.statusLabel.setText("Not Connected")

    def handle_clear_terminal(self):
        self.ui.textEdit.clear()

    def hide_show_console(self):
        if self.ui.actionHide_Show_Console.isChecked():
            self.ui.logging_plain_text_edit.show()
        else:
            self.ui.logging_plain_text_edit.hide()

    def handle_unlock(self):
        logging.debug("Unlock Command")
        self.serial_send_s.emit("$X\n")

    def handle_homing(self):
        logging.debug("Homing Command")
        self.serial_send_s.emit("$H\n")

    def handle_x_minus(self):
        logging.debug("X_minus Command")
        # self.serialTxQu.put("$J=G91 X-10 F100000\n") #todo: change this, just for test
        self.serial_send_s.emit("$J=G91 X-10 F100000\n")  # todo: change this, just for test


if __name__ == "__main__":
    pass
