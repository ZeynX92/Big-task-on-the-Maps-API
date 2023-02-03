import sys
import requests
from PyQt5 import uic
from PyQt5.QtGui import QPixmap
from PyQt5 import QtGui
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QMainWindow


class MyWidget(QMainWindow):
    def __init__(self):
        self.lat, self.lon = float(input("Lat: ")), float(input("Lon: "))
        self.z = int(input("Введите уровень масшабирования: "))

        super().__init__()
        uic.loadUi('UI.ui', self)
        self.pushButton.clicked.connect(self.change_perspective)

        self.image = None
        self.perspectives = ["map", "sat", "sat,skl"]
        self.current_perspective = 0
        self.update_map()

    def update_map(self):
        response = requests.get(
            f"https://static-maps.yandex.ru/1.x/?ll={self.lat},{self.lon}&z={self.z}&l={self.perspectives[self.current_perspective]}")

        map_file = "map.png"
        with open(map_file, "wb") as file:
            file.write(response.content)

        self.image = QPixmap("map.png").scaled(681, 481)
        self.label.setPixmap(self.image)

    def mousePressEvent(self, event):
        try:
            QApplication.focusWidget().clearFocus()
        except AttributeError:
            pass

    def keyPressEvent(self, event):
        print("HERE_UYTRTE")
        print(event.key())
        if event.key() == Qt.Key_PageUp:
            if 0 <= self.z < 17:
                self.label_2.setText("")
                self.z += 1
            else:
                self.label_2.setText("Максимальный масштаб!")
        elif event.key() == Qt.Key_PageDown:
            if 0 < self.z <= 17:
                self.label_2.setText("")
                self.z -= 1
            else:
                self.label_2.setText("Минимальный масштаб!")
        elif event.key() == Qt.Key_Up:
            self.lon += 0.05 * (17 - self.z)
        elif event.key() == Qt.Key_Down:
            self.lon -= 0.05 * (17 - self.z)
        elif event.key() == Qt.Key_Left:
            print("HERE")
            self.lat += 0.05 * (17 - self.z)
        elif event.key() == Qt.Key_Right:
            print("here")
            self.lat -= 0.05 * (17 - self.z)
        self.update_map()

    def change_perspective(self):
        self.current_perspective += 1
        self.current_perspective %= 3
        self.update_map()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyWidget()
    ex.show()
    sys.exit(app.exec_())
