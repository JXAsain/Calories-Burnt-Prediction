import sys
from PyQt6.QtWidgets import QApplication, QWidget, QLabel, QFrame, QVBoxLayout, QHBoxLayout, QPushButton, QLineEdit, QComboBox, QMessageBox, QFileDialog
from PyQt6.QtGui import QPixmap


class CaloriePredictor(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
    
    # UI Formate
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
        self.predictButton = QPushButton("🚨 Calorie Prediction", self)
        self.predictButton.clicked.connect(self.predictCalories)
        layout.addWidget(self.predictButton)

        # Placeholder for the Prediction Calories
        self.resultLabel = QLabel("", self)
        layout.addWidget(self.resultLabel)

        # Placeholder for the Percentile Value
        self.percentileLabel = QLabel("", self)
        layout.addWidget(self.percentileLabel)

        # Placeholder for the Prediction Plot
        self.plotLabel = QLabel(self)
        layout.addWidget(self.plotLabel)

        # Pixel Padding and Divider Line
        layout.addSpacing(10)
        divider = QFrame()
        divider.setFrameShape(QFrame.Shape.HLine)
        divider.setFrameShadow(QFrame.Shadow.Sunken)
        layout.addWidget(divider)
        layout.addSpacing(10)

        # Upload File Section
        uploadRow = QHBoxLayout()

        self.uploadButton = QPushButton("📁 Upload CSV", self)
        self.uploadButton.setFixedWidth(150)
        self.uploadButton.clicked.connect(self.selectFile)

        # Shows Filename after Upload
        self.csvLoadedLabel = QLabel("")

        uploadRow.addWidget(self.csvLoadedLabel)
        uploadRow.addStretch()
        uploadRow.addWidget(self.uploadButton)

        layout.addLayout(uploadRow)

        self.processButton = QPushButton("⚙️ Process CSV Data", self)
        self.processButton.clicked.connect(self.processData)
        layout.addWidget(self.processButton)

        # Placeholder for the Group Prediction Plot
        self.csvPlotLabel = QLabel(self)
        layout.addWidget(self.csvPlotLabel)

        self.setLayout(layout)


    # Processes User Input
    def predictCalories(self):
        from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
        from matplotlib.figure import Figure
        import modelFile

        age = int(self.ageInput.text())
        gender = self.genderInput.currentText()
        height = int(self.heightInput.text())
        heart_rate = int(self.heartRateInput.text())
        body_temp = float(self.bodyTempInput.text())

        if gender == "Select Gender Here":
            QMessageBox.warning(self, "Input Error", "⚠️ Please select a valid gender ⚠️")
            return
        
        # Limiter Control
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
            
            results = modelFile.run(userData)

            # Backend Returns (calories, percentile, figure)
            if isinstance(results, tuple) and len(results) == 3:
                predictedCalories, percentile, fig = results

                self.resultLabel.setText(f"🔥 Estimated Calories Burnt: {predictedCalories:.2f} kcal 🔥")
                self.percentileLabel.setText(f"🏅 Percentile Ranking: {percentile} % 🏅")

                # Rendering Plot in UI (Expecting a Matplotlib Figure)
                layout = self.layout()
                layout.removeWidget(self.plotLabel)
                self.plotLabel.deleteLater()

                canvas = FigureCanvas(fig)
                canvas.setFixedSize(400, 300)
                self.plotLabel = canvas
                layout.addWidget(self.plotLabel)

            else:
                QMessageBox.warning(self, "Backend Error", "⚠️ Unexpected response from the backend. ⚠️")
        
        except ValueError:
            QMessageBox.warning(self, "Input Error", "⚠️ Please enter valid numerical values. ⚠️")

        except Exception as e:
            QMessageBox.critical(self, "Prediction Error", f"⚠️ Failed to retrieve your prediction ⚠️\n{str(e)}")


    # Opens File
    def selectFile(self):
        fileDialog = QFileDialog()
        filePath, _ = fileDialog.getOpenFileName(self, "Select CSV File", "", "CSV Files (*.csv)")
        
        if filePath:
            self.csvPath = filePath
            self.csvLoadedLabel.setText(f"✅ {filePath.split('/')[-1]}")


    # Sends File and Display Results
    def processData(self):
        from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
        from matplotlib.figure import Figure
        import modelFile

        if not hasattr(self, 'csvPath'):
            QMessageBox.warning(self, "No File", "⚠️ Please upload a CSV file first. ⚠️")
            return
        
        try:
            # Expecting a Matplotlib Figure
            fig = modelFile.process_csv(self.csvPath)
            
            if isinstance(fig, Figure):
                canvas = FigureCanvas(fig)
                canvas.draw()
                canvas.setFixedSize(400, 300)

                layout = self.layout()
                layout.removeWidget(self.csvPlotLabel)
                self.csvPlotLabel.deleteLater()
                self.csvPlotLabel = canvas
                layout.addWidget(self.csvPlotLabel)
            
            else:
                QMessageBox.warning(self, "Processing Error", "⚠️ Backend did not return a valid figure. ⚠️")
        
        except Exception as e:
            QMessageBox.critical(self, "Processing Error", f"⚠️ Could not process CSV:\n{str(e)} ⚠️")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = CaloriePredictor()
    window.show()
    sys.exit(app.exec())
