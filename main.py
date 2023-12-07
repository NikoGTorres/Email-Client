# Import necessary libraries
from PyQt5.QtWidgets import *
from PyQt5 import uic

# Library for Simple Mail Transfer Protocol (SMTP)
import smtplib
from email import encoders

# Import in order to allow for attachments
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart

class MyGUI(QMainWindow):
    def __init__(self):
        super(MyGUI, self).__init__()
        # Load the UI file
        uic.loadUi("mailgui.ui", self)
        self.show()

        # Connect buttons to their respective functions
        self.pushButton.clicked.connect(self.login)
        self.pushButton_2.clicked.connect(self.attach_sth)
        self.pushButton_3.clicked.connect(self.send_mail)
    
    # Login Function
    def login(self):
        try:
            # Set up SMTP server connection
            self.server = smtplib.SMTP(self.lineEdit_3.text(), self.lineEdit_4.text())
            self.server.ehlo()
            self.server.starttls()
            self.server.ehlo()
            self.server.login(self.lineEdit.text(), self.lineEdit_2.text())

            # Disable login input fields and enable email composition elements
            self.lineEdit.setEnabled(False)
            self.lineEdit_2.setEnabled(False)
            self.lineEdit_3.setEnabled(False)
            self.lineEdit_4.setEnabled(False)
            self.pushButton.setEnabled(False)

            self.lineEdit_5.setEnabled(True)
            self.lineEdit_6.setEnabled(True)
            self.textEdit.setEnabled(True)
            self.pushButton_2.setEnabled(True)
            self.pushButton_3.setEnabled(True)

            # Create a MIME message for email composition
            self.msg = MIMEMultipart()
        except smtplib.SMTPAuthenticationError:
            # Display error message for invalid login info
            message_box = QMessageBox()
            message_box.setText("Invalid Login Info")
            message_box.exec()
        except:
            # Display error message for login failure
            message_box = QMessageBox()
            message_box.setText("Login Failed")
            message_box.exec()

    # Attachments Function
    def attach_sth(self):
        # Open a file dialog to select attachments
        options = QFileDialog.options()
        filenames, _ = QFileDialog.getOpenFileNames(self, "Open File", "", "All Files (*.*)", options=options)
        if filenames != []:
            for filename in filenames:
                # Read and attach each selected file
                attachment = open(filename, 'rb')
                filename = filename[filename.rfind("/") + 1:]
                p = MIMEBase('application', 'octet-stream')
                p.set_payload(attachment.read())
                encoders.encode_base64(p)
                p.add_header("Content-Disposition", f"attachment; filename={filename}")
                self.msg.attach(p)
                # Update the UI with attached filenames
                if not self.label_8.text().endswith(":"):
                    self.label_8.setText(self.label_8.text() + ",")
                self.label_8.setText(self.label_8.text() + " " + filename)
    
    # Send Mail Function
    def send_mail(self):
        # Display confirmation dialog for sending the email
        dialog = QMessageBox()
        dialog.setText("Do you want to send this mail?")
        dialog.addButton(QPushButton("Yes"), QMessageBox.YesRole)
        dialog.addButton(QPushButton("No"), QMessageBox.NoRole)

        if dialog.exec_() == 0:
            try:
                # Set up email parameters and send the email
                self.msg['From'] = "NeuralNine"
                self.msg['To'] = self.lineEdit_5.text()
                self.msg['Subject'] = self.lineEdit_6.text()
                self.msg.attach(MIMEText(self.textEdit.toPlainText(), 'plain'))
                text = self.msg.as_string()
                self.server.sendmail(self.lineEdit.text(), self.lineEdit_5.text(), text)
                # Display success message
                message_box = QMessageBox()
                message_box.setText("Email sent")
                message_box.exec()
            except:
                # Display error message for sending email failure
                message_box = QMessageBox()
                message_box.setText("Sending Email Failed")
                message_box.exec()

# Create the application instance and run it
app = QApplication([])
window = MyGUI()
app.exec_()
