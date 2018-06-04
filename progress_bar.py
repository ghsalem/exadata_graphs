from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Form(object):
	def setupUi(self, Form):
		Form.setObjectName("Form")
		Form.resize(575, 84)
		self.progressBar = QtWidgets.QProgressBar(Form)
		self.progressBar.setGeometry(QtCore.QRect(30, 30, 500, 35))
		sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
		sizePolicy.setHorizontalStretch(0)
		sizePolicy.setVerticalStretch(0)
		sizePolicy.setHeightForWidth(self.progressBar.sizePolicy().hasHeightForWidth())
		self.progressBar.setSizePolicy(sizePolicy)
		self.progressBar.setMinimumSize(QtCore.QSize(500, 35))
		self.progressBar.setMaximumSize(QtCore.QSize(500, 35))
		self.progressBar.setProperty("value", 0)
		self.progressBar.setObjectName("progressBar")
	
		self.retranslateUi(Form)
		QtCore.QMetaObject.connectSlotsByName(Form)

	def retranslateUi(self, Form):
		_translate = QtCore.QCoreApplication.translate
		Form.setWindowTitle(_translate("Form", "Progress bar"))
	

class ProgressBar(QtWidgets.QDialog, Ui_Form):
	def __init__(self, desc = None, parent=None):
		super(ProgressBar, self).__init__(parent)
		self.setupUi(self)
		self.show()

		if desc != None:
			self.setDescription(desc)

	def setValue(self, val): # Sets value
		self.progressBar.setProperty("value", val)

	def setDescription(self, desc): # Sets Pbar window title
		self.setWindowTitle(desc)
	