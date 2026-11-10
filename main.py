from PySide6.QtWidgets import (
    QApplication,
    QMainWindow,
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QListWidget,
    QTextEdit,
    QFrame,
    QToolBar,
    QStatusBar,
    QSplitter,
    QTreeWidget,
    QTreeWidgetItem,
    QSlider,
    QGroupBox,
    QFormLayout,
    QWidget, QVBoxLayout, QFormLayout,
    QGroupBox, QSlider, QTextEdit,
    QFrame, QTabWidget
)
from PySide6.QtCore import Qt
from PySide6.QtGui import QAction
import sys


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("3D Camera Studio")
        self.resize(1600, 950)

        self.setStyleSheet("""
            QMainWindow {
                background-color: #1e1e1e;
            }

            QWidget {
                background-color: #252526;
                color: #e0e0e0;
                font-size: 12px;
            }

            QPushButton {
                background-color: #3c3c3c;
                border: 1px solid #555;
                padding: 8px;
                border-radius: 6px;
            }

            QPushButton:hover {
                background-color: #4a4a4a;
            }

            QTextEdit, QListWidget, QTreeWidget {
                background-color: #1b1b1b;
                border: 1px solid #444;
            }

            QGroupBox {
                border: 1px solid #444;
                margin-top: 10px;
                padding-top: 10px;
                font-weight: bold;
            }

            QSlider::groove:horizontal {
                height: 4px;
                background: #444;
            }

            QSlider::handle:horizontal {
                background: #00aaff;
                width: 14px;
                margin: -5px 0;
                border-radius: 7px;
            }
                           
            QTabWidget::pane {
                border: 1px solid #444;
                background: #252526;
                top: -1px;
            }

            QTabBar::tab {
                background: #2d2d30;
                color: #cccccc;
                padding: 10px;
                min-width: 120px;
                border: 1px solid #444;
                border-bottom: none;
                border-top-left-radius: 6px;
                border-top-right-radius: 6px;
            }

            QTabBar::tab:selected {
                background: #0078d7;
                color: white;
                font-weight: bold;
            }

            QTabBar::tab:hover {
                background: #3e3e42;
            }
        """)

        self.create_toolbar()
        # self.create_statusbar()
        self.create_main_layout()
    def create_toolbar(self):
        
        # Create Menu Bar
        menu_bar = self.menuBar()

        # =========================
        # File Menu
        # =========================
        file_menu = menu_bar.addMenu("File")

        open_action = QAction("Open", self)
        save_action = QAction("Save ", self)
        exit_action = QAction("Exit", self)

        file_menu.addAction(open_action)
        file_menu.addAction(save_action)
        file_menu.addAction(exit_action)

        # =========================
        # View Menu
        # =========================
        view_menu = menu_bar.addMenu("View")

        rgb_view_action = QAction("Reset", self)
        depth_view_action = QAction("Full Screen", self)
        pointcloud_view_action = QAction("Information", self)

        view_menu.addAction(rgb_view_action)
        view_menu.addAction(depth_view_action)
        view_menu.addAction(pointcloud_view_action)

        # =========================
        # Tools Menu
        # =========================
        tools_menu = menu_bar.addMenu("Tools")

        calibration_action = QAction("Calibration", self)
        meshing_action = QAction("Meshing", self)
        filtering_action = QAction("Filtering", self)

        tools_menu.addAction(calibration_action)
        tools_menu.addAction(meshing_action)
        tools_menu.addAction(filtering_action)

        # =========================
        # Help Menu
        # =========================
        help_menu = menu_bar.addMenu("Help")

        documentation_action = QAction("Documentation", self)
        update_action = QAction("Check Updates", self)
        about_action = QAction("About", self)

        help_menu.addAction(documentation_action)
        help_menu.addAction(update_action)
        help_menu.addAction(about_action)



    def create_statusbar(self):
        status = QStatusBar()
        status.showMessage("Ready")
        self.setStatusBar(status)

    def create_main_layout(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        main_layout = QHBoxLayout(central_widget)
        main_layout.setContentsMargins(4, 4, 4, 4)

        splitter = QSplitter(Qt.Horizontal)

        # ==================================
        # CENTER VIEWER
        # ==================================
        center_panel = QFrame()

        viewer = QLabel("3D POINT CLOUD VIEW")
        viewer.setAlignment(Qt.AlignCenter)
        viewer.setStyleSheet("""
            background-color: #111;
            border: 1px solid #444;
            font-size: 28px;
            font-weight: bold;
            color: #00aaff;
        """)
        # ==================================
        # RIGHT PANEL
        # ==================================
        right_panel = QFrame()
        right_panel.setFixedWidth(320)

        right_layout = QVBoxLayout(right_panel)

        # ==================================
        # TAB WIDGET
        # ==================================
        tabs = QTabWidget()

        # =========================================================
        # RGB CAMERA TAB
        # =========================================================
        rgb_tab = QWidget()
        rgb_layout = QVBoxLayout(rgb_tab)

        rgb_settings_group = QGroupBox("RGB Capture Settings")
        rgb_settings_layout = QFormLayout()

        rgb_exposure_slider = QSlider(Qt.Horizontal)
        rgb_gain_slider = QSlider(Qt.Horizontal)
        rgb_brightness_slider = QSlider(Qt.Horizontal)

        rgb_settings_layout.addRow("Exposure", rgb_exposure_slider)
        rgb_settings_layout.addRow("Gain", rgb_gain_slider)
        rgb_settings_layout.addRow("Brightness", rgb_brightness_slider)

        rgb_settings_group.setLayout(rgb_settings_layout)
        rgb_button_layout = QHBoxLayout()

        rgb_log_group = QGroupBox("RGB System Log")
        rgb_log_layout = QVBoxLayout()

        rgb_log_output = QTextEdit()
        rgb_log_output.setReadOnly(True)
        rgb_log_output.append("[INFO] RGB Camera Ready")

        rgb_log_layout.addWidget(rgb_log_output)
        rgb_log_group.setLayout(rgb_log_layout)



        rgb_layout.addWidget(rgb_settings_group)
        rgb_layout.addWidget(rgb_log_group)

        # =========================================================
        # 3D CAMERA TAB
        # =========================================================
        depth_tab = QWidget()
        depth_layout = QVBoxLayout(depth_tab)

        depth_settings_group = QGroupBox("3D Camera Settings")
        depth_settings_layout = QFormLayout()

        depth_exposure_slider = QSlider(Qt.Horizontal)
        depth_gain_slider = QSlider(Qt.Horizontal)
        depth_brightness_slider = QSlider(Qt.Horizontal)

        depth_settings_layout.addRow("Depth Exposure", depth_exposure_slider)
        depth_settings_layout.addRow("Depth Gain", depth_gain_slider)
        depth_settings_layout.addRow("Depth Brightness", depth_brightness_slider)

        depth_settings_group.setLayout(depth_settings_layout)

        depth_log_group = QGroupBox("3D Camera Log")
        depth_log_layout = QVBoxLayout()

        depth_log_output = QTextEdit()
        depth_log_output.setReadOnly(True)
        depth_log_output.append("[INFO] 3D Camera Ready")

        depth_log_layout.addWidget(depth_log_output)
        depth_log_group.setLayout(depth_log_layout)

        depth_layout.addWidget(depth_settings_group)
        depth_layout.addWidget(depth_log_group)
        # =========================================================
        # 2D + 3D TAB
        # =========================================================
        fusion_tab = QWidget()
        fusion_layout = QVBoxLayout(fusion_tab)

        fusion_group = QGroupBox("2D + 3D Fusion Settings")
        fusion_settings = QFormLayout()

        fusion_alpha_slider = QSlider(Qt.Horizontal)
        fusion_depth_slider = QSlider(Qt.Horizontal)

        fusion_settings.addRow("Fusion Alpha", fusion_alpha_slider)
        fusion_settings.addRow("Depth Scale", fusion_depth_slider)

        fusion_group.setLayout(fusion_settings)

        fusion_log = QTextEdit()
        fusion_log.setReadOnly(True)
        fusion_log.append("[INFO] 2D + 3D Fusion Mode Ready")

        fusion_layout.addWidget(fusion_group)
        fusion_layout.addWidget(fusion_log)

        # ==================================
        # ADD TABS
        # ==================================
        tabs.addTab(rgb_tab, "RGB Camera")
        tabs.addTab(depth_tab, "3D Camera")
        tabs.addTab(fusion_tab, "2D + 3D")

        # ==================================
        # ADD TAB WIDGET TO RIGHT PANEL
        # ==================================
        right_layout.addWidget(tabs)

        # ==================================
        # ADD TO SPLITTER
        # ==================================
        splitter.addWidget(center_panel)
        splitter.addWidget(right_panel)

        splitter.setSizes([250, 1000, 300])

        main_layout.addWidget(splitter)


if __name__ == "__main__":
    app = QApplication(sys.argv)

    window = MainWindow()
    window.show()

    sys.exit(app.exec())
