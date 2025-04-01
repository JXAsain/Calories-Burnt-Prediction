import joblib
import numpy as np
from PyQt6.QtCore import Qt
import pytest
from caloriesUI_app.elementsUI import CaloriePredictor
from caloriesUI_app.eventHandlers import extend_caloriesPredictor
from PyQt6.QtWidgets import QApplication


@pytest.fixture
def app(qtbot):
    extend_caloriesPredictor()
    # Initialize the application
    calorie_app = CaloriePredictor()
    calorie_app.hide()
    qtbot.addWidget(calorie_app)  # Add the widget to qtbot for lifecycle management
    return calorie_app


model = joblib.load('calories_predictor.pkl')


# np.array([[gender, age, height, heart_rate, body_temp]])


def test_gender_validation():
   input_data = np.array([["Select Gender Here", 21, 170, 156, 39.5]])
   with pytest.raises(ValueError):
       model.predict(input_data)


def test_age_validation():
   input_data = np.array([['male', None, 170, 156, 39.5]])
   with pytest.raises(ValueError):
       model.predict(input_data)


def test_height_validation():
   input_data = np.array([['male', 21, None, 156, 39.5]])
   with pytest.raises(ValueError):
       model.predict(input_data)


def test_heart_validation():
   input_data = np.array([['male', 21, 170, None, 39.5]])
   with pytest.raises(ValueError):
       model.predict(input_data)


def test_temp_validation():
   input_data = np.array([['male', 21, 170, 156, None]])
   with pytest.raises(ValueError):
       model.predict(input_data)


















#ages
def test_over_age(app, qtbot, mocker):
    mock_warning = mocker.patch("PyQt6.QtWidgets.QMessageBox.warning")

    # Set inputs
    app.ageInput.setText("150") #over
    app.genderInput.setCurrentText("Male")  
    app.heightInput.setText("175") 
    app.heartRateInput.setText("80")  
    app.bodyTempInput.setText("36.5")  

    # Simulate button click
    qtbot.mouseClick(app.predictButton, Qt.MouseButton.LeftButton)

    # Assert QMessageBox.warning was called
    mock_warning.assert_called_once()

    # Assert no result 
    assert app.resultLabel.text() == ""


def test_under_age(app, qtbot, mocker):
    mock_warning = mocker.patch("PyQt6.QtWidgets.QMessageBox.warning")

    # Set inputs
    app.ageInput.setText("-1") #under
    app.genderInput.setCurrentText("Male")  
    app.heightInput.setText("175") 
    app.heartRateInput.setText("80")  
    app.bodyTempInput.setText("36.5")  

    # Simulate button click
    qtbot.mouseClick(app.predictButton, Qt.MouseButton.LeftButton)

    # Assert QMessageBox.warning was called
    mock_warning.assert_called_once()

    # Assert no result
    assert app.resultLabel.text() == ""


def test_lowest_age(app, qtbot, mocker):
    mock_warning = mocker.patch("PyQt6.QtWidgets.QMessageBox.warning")

    # Set inputs
    app.ageInput.setText("0") #lowest
    app.genderInput.setCurrentText("Male")  
    app.heightInput.setText("175") 
    app.heartRateInput.setText("80")  
    app.bodyTempInput.setText("36.5")  

    # Simulate button click
    qtbot.mouseClick(app.predictButton, Qt.MouseButton.LeftButton)

    # Assert result
    assert app.resultLabel.text() != ""


def test_highest_age(app, qtbot, mocker):
    mock_warning = mocker.patch("PyQt6.QtWidgets.QMessageBox.warning")

    # Set inputs
    app.ageInput.setText("130") #highest
    app.genderInput.setCurrentText("Male")  
    app.heightInput.setText("175") 
    app.heartRateInput.setText("80")  
    app.bodyTempInput.setText("36.5")  

    # Simulate button click
    qtbot.mouseClick(app.predictButton, Qt.MouseButton.LeftButton)

    # Assert result
    assert app.resultLabel.text() != ""














# heights
def test_over_height(app, qtbot, mocker):
    mock_warning = mocker.patch("PyQt6.QtWidgets.QMessageBox.warning")

    # Set inputs
    app.ageInput.setText("30") 
    app.genderInput.setCurrentText("Male")  
    app.heightInput.setText("300") #over
    app.heartRateInput.setText("80")  
    app.bodyTempInput.setText("36.5")  

    # Simulate button click
    qtbot.mouseClick(app.predictButton, Qt.MouseButton.LeftButton)

    # Assert QMessageBox.warning was called
    mock_warning.assert_called_once()

    # Assert no result 
    assert app.resultLabel.text() == ""


def test_under_height(app, qtbot, mocker):
    mock_warning = mocker.patch("PyQt6.QtWidgets.QMessageBox.warning")

    # Set inputs
    app.ageInput.setText("30") 
    app.genderInput.setCurrentText("Male")  
    app.heightInput.setText("0") #under
    app.heartRateInput.setText("80")  
    app.bodyTempInput.setText("36.5")  

    # Simulate button click
    qtbot.mouseClick(app.predictButton, Qt.MouseButton.LeftButton)

    # Assert QMessageBox.warning was called
    mock_warning.assert_called_once()

    # Assert no result
    assert app.resultLabel.text() == ""


def test_lowest_height(app, qtbot, mocker):
    mock_warning = mocker.patch("PyQt6.QtWidgets.QMessageBox.warning")

    # Set inputs
    app.ageInput.setText("30") 
    app.genderInput.setCurrentText("Male")  
    app.heightInput.setText("1") #lowest
    app.heartRateInput.setText("80")  
    app.bodyTempInput.setText("36.5")  

    # Simulate button click
    qtbot.mouseClick(app.predictButton, Qt.MouseButton.LeftButton)

    # Assert result
    assert app.resultLabel.text() != ""


