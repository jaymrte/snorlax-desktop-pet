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
resize_margin = 50
screen = app.primaryScreen()
geometry = screen.geometry()

screen_width = geometry.width()
screen_height = geometry.height()

class PetWindow(QWidget):
    def __init__(self):
        super().__init__()
        
        self.drag_position = None
        self.resizing = False
        
        self.label = QLabel(self)
        self.label.move (0, 0)
        self.label.resize(pet_size, pet_size)

        gif_path = os.path.join(BASE_DIR, "assets", "snorlax.gif")
        
        self.movie = QMovie(gif_path)
        self.movie.setScaledSize(QSize(pet_size, pet_size))

        self.label.setMovie(self.movie)
        self.movie.start()
        
    
    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            
            if (
                event.position().x() > self.width() - resize_margin
                and event.position().y() > self.height() - resize_margin
            ):
                print("RESIZE MODE")
                self.resizing = True
                self.resize_start = event.globalPosition().toPoint()
                self.start_size = self.size()

            else:
                self.drag_position = event.globalPosition().toPoint()
    
    def mouseMoveEvent(self, event):
        
        if self.resizing:
            difference = event.globalPosition().toPoint() - self.resize_start

            new_width = self.start_size.width() + difference.x()
            new_height = self.start_size.height() + difference.y()

            if new_width > 50 and new_height > 50:
                self.resize(new_width, new_height)
            
        elif self.drag_position:
           difference = event.globalPosition().toPoint() - self.drag_position
           self.move(self.pos() + difference)
            
           save_position(self.x(), self.y())
            
           self.drag_position = event.globalPosition().toPoint()
    
    def mouseReleaseEvent(self, event):
        self.drag_position = None
        self.resizing = False

    def resizeEvent(self, event):
        new_size = self.size()

        self.label.resize(new_size)
        self.movie.setScaledSize(new_size)

        self.movie.stop()
        self.movie.start()

        super().resizeEvent(event)
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

def save_position(x, y):
    with open (SETTINGS_FILE, "w") as file:
        json.dump(
            {
                "x": x,
                "y": y
            },
            file
        )

saved_position = load_position()

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


