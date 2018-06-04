# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'choose_stats.ui'
#
# Created by: PyQt5 UI code generator 5.8
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets
import pandas as pd

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

class Ui_ChooseCellStats(object):
	def __init__(self):
		self.metric_name=[]
		self.metric_descriptions=[]
		
	def setupUi(self, ChooseCellStats):
		self.ChooseCellStats=ChooseCellStats
		self.ChooseCellStats.setObjectName("ChooseCellStats")
		self.ChooseCellStats.resize(446, 460)
		sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
		sizePolicy.setHorizontalStretch(0)
		sizePolicy.setVerticalStretch(0)
		sizePolicy.setHeightForWidth(self.ChooseCellStats.sizePolicy().hasHeightForWidth())
		self.ChooseCellStats.setSizePolicy(sizePolicy)
		self.verticalLayout = QtWidgets.QVBoxLayout(self.ChooseCellStats)
		self.verticalLayout.setSpacing(7)
		self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
		self.buttonBox = QtWidgets.QDialogButtonBox(ChooseCellStats)
		self.buttonBox.setGeometry(QtCore.QRect(159, 300, 171, 31))
		self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
		self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
		self.buttonBox.setObjectName("buttonBox")
		self.MetricDef = QtWidgets.QTreeWidget(ChooseCellStats)
		self.MetricDef.setGeometry(QtCore.QRect(20, 20, 331, 310))
		self.MetricDef.setColumnCount(2)
		self.MetricDef.setObjectName("MetricDef")
		#sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
		#sizePolicy.setHorizontalStretch(0)
		#sizePolicy.setVerticalStretch(0)
		sizePolicy.setHeightForWidth(self.MetricDef.sizePolicy().hasHeightForWidth())
		self.MetricDef.setSizePolicy(sizePolicy)
		self.verticalLayout.addWidget(self.MetricDef)
		self.verticalLayout.addWidget(self.buttonBox)
		self.load_metric_def()
		self.retranslateUi(ChooseCellStats)
		self.buttonBox.accepted.connect(self.get_selected_stat)
		self.buttonBox.rejected.connect(self.reject)
		QtCore.QMetaObject.connectSlotsByName(ChooseCellStats)

	def reject(self):
		self.is_accepted=False
		self.ChooseCellStats.close()

	def get_selected_stat(self):
		iterator = QtWidgets.QTreeWidgetItemIterator(self.MetricDef, QtWidgets.QTreeWidgetItemIterator.Checked)
		self.metric_name=[]
		while iterator.value():
			item = iterator.value()
			met=item.text(1)
			self.metric_name.append(met)
			iterator+=1
		self.ChooseCellStats.close()

	def load_metric_def(self):
		self.metric_descriptions=pd.read_csv('cstatslist.csv',sep=';',names=['MetricType','Metric']).sort_values(['MetricType','Metric'])
		root_ot=""
		for i in range(len(self.metric_descriptions)):
			met=self.metric_descriptions.iloc[i]['Metric']
			if root_ot!=self.metric_descriptions.iloc[i]['MetricType']:
				root = QtWidgets.QTreeWidgetItem(self.MetricDef, list(self.metric_descriptions.iloc[i][['MetricType','Metric']]))
				root_ot=self.metric_descriptions.iloc[i]['MetricType']
				root.setFlags(root.flags() | QtCore.Qt.ItemIsUserCheckable)
				if met in self.metric_name:
					root.setCheckState(0, QtCore.Qt.Checked)
				else:
					root.setCheckState(0, QtCore.Qt.Unchecked)
			else:
				child=QtWidgets.QTreeWidgetItem(root, list(self.metric_descriptions.iloc[i][['MetricType','Metric']]))
				child.setFlags(child.flags() | QtCore.Qt.ItemIsUserCheckable)
				if met in self.metric_name:
					child.setCheckState(0, QtCore.Qt.Checked)
				else:
					child.setCheckState(0, QtCore.Qt.Unchecked)
		for i in range(self.MetricDef.columnCount()):
			self.MetricDef.resizeColumnToContents(i)


	def retranslateUi(self, ChooseCellStats):
		_translate = QtCore.QCoreApplication.translate
		ChooseCellStats.setWindowTitle(_translate("ChooseCellStats", "Choose Statistics to Graph"))
		self.MetricDef.headerItem().setText(0, _translate("CellMH", "Metric Type", None))
		self.MetricDef.headerItem().setText(1, _translate("CellMH", "Metric", None))

