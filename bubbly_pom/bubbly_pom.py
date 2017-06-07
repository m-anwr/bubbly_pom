# PyQt imports
from PyQt5.QtWidgets import QMainWindow, QSystemTrayIcon, QAction, QMenu, \
    QSplashScreen, QHeaderView, QTableWidgetItem, QAbstractItemView
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtCore import pyqtSlot, QCoreApplication, Qt

# Local imports
from bubbly_pom.bubbly_pom_ui import Ui_MainWindow
from bubbly_pom import resources
from bubbly_pom.user_data import UserData
from bubbly_pom.timer import Timer
from bubbly_pom.note_manager import NoteManager
from bubbly_pom.wizard_ui import AboutWizard


class BubblyPom(QMainWindow, Ui_MainWindow):
    def __init__(self):
        QMainWindow.__init__(self)

        self.show_splash()
        self.init_ui()
        self.fetch_settings()
        self.init_tray_icon()
        self.init_timer()
        self.init_note()
        self.about_wiz = AboutWizard()
        self.init_connection()
        self.clear_progress()

    def show_splash(self):
        splash = QSplashScreen(QPixmap(":/splash"))
        splash.setWindowFlags(Qt.FramelessWindowHint)
        splash.setAttribute(Qt.WA_TranslucentBackground, True)
        splash.show()
        splash.finish(self)

    def fetch_settings(self):
        self.user_data = UserData()
        self.timer_settings = self.user_data.fetch_timer_settings()

        self.pom_dial.setValue(self.timer_settings["pomodoro_duration"])
        self.pom_dur_lcd.display(self.timer_settings["pomodoro_duration"])

        self.short_brk_dial.setValue(self.timer_settings["short_break_duration"])
        self.short_brk_lcd.display(self.timer_settings["short_break_duration"])

        self.long_brk_dial.setValue(self.timer_settings["long_break_duration"])
        self.long_brk_lcd.display(self.timer_settings["long_break_duration"])

        self.long_brk_freq_dial.setValue(self.timer_settings["long_break_frequency"])
        self.long_brk_freq_lcd.display(self.timer_settings["long_break_frequency"])

    def init_ui(self):
        self.setupUi(self)
        self.tabWidget.tabBar().hide()

        self.setWindowIcon(QIcon(":/lollipop_ico"))

        self.timer_tab_btn.setIcon(QIcon(":/timer_ico"))
        self.notes_tab_btn.setIcon(QIcon(":/note_ico"))
        self.pinterest_tab_btn.setIcon(QIcon(":/pinterest_ico"))
        self.soundcloud_tab_btn.setIcon(QIcon(":/soundcloud_ico"))

        self.notes_table.setHorizontalHeaderLabels(["Title", "Date"])
        self.notes_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.notes_table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.notes_table.setSelectionBehavior(QAbstractItemView.SelectRows)

        self.pinterest_tab_btn.setDisabled(True)
        self.pinterest_tab_btn.setToolTip("Pinterest: Coming soon...")
        self.soundcloud_tab_btn.setDisabled(True)
        self.soundcloud_tab_btn.setToolTip("Soundcloud: Coming soon...")


    def init_tray_icon(self):
        self.current_timer_action = QAction("Timer Stopped", self)
        self.current_timer_action.setDisabled(True)
        self.start_timer_action = QAction("Start timer", self)
        self.stop_timer_action = QAction("Stop timer", self)
        self.next_timer_action = QAction("Next timer", self)

        self.new_note_action = QAction("New note/idea", self)

        self.restore_action = QAction("Show Main Window", self)

        self.about_action = QAction("About ;)", self)
        self.quit_action = QAction("Quit", self)

        tray_icon_menu = QMenu(self)
        tray_icon_menu.addAction(self.current_timer_action)
        tray_icon_menu.addAction(self.start_timer_action)
        tray_icon_menu.addAction(self.stop_timer_action)
        tray_icon_menu.addAction(self.next_timer_action)
        tray_icon_menu.addSeparator()
        tray_icon_menu.addAction(self.new_note_action)
        tray_icon_menu.addSeparator()
        tray_icon_menu.addAction(self.restore_action)
        tray_icon_menu.addSeparator()
        tray_icon_menu.addAction(self.about_action)
        tray_icon_menu.addAction(self.quit_action)

        self.tray_icon = QSystemTrayIcon(QIcon(':/lollipop_ico'), self)
        self.tray_icon.setContextMenu(tray_icon_menu)
        self.tray_icon.show()



    def init_timer(self):
        self.timer = Timer(
            self.pom_dial.value(),
            self.short_brk_dial.value(),
            self.long_brk_dial.value(),
            self.long_brk_freq_dial.value()
        )

    def init_note(self):
        if not hasattr(self, "note_manager"):
            self.note_manager = NoteManager()

        for n in self.note_manager.notes_list:
            self.notes_table.insertRow(self.notes_table.rowCount())
            self.notes_table.setItem(
                self.notes_table.rowCount() - 1,
                0,
                QTableWidgetItem(n["title"])
            )
            self.notes_table.setItem(
                self.notes_table.rowCount() - 1,
                1,
                QTableWidgetItem(n["date"])
            )

    def init_connection(self):
        self.timer_tab_btn.clicked.connect(self.change_tab)
        self.notes_tab_btn.clicked.connect(self.change_tab)
        self.pinterest_tab_btn.clicked.connect(self.change_tab)
        self.soundcloud_tab_btn.clicked.connect(self.change_tab)

        self.restore_action.triggered.connect(self.show)
        self.tray_icon.activated.connect(self.show)
        self.quit_action.triggered.connect(self.quit)
        self.actionExit.triggered.connect(self.quit)

        self.pom_dial.valueChanged[int].connect(self.timer.pom_dur_changed)
        self.short_brk_dial.valueChanged[int].connect(self.timer.short_dur_changed)
        self.long_brk_dial.valueChanged[int].connect(self.timer.long_dur_changed)
        self.long_brk_freq_dial.valueChanged[int].connect(self.timer.long_freq_changed)

        self.start_timer_action.triggered.connect(self.timer.start)
        self.start_timer_btn.clicked.connect(self.timer.start)

        self.next_timer_action.triggered.connect(self.timer.next)
        self.next_timer_btn.clicked.connect(self.timer.next)

        self.stop_timer_action.triggered.connect(self.timer.stop)
        self.stop_timer_btn.clicked.connect(self.timer.stop)

        self.stop_timer_action.triggered.connect(self.clear_progress)
        self.stop_timer_btn.clicked.connect(self.clear_progress)

        self.timer.notify.connect(self.show_notification)
        self.timer.notify_progress.connect(self.update_progress)

        self.add_note_btn.clicked.connect(self.note_manager.show_new)
        self.new_note_action.triggered.connect(self.note_manager.show_new)
        self.note_manager.new_note_added.connect(self.add_new_note)
        self.note_manager.refresh_table.connect(self.reconstruct_notes_table)

        self.notes_table.cellDoubleClicked.connect(self.show_note)
        self.notes_table.itemSelectionChanged.connect(self.enable_delete_btn)
        self.delete_note_btn.clicked.connect(self.delete_note)

        self.about_action.triggered.connect(self.about_wiz.show)
        self.actionAbout.triggered.connect(self.about_wiz.show)

    @pyqtSlot()
    def enable_delete_btn(self):
        cond = len(self.notes_table.selectedItems()) > 0
        self.delete_note_btn.setEnabled(cond)

    @pyqtSlot()
    def delete_note(self):
        for i in self.notes_table.selectedItems():
            if i.column() == 1:
                self.note_manager.delete_note(i.text())

        self.reconstruct_notes_table()

    @pyqtSlot()
    def reconstruct_notes_table(self):
        self.notes_table.setRowCount(0)
        self.init_note()

    @pyqtSlot(str, str)
    def add_new_note(self, title, date):
        self.notes_table.insertRow(self.notes_table.rowCount())
        self.notes_table.setItem(
            self.notes_table.rowCount() - 1,
            0,
            QTableWidgetItem(title)
        )
        self.notes_table.setItem(
            self.notes_table.rowCount() - 1,
            1,
            QTableWidgetItem(date)
        )

    @pyqtSlot(int, int)
    def show_note(self, row, col):
        title = self.notes_table.item(row, 0).text()
        timestamp = self.notes_table.item(row, 1).text()
        self.note_manager.show_existing(title, timestamp)

    @pyqtSlot()
    def clear_progress(self):
        self.curr_timer_progress.setValue(100)
        self.current_timer_action.setText("Timer Stopped")

    @pyqtSlot(int, int, int)
    def update_progress(self, mins, secs, progress):
        self.curr_timer_progress.setValue(progress)
        self.current_timer_action.setText(
            "Remaining: {}:{}".format(mins, secs)
        )

    @pyqtSlot(str, int)
    def show_notification(self, timer_type, timer_dur):
        self.tray_icon.showMessage(
            "BubblyPom: {}".format(timer_type),
            "Duration: {} min".format(timer_dur),
            QSystemTrayIcon.Information, 5000
        )

    @pyqtSlot()
    def change_tab(self):
        if self.sender() == self.timer_tab_btn:
            self.tabWidget.setCurrentIndex(0)
        elif self.sender() == self.notes_tab_btn:
            self.tabWidget.setCurrentIndex(1)
        elif self.sender() == self.pinterest_tab_btn:
            self.tabWidget.setCurrentIndex(2)
        else:
            self.tabWidget.setCurrentIndex(3)

    @pyqtSlot()
    def quit(self):
        self.timer_settings["pomodoro_duration"] = self.pom_dial.value()
        self.timer_settings["short_break_duration"] = self.short_brk_dial.value()
        self.timer_settings["long_break_duration"] = self.long_brk_dial.value()
        self.timer_settings["long_break_frequency"] = self.long_brk_freq_dial.value()
        self.user_data.save_timer_settings(self.timer_settings)
        self.note_manager.save_all()
        QCoreApplication.instance().quit()