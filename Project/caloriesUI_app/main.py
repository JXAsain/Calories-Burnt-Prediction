import sys
from PyQt6.QtWidgets import QApplication
from caloriesUI_app.elementsUI import CaloriePredictor
from caloriesUI_app.eventHandlers import extend_caloriesPredictor

if __name__ == "__main__":
    extend_caloriesPredictor()
    app = QApplication(sys.argv)
    window = CaloriePredictor()
    window.show()
    sys.exit(app.exec())