def test_highest_height(app, qtbot, mocker):
    mock_warning = mocker.patch("PyQt6.QtWidgets.QMessageBox.warning")

    # Set inputs
    app.ageInput.setText("130") 
    app.genderInput.setCurrentText("Male")  
    app.heightInput.setText("275") #highest
    app.heartRateInput.setText("80")  
    app.bodyTempInput.setText("36.5")  

    # Simulate button click
    qtbot.mouseClick(app.predictButton, Qt.MouseButton.LeftButton)

    # Assert result
    assert app.resultLabel.text() != ""
















# heart
def test_over_heart(app, qtbot, mocker):
    mock_warning = mocker.patch("PyQt6.QtWidgets.QMessageBox.warning")

    # Set inputs
    app.ageInput.setText("30") 
    app.genderInput.setCurrentText("Male")  
    app.heightInput.setText("175") 
    app.heartRateInput.setText("250")  #over
    app.bodyTempInput.setText("36.5")  

    # Simulate button click
    qtbot.mouseClick(app.predictButton, Qt.MouseButton.LeftButton)

    # Assert QMessageBox.warning was called
    mock_warning.assert_called_once()

    # Assert no result 
    assert app.resultLabel.text() == ""


def test_under_heart(app, qtbot, mocker):
    mock_warning = mocker.patch("PyQt6.QtWidgets.QMessageBox.warning")

    # Set inputs
    app.ageInput.setText("30") 
    app.genderInput.setCurrentText("Male")  
    app.heightInput.setText("175") 
    app.heartRateInput.setText("10")  #under
    app.bodyTempInput.setText("36.5")  

    # Simulate button click
    qtbot.mouseClick(app.predictButton, Qt.MouseButton.LeftButton)

    # Assert QMessageBox.warning was called
    mock_warning.assert_called_once()

    # Assert no result
    assert app.resultLabel.text() == ""


def test_lowest_heart(app, qtbot, mocker):
    mock_warning = mocker.patch("PyQt6.QtWidgets.QMessageBox.warning")

    # Set inputs
    app.ageInput.setText("30") 
    app.genderInput.setCurrentText("Male")  
    app.heightInput.setText("175") 
    app.heartRateInput.setText("20")  #lowest
    app.bodyTempInput.setText("36.5")  

    # Simulate button click
    qtbot.mouseClick(app.predictButton, Qt.MouseButton.LeftButton)

    # Assert result
    assert app.resultLabel.text() != ""


def test_highest_heart(app, qtbot, mocker):
    mock_warning = mocker.patch("PyQt6.QtWidgets.QMessageBox.warning")

    # Set inputs
    app.ageInput.setText("30") 
    app.genderInput.setCurrentText("Male")  
    app.heightInput.setText("175") 
    app.heartRateInput.setText("220")  #highest
    app.bodyTempInput.setText("36.5")  

    # Simulate button click
    qtbot.mouseClick(app.predictButton, Qt.MouseButton.LeftButton)

    # Assert result
    assert app.resultLabel.text() != ""






















# body temp
def test_over_temp(app, qtbot, mocker):
    mock_warning = mocker.patch("PyQt6.QtWidgets.QMessageBox.warning")

    # Set inputs
    app.ageInput.setText("30") 
    app.genderInput.setCurrentText("Male")  
    app.heightInput.setText("175") 
    app.heartRateInput.setText("80")  
    app.bodyTempInput.setText("45.0")  #over

    # Simulate button click
    qtbot.mouseClick(app.predictButton, Qt.MouseButton.LeftButton)

    # Assert QMessageBox.warning was called
    mock_warning.assert_called_once()

    # Assert no result 
    assert app.resultLabel.text() == ""


def test_under_temp(app, qtbot, mocker):
    mock_warning = mocker.patch("PyQt6.QtWidgets.QMessageBox.warning")

    # Set inputs
    app.ageInput.setText("30") 
    app.genderInput.setCurrentText("Male")  
    app.heightInput.setText("175") 
    app.heartRateInput.setText("80")  
    app.bodyTempInput.setText("30.0")  #under

    # Simulate button click
    qtbot.mouseClick(app.predictButton, Qt.MouseButton.LeftButton)

    # Assert QMessageBox.warning was called
    mock_warning.assert_called_once()

    # Assert no result
    assert app.resultLabel.text() == ""


def test_lowest_temp(app, qtbot, mocker):
    mock_warning = mocker.patch("PyQt6.QtWidgets.QMessageBox.warning")

    # Set inputs
    app.ageInput.setText("30") 
    app.genderInput.setCurrentText("Male")  
    app.heightInput.setText("175") 
    app.heartRateInput.setText("80")  
    app.bodyTempInput.setText("35.0")  #lowest

    # Simulate button click
    qtbot.mouseClick(app.predictButton, Qt.MouseButton.LeftButton)

    # Assert result
    assert app.resultLabel.text() != ""


def test_highest_temp(app, qtbot, mocker):
    mock_warning = mocker.patch("PyQt6.QtWidgets.QMessageBox.warning")

    # Set inputs
    app.ageInput.setText("30") 
    app.genderInput.setCurrentText("Male")  
    app.heightInput.setText("175") 
    app.heartRateInput.setText("80")  
    app.bodyTempInput.setText("42.0")  #highest

    # Simulate button click
    qtbot.mouseClick(app.predictButton, Qt.MouseButton.LeftButton)

    # Assert result
    assert app.resultLabel.text() != ""
