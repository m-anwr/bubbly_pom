from PyQt5.QtCore import QObject, pyqtSlot, pyqtSignal, QTimer
from enum import Enum


class TimerType(Enum):
    Pom = 0
    ShortBrk = 1
    LongBrk = 2


class Timer(QObject):
    notify = pyqtSignal(str, int)
    notify_progress = pyqtSignal(int, int, int)

    def __init__(self, pom_dur, short_dur, long_dur, long_freq):
        QObject.__init__(self)

        self.pom_dur = pom_dur
        self.short_dur = short_dur
        self.long_dur = long_dur
        self.long_freq = long_freq

        self.timer = QTimer()
        self.timer.setSingleShot(True)
        self.timer.timeout.connect(self.next)

        self.notification_timer = QTimer()
        self.notification_timer.timeout.connect(self.send_progress)

        self.curr_timer_type = TimerType.Pom
        self.finished_poms = 0

    def send_progress(self):
        #print(f"Send progress: [{self.curr_timer_type} {self.pom_dur} {self.short_dur} {self.long_dur}] {self.timer.remainingTime()}")
        remaining_time = self.timer.remainingTime()
        mins = (remaining_time / 1000) // 60
        secs = (remaining_time / 1000) % 60
        self.notify_progress.emit(mins, secs, (remaining_time/self.timer.interval())*100)

    @pyqtSlot()
    def start(self):
        if self.curr_timer_type == TimerType.Pom:
            self.timer.start(self.pom_dur * 60 * 1000)
            self.notify.emit("Pomodoro", self.pom_dur )
        elif self.curr_timer_type == TimerType.ShortBrk:
            self.timer.start(self.short_dur * 60 * 1000)
            self.notify.emit("Short Break", self.short_dur)
        elif self.curr_timer_type == TimerType.LongBrk:
            self.timer.start(self.long_dur * 60 * 1000)
            self.notify.emit("Long Break", self.long_dur)

        self.notification_timer.start(1000)

    @pyqtSlot()
    def stop(self):
        print("stop")
        self.timer.stop()
        self.notification_timer.stop()

    @pyqtSlot()
    def next(self):
        if self.curr_timer_type == TimerType.Pom:
            self.finished_poms += 1
            if self.finished_poms == self.long_freq:
                self.finished_poms = 0
                self.curr_timer_type = TimerType.LongBrk
            else:
                self.curr_timer_type = TimerType.ShortBrk
        elif self.curr_timer_type == TimerType.ShortBrk:
            self.curr_timer_type = TimerType.Pom
        elif self.curr_timer_type == TimerType.LongBrk:
            self.curr_timer_type = TimerType.Pom

        self.timer.stop()
        self.start()

    @pyqtSlot(int)
    def pom_dur_changed(self, new_dur):
        self.pom_dur = new_dur

    @pyqtSlot(int)
    def short_dur_changed(self, new_dur):
        self.short_dur = new_dur

    @pyqtSlot(int)
    def long_dur_changed(self, new_dur):
        self.long_dur = new_dur

    @pyqtSlot(int)
    def long_freq_changed(self, new_freq):
        self.long_freq = new_freq