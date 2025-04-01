from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (QWidget, QLabel, QVBoxLayout, QHBoxLayout, QScrollArea,
                             QPushButton, QLineEdit, QComboBox, QFrame, QSizePolicy)


class CaloriePredictor(QWidget):
    
    def __init__(self):
        super().__init__()
        self.initUI()


    # UI Format
    def initUI(self):
        self.setWindowTitle("🔥 Calorie Burnt Prediction App 🔥")
        self.showMaximized()

        mainLayout = QVBoxLayout(self)

        scroll = QScrollArea(self)
        scroll.setWidgetResizable(True)
        scroll.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)

        content = QWidget()
        scroll.setWidget(content)
        content.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)

        self.contentLayout = QVBoxLayout(content)

        mainLayout.addWidget(scroll)

        # Input Fields
        self.ageInput = QLineEdit(self)
        self.ageInput.setPlaceholderText("Enter Age Here")
        self.contentLayout.addWidget(QLabel("Age:"))
        self.contentLayout.addWidget(self.ageInput)

        self.genderInput = QComboBox(self)
        self.genderInput.addItems(["Select Gender Here", "Male", "Female"])
        self.contentLayout.addWidget(QLabel("Gender:"))
        self.contentLayout.addWidget(self.genderInput)

        self.heightInput = QLineEdit(self)
        self.heightInput.setPlaceholderText("Enter Height Here")
        self.contentLayout.addWidget(QLabel("Height (cm):"))
        self.contentLayout.addWidget(self.heightInput)

        self.heartRateInput = QLineEdit(self)
        self.heartRateInput.setPlaceholderText("Enter Heart Rate Here")
        self.contentLayout.addWidget(QLabel("Heart Rate (bpm):"))
        self.contentLayout.addWidget(self.heartRateInput)

        self.bodyTempInput = QLineEdit(self)
        self.bodyTempInput.setPlaceholderText("Enter Body Temperature Here")
        self.contentLayout.addWidget(QLabel("Body Temperature (°C):"))
        self.contentLayout.addWidget(self.bodyTempInput)

        # Prediction Button
        self.predictButton = QPushButton("🚨 Calorie Prediction", self)
        self.predictButton.clicked.connect(self.predictCalories)
        self.contentLayout.addWidget(self.predictButton)

        # Placeholder for the Prediction Calories
        self.resultLabel = QLabel("", self)
        self.contentLayout.addWidget(self.resultLabel)

        # Placeholder for the Percentile Value
        self.percentileLabel = QLabel("", self)
        self.contentLayout.addWidget(self.percentileLabel)

        # Pixel Padding
        self.contentLayout.addSpacing(10)

        # Divider Line
        topDivider = QFrame()
        topDivider.setFrameShape(QFrame.Shape.HLine)
        topDivider.setFrameShadow(QFrame.Shadow.Sunken)
        self.contentLayout.addWidget(topDivider)

        # Pixal Padding
        self.contentLayout.addSpacing(10)

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

        self.contentLayout.addLayout(uploadRow)

        self.processButton = QPushButton("⚙️ Process CSV Data", self)
        self.processButton.clicked.connect(self.renderPlot)
        self.contentLayout.addWidget(self.processButton)

        # Pixel Padding
        self.contentLayout.addSpacing(10)

        # Top Divider Line
        topDivider = QFrame()
        topDivider.setFrameShape(QFrame.Shape.HLine)
        topDivider.setFrameShadow(QFrame.Shadow.Sunken)
        self.contentLayout.addWidget(topDivider)

        # Centered layout for toggle button
        toggleLayout = QHBoxLayout()

        # Toggle Function (False = Histogram, True = Scatter)
        self.plotToggleButton = QPushButton("View: Histogram", self)
        self.plotToggleButton.setCheckable(True)
        self.plotToggleButton.setChecked(False)
        self.plotToggleButton.setFixedWidth(150)
        self.plotToggleButton.clicked.connect(self.togglePlotType)

        toggleLayout.addStretch()
        toggleLayout.addWidget(self.plotToggleButton)
        toggleLayout.addStretch()

        self.contentLayout.addLayout(toggleLayout)

        # Bottom Divider Line
        bottomDivider = QFrame()
        bottomDivider.setFrameShape(QFrame.Shape.HLine)
        bottomDivider.setFrameShadow(QFrame.Shadow.Sunken)
        self.contentLayout.addWidget(bottomDivider)

        # Pixal Padding
        self.contentLayout.addSpacing(10)
