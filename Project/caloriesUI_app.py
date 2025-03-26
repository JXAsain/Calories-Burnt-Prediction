import sys
from PyQt6.QtWidgets import QApplication, QWidget, QLabel, QVBoxLayout, QPushButton, QLineEdit, QComboBox, QMessageBox
import modelFile

class CaloriePredictor(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
    
    def initUI(self):
        self.setWindowTitle("🔥 Calorie Burnt Prediction App 🔥")
        self.setGeometry(100, 100, 400, 300)

        layout = QVBoxLayout()

        # Input Fields
        self.ageInput = QLineEdit(self)
        self.ageInput.setPlaceholderText("Enter Age Here")
        layout.addWidget(QLabel("Age:"))
        layout.addWidget(self.ageInput)

        self.genderInput = QComboBox(self)
        self.genderInput.addItems(["Select Gender Here", "Male", "Female"])
        layout.addWidget(QLabel("Gender:"))
        layout.addWidget(self.genderInput)

        self.heightInput = QLineEdit(self)
        self.heightInput.setPlaceholderText("Enter Height Here")
        layout.addWidget(QLabel("Height (cm):"))
        layout.addWidget(self.heightInput)

        self.heartRateInput = QLineEdit(self)
        self.heartRateInput.setPlaceholderText("Enter Heart Rate Here")
        layout.addWidget(QLabel("Heart Rate (bpm):"))
        layout.addWidget(self.heartRateInput)

        self.bodyTempInput = QLineEdit(self)
        self.bodyTempInput.setPlaceholderText("Enter Body Temperature Here")
        layout.addWidget(QLabel("Body Temperature (°C):"))
        layout.addWidget(self.bodyTempInput)

        # Prediction Button
        self.predictButton = QPushButton("🚨 CALORIE PREDICTION", self)
        self.predictButton.clicked.connect(self.predictCalories)
        layout.addWidget(self.predictButton)

        # Result Label
        self.resultLabel = QLabel("", self)
        layout.addWidget(self.resultLabel)

        self.setLayout(layout)
    
    def predictCalories(self):
        # When Button is Clicked it Processes User Input
        age = int(self.ageInput.text())
        gender = self.genderInput.currentText()
        height = int(self.heightInput.text())
        heart_rate = int(self.heartRateInput.text())
        body_temp = float(self.bodyTempInput.text())

        if gender == "Select Gender Here":
            QMessageBox.warning(self, "Input Error", "⚠️ Please select a valid gender ⚠️")
            return
        
        # Limiter Control Here
        if not (0 <= age <= 130):
            QMessageBox.warning(self, "Input Error", "⚠️ Age must be between 0 and 130 years ⚠️")
            return
        
        if not (1 <= height <= 275):
            QMessageBox.warning(self, "Input Error", "⚠️ Height must be between 1 and 275 cm ⚠️")
            return
        
        if not (20 <= heart_rate <= 220):
            QMessageBox.warning(self, "Input Error", "⚠️ Heart rate must be between 20 and 220 bpm ⚠️")
            return
        
        if not (35.0 <= body_temp <= 42.0):
            QMessageBox.warning(self, "Input Error", "⚠️ Body temperature must be between 35.0 and 42.0 °C ⚠️")
            return
        
        try:
            userData = {
                "age": int(age),
                "gender": gender,
                "height": int(height),
                "heart": int(heart_rate),
                "bodyTemp": float(body_temp)
            }
            predictedCalories = modelFile.run(userData)
            self.resultLabel.setText(f"🔥 Estimated Calories Burnt: {predictedCalories[0]:.2f} kcal 🔥")
        
        except ValueError:
            QMessageBox.warning(self, "Input Error", "⚠️ Please enter valid numerical values. ⚠️")

        except Exception as e:
            QMessageBox.critical(self, "Prediction Error", f"⚠️ Failed to retrieve your prediction ⚠️\n{str(e)}")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = CaloriePredictor()
    window.show()
    sys.exit(app.exec())
