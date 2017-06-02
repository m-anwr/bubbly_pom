from datetime import time

from PyQt5.QtWidgets import QDialog
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import pyqtSlot, pyqtSignal
from bubbly_pom.note_form import Ui_Dialog
from bubbly_pom import resources
import bubbly_pom.bubbly_pom_globals as bpg
import json, os, datetime


class NoteManager(QDialog, Ui_Dialog):
    new_note_added = pyqtSignal(str, str)
    refresh_table = pyqtSignal()

    def __init__(self):
        QDialog.__init__(self)
        self.setupUi(self)
        self.setWindowIcon(QIcon(":/lollipop_ico"))
        self.save_note_btn.clicked.connect(self.save_note)

        with open(os.path.join(bpg.user_app_folder_path, bpg.notes_list_file)) as f:
            self.notes_list = json.loads(f.read())

        self.timestamp = None

    @pyqtSlot()
    def show_existing(self, title, timestamp):
        self.note_title.setText(title)
        self.timestamp = timestamp
        with open(os.path.join(bpg.notes_folder_path, self.timestamp), "r+") as f:
            self.note_body.setText(f.read())

        self.show()

    @pyqtSlot()
    def save_note(self):
        self.hide()

        if self.timestamp is None:
            self.timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S %p")

            data_dict = {
                "title": self.note_title.text(),
                "date": self.timestamp
            }
            self.notes_list.append(data_dict)

            self.new_note_added.emit(self.note_title.text(), self.timestamp)
        else:
            item = list(filter(lambda n: n['date'] == self.timestamp, self.notes_list))[0]
            new_item = item.copy()
            new_item["title"] = self.note_title.text()
            self.notes_list.remove(item)
            self.notes_list.append(new_item)

        with open(os.path.join(bpg.notes_folder_path, self.timestamp), "w+") as f:
            f.seek(0)
            f.write(self.note_body.toPlainText())
            f.truncate()

        self.save_all()
        self.refresh_table.emit()
        self.timestamp = None

    @pyqtSlot()
    def show_new(self):
        self.note_title.setText("")
        self.note_body.setText("")
        self.show()

    def save_all(self):
        print("Saving Notes Data")
        with open(os.path.join(bpg.user_app_folder_path, bpg.notes_list_file), "r+") as f:
            f.seek(0)
            f.write(json.dumps(self.notes_list))
            f.truncate()

    def reject(self):
        self.timestamp = None
        QDialog.reject(self)

    def delete_note(self, timestamp):
        item = list(filter(lambda n: n['date'] == timestamp, self.notes_list))[0]
        self.notes_list.remove(item)
