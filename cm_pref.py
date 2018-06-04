# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'cm_pref.ui'
#
# Created by: PyQt5 UI code generator 5.10.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_qt_pref(object):
    def setupUi(self, qt_pref):
        qt_pref.setObjectName("qt_pref")
        qt_pref.resize(580, 356)
        self.buttonBox = QtWidgets.QDialogButtonBox(qt_pref)
        self.buttonBox.setGeometry(QtCore.QRect(210, 310, 341, 32))
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.splitter = QtWidgets.QSplitter(qt_pref)
        self.splitter.setGeometry(QtCore.QRect(190, 10, 125, 42))
        self.splitter.setOrientation(QtCore.Qt.Vertical)
        self.splitter.setObjectName("splitter")
        self.RWbox = QtWidgets.QComboBox(qt_pref)
        self.RWbox.setGeometry(QtCore.QRect(110, 10, 171, 26))
        self.RWbox.setObjectName("RWbox")
        self.RWLabel = QtWidgets.QLabel(qt_pref)
        self.RWLabel.setGeometry(QtCore.QRect(10, 10, 91, 16))
        self.RWLabel.setObjectName("RWLabel")
        self.FilesOpen = QtWidgets.QLineEdit(qt_pref)
        self.FilesOpen.setGeometry(QtCore.QRect(110, 60, 231, 21))
        self.FilesOpen.setObjectName("FilesOpen")
        self.OpenFiles = QtWidgets.QLabel(qt_pref)
        self.OpenFiles.setGeometry(QtCore.QRect(10, 60, 71, 16))
        self.OpenFiles.setObjectName("OpenFiles")
        self.SelectFile = QtWidgets.QPushButton(qt_pref)
        self.SelectFile.setGeometry(QtCore.QRect(340, 60, 113, 32))
        self.SelectFile.setObjectName("SelectFile")
        self.devices = QtWidgets.QLabel(qt_pref)
        self.devices.setGeometry(QtCore.QRect(10, 110, 71, 16))
        self.devices.setObjectName("devices")
        self.device_regexp = QtWidgets.QLineEdit(qt_pref)
        self.device_regexp.setGeometry(QtCore.QRect(110, 110, 171, 21))
        self.device_regexp.setObjectName("device_regexp")

        self.retranslateUi(qt_pref)
        self.buttonBox.accepted.connect(qt_pref.accept)
        self.buttonBox.rejected.connect(qt_pref.reject)
        QtCore.QMetaObject.connectSlotsByName(qt_pref)

    def retranslateUi(self, qt_pref):
        _translate = QtCore.QCoreApplication.translate
        qt_pref.setWindowTitle(_translate("qt_pref", "Preferences"))
        self.RWLabel.setText(_translate("qt_pref", "Data to Draw"))
        self.OpenFiles.setText(_translate("qt_pref", "Open Files"))
        self.SelectFile.setText(_translate("qt_pref", "Select File"))
        self.devices.setText(_translate("qt_pref", "Devices"))
        self.device_regexp.setToolTip(_translate("qt_pref", "Enter a regexp (e.g.  nv.*)"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    qt_pref = QtWidgets.QDialog()
    ui = Ui_qt_pref()
    ui.setupUi(qt_pref)
    qt_pref.show()
    sys.exit(app.exec_())

