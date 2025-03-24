import sys
import os
import time
import hashlib
from PyQt6.QtWidgets import QApplication, QWidget, QLineEdit, QPushButton, QLabel, QGridLayout, QSizePolicy
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QIcon
from PyQt6.QtSql import QSqlDatabase, QSqlQuery, QSqlError
from caloriesUI_app import CaloriePredictor # brings the calorie predictor application into this

# Username: JustinL     Password: password
class LoginWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Login')
        self.setWindowIcon(QIcon(''))
        self.setGeometry(100, 100, 400, 100) 
                                 # width, height

        layout = QGridLayout()
        self.setLayout(layout)

        labels = {}
        self.lineEdits = {}

        labels['Username'] = QLabel('Username:')
        labels['Password'] = QLabel('Password:')
        labels['Username'].setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        labels['Password'].setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)

        self.lineEdits['Username'] = QLineEdit()
        self.lineEdits['Password'] = QLineEdit()
        self.lineEdits['Password'].setEchoMode(QLineEdit.EchoMode.Password)

        layout.addWidget(labels['Username'],            0, 0, 1, 1) # positions on the grid
        layout.addWidget(self.lineEdits['Username'],    0, 1, 1, 3)
        layout.addWidget(labels['Password'],            1, 0, 1, 1)
        layout.addWidget(self.lineEdits['Password'],    1, 1, 1, 3)

        # login button
        button_login = QPushButton('&Log In', clicked=self.checkCredential)
        layout.addWidget(button_login, 2, 3, 1, 1)

        # sign in button
        button_signup = QPushButton('&Sign Up', clicked=self.signUp)
        layout.addWidget(button_signup, 2, 2, 1, 1)

        # guest login button
        button_guest = QPushButton('&Guest', clicked=self.guestLogin)
        layout.addWidget(button_guest, 2, 1, 1, 1)

        # error text
        self.status = QLabel('')
        self.status.setStyleSheet('color:red;')
        layout.addWidget(self.status)
        
        # connects to the local database 
        self.connectToDB()

    def connectToDB(self):
        db_path = "users.db"  # Local SQLite database file
        self.db = QSqlDatabase.addDatabase('QSQLITE')
        self.db.setDatabaseName(db_path)

        if not self.db.open():
            self.status.setText(f'Connection Failed: {self.db.lastError().text()}')
        else:
            self.createUsersTable()
    
    def createUsersTable(self):
        query = QSqlQuery()
        query.exec("""
        CREATE TABLE IF NOT EXISTS Users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            Username TEXT UNIQUE NOT NULL,
            Password TEXT NOT NULL
        )
        """)

    # encodes password in the db
    def hashPassword(self, password): 
        return hashlib.sha256(password.encode()).hexdigest()

    # checks if the username and password is correct, if so, moves on to the calories perdiction app, otherwise, displays a status text
    def checkCredential(self):
        username = self.lineEdits['Username'].text()
        password = self.lineEdits['Password'].text()
        hashed_password = self.hashPassword(password)

        query = QSqlQuery()
        query.prepare('SELECT Password FROM Users WHERE Username=:username')
        query.bindValue(':username', username)
        query.exec()

        if query.first():
            stored_password = query.value(0)
            if stored_password == hashed_password:  # Compare hashed values
                time.sleep(1)
                 # Open the caloriesUI_app.py
                self.otherApp = CaloriePredictor()  # Create an instance of the other app
                self.otherApp.show()  # Show the other application window
                self.close()

            else:
                self.status.setText('Password is incorrect')
        else:
            self.status.setText('Username is not found')

    # takes the text in username and password lines and creates a username and password in the db for it, usernames must be unique, hashs the password
    def signUp(self):
        username = self.lineEdits['Username'].text()
        password = self.lineEdits['Password'].text()
        hashed_password = self.hashPassword(password)

        if not username or not password:
            self.status.setText('Username and Password required')
            return

        query = QSqlQuery()
        query.prepare('INSERT INTO Users (Username, Password) VALUES (:username, :password)')
        query.bindValue(':username', username)
        query.bindValue(':password', hashed_password)

        if query.exec():
            self.status.setText('Sign Up Successful!')
        else:
            self.status.setText('Username already exists')

    # doesnt require username or password to open app, nothing is saved
    def guestLogin(self):
         # Open the caloriesUI_app.py
        self.otherApp = CaloriePredictor()  # Create an instance of the other app
        self.otherApp.show()  # Show the other application window
        self.close()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    
    loginWindow = LoginWindow()
    loginWindow.show()

    try:
        sys.exit(app.exec())
    except SystemExit:
        print('Closing Window...')
