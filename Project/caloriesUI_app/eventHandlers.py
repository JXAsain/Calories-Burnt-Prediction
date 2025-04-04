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
                plots = {
                    "Age vs Calories Burned": {
                        "figure": modelFile.userdata_compare_statter(self.userData)["Age"],
                        "explanation": f"This scatter plot shows how you compare to others in your age group on calories burned. \n\nYou are in the {modelFile.percentile('Age', self.userData['age'])} percentile for age."
                    },
                    "Height vs Calories Burned": {
                        "figure": modelFile.userdata_compare_statter(self.userData)["Height"],
                        "explanation": f"This scatter plot shows how you compare to others in around your height group on calories burnt. \n\nYou are in the {modelFile.percentile('Height', self.userData['height'])} percentile for height. "
                    },
                    "Heart Rate vs Calories Burned": {
                        "figure": modelFile.userdata_compare_statter(self.userData)["Heart_Rate"],
                        "explanation": f"Higher heart rates generally lead to increased calorie burn. This scatter plot compares your heart rate and calories burned to 1000 others. \n\nYou are in the {modelFile.percentile('Heart_Rate', self.userData['heart'])} percentile for heart rate."
                    },
                    "Body Temperature vs Calories Burned": {
                        "figure": modelFile.userdata_compare_statter(self.userData)["Body_Temp"],
                        "explanation": f"This scatter plot visualizes the effect of body temperature on calorie burning. Your data point is highlighted in red. \n\nYou are in the {modelFile.percentile('Body_Temp', self.userData['bodyTemp'])} percentile for body temperature."
                    }
                }
            else:
                plots = {
                    "Age Distribution": {
                        "figure": modelFile.userdata_compare_histogram(self.userData)["Age"],
                        "explanation": f"This histogram shows the age distribution of users. Your age is marked in red. \n\nYou are in the {modelFile.percentile('Age', self.userData['age'])} percentile for age."
                    },
                    "Height Distribution": {
                        "figure": modelFile.userdata_compare_histogram(self.userData)["Height"],
                        "explanation": f"This histogram shows the height distribution of users. Your height is marked in red. \n\nYou are in the {modelFile.percentile('Height', self.userData['height'])} percentile for height."
                    },
                    "Heart Rate Distribution": {
                        "figure": modelFile.userdata_compare_histogram(self.userData)["Heart_Rate"],
                        "explanation": f"This histogram visualizes how your heart rate compares to other users. \n\nYou are in the {modelFile.percentile('Heart_Rate', self.userData['heart'])} percentile for heart rate."
                    },
                    "Body Temperature Distribution": {
                        "figure": modelFile.userdata_compare_histogram(self.userData)["Body_Temp"],
                        "explanation": f"This histogram displays the distribution of body temperatures among users. \n\nYou are in the {modelFile.percentile('Body_Temp', self.userData['bodyTemp'])} percentile for body temperature."
                    }
                }

            # modify explanations based on conditions
            for key, plot in plots.items():
                # age comment additions
                if "Age" in key:
                    user_age = self.userData['age']
                    if user_age > 40:
                        plot["explanation"] += "\n\nAt your age, you should consult your doctor before you continue exercising."
                # heart rate comment additions
                if "Heart Rate" in key:
                    user_hr = self.userData['heart']
                    user_max_hr = 220-self.userData['age']
                    if user_hr > user_max_hr:
                        plot["explanation"] += f"\n\nAt your age, you're above your estimated Maximum Heart Rate, {user_max_hr} bpm, please take it easy."
                    if 60 <= user_hr < 100:
                        plot["explanation"] += "\n\nYour heart rate implies you're at a resting rate. Is that the best you can do?"
                    if user_hr < 60:
                        plot["explanation"] += "\n\nYour heart rate implies that you are sleeping. If that is not the case, consider contacting your doctor."
                if "Body Temperature" in key:
                    user_bt = self.userData['bodyTemp']
                    user_bt_fahrenheit=(user_bt*1.8) + 32 
                    if user_bt > 39.5:
                        plot["explanation"] += f"\n\nWARNING: Your body temperature is at a dangerous level of {user_bt} degrees Celsius ({user_bt_fahrenheit} degrees Fahrenheit). Please seek immediate medical attention if temperature doesn't decrease."
                    if user_bt <= 35:
                        plot["explanation"] += f"\n\nWARNING: Your body temperature is at a dangerous level of {user_bt} degrees Celsius ({user_bt_fahrenheit} degrees Fahrenheit). Please seek immediate medical attention, you maybe experiencing hypothermia."

                

        else:
            if not hasattr(self, 'csvPath'):
                QMessageBox.warning(self, "No File", "⚠️ Please upload a CSV file first. ⚠️")
                return

            # Toggle for CSV Plot
            if self.plotToggleButton.isChecked():
                plots = {
                    "Age vs Calories Burned": {
                        "figure": modelFile.received_csv_data_scatter(self.csvPath)["Age"],
                        "explanation": "This scatter plot shows the relationship between age and calories burned in the dataset."
                    },
                    "Height vs Calories Burned": {
                        "figure": modelFile.received_csv_data_scatter(self.csvPath)["Height"],
                        "explanation": "This scatter plot visualizes how height affects calories burned."
                    },
                    "Heart Rate vs Calories Burned": {
                        "figure": modelFile.received_csv_data_scatter(self.csvPath)["Heart_Rate"],
                        "explanation": "Heart rate plays a significant role in calorie burning. This scatter plot compares heart rates to calories burned."
                    },
                    "Body Temperature vs Calories Burned": {
                        "figure": modelFile.received_csv_data_scatter(self.csvPath)["Body_Temp"],
                        "explanation": "This scatter plot examines how body temperature influences calorie burning."
                    }
                }
            else:
                plots = {
                    "Age Distribution": {
                        "figure": modelFile.received_csv_data_histogram(self.csvPath)["Age"],
                        "explanation": "This histogram represents the age distribution in the dataset."
                    },
                    "Height Distribution": {
                        "figure": modelFile.received_csv_data_histogram(self.csvPath)["Height"],
                        "explanation": "This histogram shows the distribution of heights in the dataset."
                    },
                    "Heart Rate Distribution": {
                        "figure": modelFile.received_csv_data_histogram(self.csvPath)["Heart_Rate"],
                        "explanation": "This histogram represents the distribution of heart rates in the dataset."
                    },
                    "Body Temperature Distribution": {
                        "figure": modelFile.received_csv_data_histogram(self.csvPath)["Body_Temp"],
                        "explanation": "This histogram visualizes the body temperature distribution within the dataset."
                    }
                }

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

    for desc, details in plots.items():
        fig = details["figure"]
        explanation = details["explanation"]

        canvas = FigureCanvas(fig)
        canvas.setMinimumHeight(canvas.sizeHint().height())
        canvas.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        canvas.updateGeometry()
        canvas.draw()

        label = QLabel(explanation)  # Displaying a detailed explanation instead of a simple title

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
