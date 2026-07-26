import os
import json

from PyQt6.QtWidgets import QApplication, QWidget, QLabel, QMenu
from PyQt6.QtCore import Qt, QSize
from PyQt6.QtGui import QMovie
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
SETTINGS_FILE = os.path.join(BASE_DIR, "settings.json")


def load_position():
    if os.path.exists(SETTINGS_FILE):
        with open(SETTINGS_FILE, "r") as file:
            return json.load(file)

app = QApplication([])

pet_size = 200
screen = app.primaryScreen()
geometry = screen.geometry()

screen_width = geometry.width()
screen_height = geometry.height()

class PetWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.drag_position = None
    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.drag_position = event.globalPosition().toPoint()
    
    def mouseMoveEvent(self, event):
        if self.drag_position:
            difference = event.globalPosition().toPoint() - self.drag_position
            self.move(self.pos() + difference)
            
            save_position(self.x(), self.y())
            
            self.drag_position = event.globalPosition().toPoint()
    
    def mouseReleaseEvent(self, event):
        self.drag_position = None

    def quit_pet(self):
        self.close()
    def contextMenuEvent(self, event):
        menu = QMenu(self)

        quit_action = menu.addAction("Quit")

        action = menu.exec(event.globalPos())

        if action == quit_action:
            self.quit_pet()

window = PetWindow()
window.resize(pet_size, pet_size)

window.setWindowTitle("Snorlax Companion")
window.setWindowFlags(Qt.WindowType.FramelessWindowHint)
window.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)


label = QLabel(window)
label.move (0, 0)
label.resize(pet_size, pet_size)

gif_path = os.path.join(BASE_DIR, "assets", "snorlax.gif")
movie = QMovie(gif_path)
movie.setScaledSize(QSize(pet_size, pet_size))

label.setMovie(movie)
movie.start()

saved_position = load_position()

def save_position(x, y):
    with open (SETTINGS_FILE, "w") as file:
        json.dump(
            {
                "x": x,
                "y": y
            },
            file
        )

if saved_position:
    window.move(
        saved_position["x"],
        saved_position["y"]
    )
else:
    window.move(
        (screen_width - pet_size) // 2,
        screen_height - 250
    )

window.show()

app.exec()


