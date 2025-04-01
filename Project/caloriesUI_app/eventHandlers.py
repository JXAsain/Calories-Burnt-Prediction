from PyQt6.QtWidgets import QMessageBox, QFileDialog, QSizePolicy
from caloriesUI_app.elementsUI import CaloriePredictor


# Processes User Input
def predictCalories(self):
    import modelFile

    age = int(self.ageInput.text())
    gender = self.genderInput.currentText()
    height = int(float(self.heightInput.text()))
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
        self.userData = {
            "age": int(age),
            "gender": gender,
            "height": int(height),
            "heart": int(heart_rate),
            "bodyTemp": float(body_temp)
        }

        # Run the prediction (returns only calories)
        predicted = modelFile.run(self.userData)
        predicted_value = float(predicted[0])
        self.userData["calories"] = predicted_value  # For plot toggle

        # Get percentile separately using calories
        percentile = modelFile.percentile("Calories", predicted_value)

        # Display results
        self.resultLabel.setText(f"🔥 Estimated Calories Burnt: {predicted_value:.2f} kcal 🔥")
        self.percentileLabel.setText(f"🏅 Percentile Ranking: {percentile}% 🏅")

        # Show user's plot (from toggle selection)
        self.renderPlot(True)

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
    
    if hasattr(self, 'multiFigureGroupCanvas'):
        self.contentLayout.removeWidget(self.multiFigureGroupCanvas)
        self.multiFigureGroupCanvas.deleteLater()
        del self.multiFigureGroupCanvas


# Sends File and Display Results (Both CSV & User)
def renderPlot(self, userInput=False):
    import modelFile

    try:
        if userInput:
            if not hasattr(self, 'userData') or 'calories' not in self.userData:
                return

            # Toggle for User Plot
            if self.plotToggleButton.isChecked():
                plots = modelFile.userdata_compare_statter(self.userData)
            else:
                plots = modelFile.userdata_compare_histogram(self.userData)

        else:
            if not hasattr(self, 'csvPath'):
                QMessageBox.warning(self, "No File", "⚠️ Please upload a CSV file first. ⚠️")
                return

            # Toggle for CSV Plot
            if self.plotToggleButton.isChecked():
                plots = modelFile.received_csv_data_scatter(self.csvPath)
            else:
                plots = modelFile.received_csv_data_histogram(self.csvPath)

        # Replace Previous Group Based on Context if Any
        if hasattr(self, 'multiFigureGroupCanvas'):
            self.contentLayout.removeWidget(self.multiFigureGroupCanvas)
            self.multiFigureGroupCanvas.deleteLater()
            del self.multiFigureGroupCanvas

        groupContainer = buildPlotGroup(plots)

        self.multiFigureGroupCanvas = groupContainer
        self.contentLayout.addWidget(self.multiFigureGroupCanvas)

    except Exception as e:
        QMessageBox.critical(self, "Processing Error", f"⚠️ Could not render plot:\n{str(e)} ⚠️")


# Build New Group Layout
def buildPlotGroup(plots: dict):
    from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
    from PyQt6.QtWidgets import QHBoxLayout, QLabel, QWidget, QVBoxLayout, QSizePolicy
    from PyQt6.QtCore import Qt

    groupLayout = QVBoxLayout()
            
    for desc, fig in plots.items():
        canvas = FigureCanvas(fig)
        canvas.setMinimumHeight(canvas.sizeHint().height())
        canvas.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        canvas.updateGeometry()
        canvas.draw()

        label = QLabel(desc)
        label.setWordWrap(True)
        label.setMinimumWidth(300)
        label.setAlignment(Qt.AlignmentFlag.AlignVCenter)
        label.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Preferred)

        # Bold Text and Draws Box
        label.setStyleSheet("""
            QLabel {
                font-weight: bold;
                font-size: 14px;
                color: #333333;
                border: 1px solid #555;
                padding: 8px;
                border-radius: 6px;
                background-color: #f5f5f5;
            }
        """)

        rowLayout = QHBoxLayout()
        rowLayout.addWidget(canvas, 3)
        rowLayout.addSpacing(10)
        rowLayout.addWidget(label, 2)

        rowWidget = QWidget()
        rowWidget.setLayout(rowLayout)

        groupLayout.addSpacing(10)
        groupLayout.addWidget(rowWidget)

    groupContainer = QWidget()
    groupContainer.setLayout(groupLayout)
    return groupContainer
   

# Updates Toggled Button Label
def togglePlotType(self):
    if self.plotToggleButton.isChecked():
        self.plotToggleButton.setText("View: Scatter Plot")
    else:
        self.plotToggleButton.setText("View: Histogram")
        
    # Re-render CSV Plot if Loaded
    if hasattr(self, 'csvPath'):
        self.renderPlot(False)
        
    # Re-render User Plot if Available
    if hasattr(self, 'userData') and 'calories' in self.userData:
        self.renderPlot(True)


def extend_caloriesPredictor():
    CaloriePredictor.predictCalories = predictCalories
    CaloriePredictor.selectFile = selectFile
    CaloriePredictor.renderPlot = renderPlot
    CaloriePredictor.togglePlotType = togglePlotType
