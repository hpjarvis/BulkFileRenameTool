from PyQt6 import QtWidgets
from mainwindow import Ui_MainWindow
import time
import os

class MainWindowContainer(Ui_MainWindow):
    def open_folder(self, original_path = ""):
        # Open a file dialog window that allows user to select a folder.
        if original_path == False:
            folderpath = QtWidgets.QFileDialog.getExistingDirectory()
        
        else:
            folderpath = original_path

        # If a folder is selected
        # set the lineedit text to the folder directory
        # get all of the files within the directory and add them to the CurrentDirectoryWidget
        if folderpath != "":
            self.TargetDirectoryEdit.setText(folderpath)

            original_file_names = os.listdir(folderpath)
            self.CurrentDirectoryWidget.addItems(original_file_names)
            self.DirectoryPreviewWidget.addItems(original_file_names)

            extensions = list(set([x.split('.')[-1] for x in original_file_names]))
            self.FileTypesEdit.addItems(['*'] + extensions)

    def test_func(self):
        self.progressBar.setVisible(True)
        self.StartRename.setVisible(False)

        self.CurrentDirectoryWidget.clear()
        self.DirectoryPreviewWidget.clear()
        self.NewFileNameEdit.clear()
        self.open_folder(original_path = self.TargetDirectoryEdit.text())

        self.progressBar.setVisible(False)
        self.StartRename.setVisible(True)

    # when text is entered into the file name edit
    # update the preview list widget
    def update_preview(self):
        if self.DirectoryPreviewWidget.count() != 0 and self.NewFileNameEdit.text() != "":
            # Iterate through all the items, replace the names

            selected_file_type = self.FileTypesEdit.currentText()

            file_number = 0

            # for each item in the list
            for i in range(self.DirectoryPreviewWidget.count()):
                # get the filetype of the item
                extension = self.DirectoryPreviewWidget.item(i).text().split('.')[-1]

                # if a filetype is selected in the dropdown menu and it matched the file extension
                if selected_file_type != "*":
                    if extension == selected_file_type:
                        # change the text of the item and add file_number and extension back on
                        self.DirectoryPreviewWidget.item(i).setText(self.NewFileNameEdit.text() + str(file_number) + '.' + extension)
                        file_number += 1

                # if any file type is selected
                else:
                    self.DirectoryPreviewWidget.item(i).setText(self.NewFileNameEdit.text() + str(file_number) + '.' + extension)
                    file_number += 1

        else:
            self.DirectoryPreviewWidget.clear()
            self.DirectoryPreviewWidget.addItems(list([self.CurrentDirectoryWidget.item(i).text() for i in range(self.CurrentDirectoryWidget.count())]))


    # when the filetype is changed, clear the text box
    def change_file_type(self):
        self.NewFileNameEdit.clear()

    def __init__(self, MainWindow):
        self.setupUi(MainWindow)

        # set placeholder text
        self.NewFileNameEdit.setPlaceholderText("Enter New Filename for each item")

        # hide the progress bar
        self.progressBar.setVisible(False)
        # Link functions to buttons
        self.BrowseButton.clicked.connect(self.open_folder)
        self.StartRename.clicked.connect(self.test_func)

        # link text edits to functions
        self.NewFileNameEdit.textChanged.connect(self.update_preview)

        # link dropdowns to function
        self.FileTypesEdit.currentTextChanged.connect(self.change_file_type)

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = MainWindowContainer(MainWindow)
    MainWindow.show()
    sys.exit(app.exec())
