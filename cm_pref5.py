# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'cm_pref.ui'
#
# Created by: PyQt5 UI code generator 5.8
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets
from cm_pref import Ui_qt_pref
import glob

try:
	_fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
	def _fromUtf8(s):
		return s

try:
	_encoding = QtWidgets.QApplication.UnicodeUTF8
	def _translate(context, text, disambig):
		return QtWidgets.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
	def _translate(context, text, disambig):
		return QtWidgets.QApplication.translate(context, text, disambig)

class Ui_cm_pref(object):
	def setupUi(self, cm_pref, pobj):
		self.cm_pref=cm_pref
		cm_pref.setObjectName("cm_pref")
		self.qt_pref=Ui_qt_pref()
		self.parent=pobj
		self.qt_pref.setupUi(cm_pref)
		for i in self.parent.metric_column_d:
			self.qt_pref.RWbox.addItem(i)
		self.qt_pref.device_regexp.setText(self.parent.devices)
		self.qt_pref.buttonBox.accepted.connect(self.accept)
		self.qt_pref.buttonBox.rejected.connect(self.reject)
		self.qt_pref.SelectFile.clicked.connect(self.save_to_file)
		self.metric=list(self.parent.metric_column_d.keys())[0]

	def save_to_file(self):

		open_file_name, _ =QtWidgets.QFileDialog.getOpenFileNames(self.qt_pref.buttonBox, 'Open Files','','*.bz2')
		if open_file_name:
			self.open_files=open_file_name
			self.qt_pref.FilesOpen.setText(';'.join(self.open_files))

	def reject(self):
		self.cm_pref.close()


	def accept(self):
		self.open_files=None
		open_file=self.qt_pref.FilesOpen.text()
		if ('*'+open_file).rindex('*')>0:
			# will glob the file name into a list, as there is a * in the file name
			self.open_files=sorted(glob.glob(open_file))
		else:
			if len(open_file)>0:
				self.open_files=open_file.split(';')
		self.metric=self.qt_pref.RWbox.currentText()
		self.devices=self.qt_pref.device_regexp.text()
		#print("Metric",self.metric)
		self.cm_pref.close()

