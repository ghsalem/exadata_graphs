# -*- coding: utf-8 -*-
# this tool can be used to graph Exadata cell statistics. It relies on the Exawatcher files that are stored on the cells.
# You have 2 modes to execute it: either you copied a bunch of files from the cells, and have them available on your machine. In this case you can 
# provide the files using the -f switch whan starting the program (see below on the usage). Or it can be used to get near-real time data from the cells.
# this mode requires some setup that is discussed below.
# 
#             A VERY IMPORTANT NOTE
# 
#  This Tool is given as is, no warranty whatsoever if provided. It does not write anything in the Exadata system, nor in any database. Nevertheless
# you take full responsability over it's usage. It is NOT an Oracle Corp tool, and not sanctioned by Oracle Corp in a way.
#
#  ====================================================
# usage:
# python cellstats5.py [-s] [ -f list_of_files]
# the -s switch is to tell the tool to use splines when graphing the data (making for smoother plots)
# if you copied exawatcher cellstats files over to your machine, you can give the list of files after the -f switch. 
#  You can use wild cards, in this case the list_of_files should be in double quotes (e.g. -f "cell*.bz2"). You can either have the files compressed
# or uncompressed (this would be the case if you copied the latest exawatcher file).
# When used with the -f switch, the tool does not require any special setup. Otherwise, you should have a setup allowing you to ssh to the 
# exadata cells in order to get the required data. Please read the comments in the redraw_graphs function below ,to see what you should do
#
# this tool requires the different modules listed below, the biggest one sbein PyQT5, and the matplotlib package, as well as scipy, numpy and pandas
# 
import subprocess
import os,sys,getopt,re
import pandas as pd
import datetime as dt
import bz2
import glob

from PyQt5 import QtCore, QtWidgets, QtWidgets
from matplotlib.backends.backend_pdf import PdfPages

# the following are modules provided by the tool (accompanying .py files )
from cm_pref5 import Ui_cm_pref
from Cellgraphrt5 import CellGraphrtPage
#from ChooseCellStats import Ui_ChooseCellStats
from progress_bar import ProgressBar, Ui_Form
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

class Ui_CellMH(object):
	def setupUi(self, CellMH, list_of_files, p_devices):
		CellMH.setObjectName(_fromUtf8("CellMH"))
		CellMH.resize(800, 600)
		self.list_of_files=list_of_files
		sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
		sizePolicy.setHorizontalStretch(0)
		sizePolicy.setVerticalStretch(0)
		sizePolicy.setHeightForWidth(CellMH.sizePolicy().hasHeightForWidth())
		CellMH.setSizePolicy(sizePolicy)
		self.centralwidget = QtWidgets.QWidget(CellMH)
		sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
		sizePolicy.setHorizontalStretch(0)
		sizePolicy.setVerticalStretch(0)
		sizePolicy.setHeightForWidth(self.centralwidget.sizePolicy().hasHeightForWidth())
		self.centralwidget.setSizePolicy(sizePolicy)
		self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
		self.verticalLayout = QtWidgets.QVBoxLayout(self.centralwidget)
		self.verticalLayout.setSpacing(7)
		self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
		self.GraphScrollArea = QtWidgets.QScrollArea(self.centralwidget)#self.GraphArea)
		self.GraphScrollArea.setWidgetResizable(True)
		self.GraphScrollArea.setObjectName(_fromUtf8("GraphScrollArea"))
		#self.GraphScrollArea.setWidget(self.GraphArea)
		self.verticalLayout.addWidget(self.GraphScrollArea)
		self.ga_sa_contents = QtWidgets.QWidget()
		self.ga_sa_contents.setGeometry(QtCore.QRect(0, 0, 728, 476))
		sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
		sizePolicy.setHorizontalStretch(0)
		sizePolicy.setVerticalStretch(0)
		sizePolicy.setHeightForWidth(self.ga_sa_contents.sizePolicy().hasHeightForWidth())
		self.ga_sa_contents.setSizePolicy(sizePolicy)
		self.ga_sa_contents.setObjectName("ga_sa_contents")

		self.ga_vert_layout = QtWidgets.QVBoxLayout(self.ga_sa_contents)
		self.ga_vert_layout.setContentsMargins(0, 0, 0, 0)
		self.ga_vert_layout.setObjectName("ga_vert_layout")
		self.GraphScrollArea.setWidget(self.ga_sa_contents)



		CellMH.setCentralWidget(self.centralwidget)
		self.menubar = QtWidgets.QMenuBar(CellMH)
		self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 21))
		self.menubar.setObjectName(_fromUtf8("menubar"))
		self.menuFile = QtWidgets.QMenu(self.menubar)
		self.menuFile.setObjectName(_fromUtf8("menuFile"))
		CellMH.setMenuBar(self.menubar)
		self.statusbar = QtWidgets.QStatusBar(CellMH)
		self.statusbar.setObjectName(_fromUtf8("statusbar"))
		CellMH.setStatusBar(self.statusbar)
		self.actionConfigure = QtWidgets.QAction(CellMH)
		self.actionConfigure.setObjectName(_fromUtf8("actionConfigure"))
		self.actionExit = QtWidgets.QAction(CellMH)
		self.actionExit.setObjectName(_fromUtf8("actionExit"))
#		self.ChooseStats = QtWidgets.QAction(CellMH)
#		self.ChooseStats.setObjectName(_fromUtf8("ChooseStats"))
		self.Save_to_PDF = QtWidgets.QAction(CellMH)
		self.Save_to_PDF.setObjectName(_fromUtf8("Save_to_PDF"))
		self.menuFile.addAction(self.actionConfigure)
		#self.menuFile.addAction(self.ChooseStats)
		self.menuFile.addAction(self.Save_to_PDF)
		self.menuFile.addAction(self.actionExit)
		self.menubar.addAction(self.menuFile.menuAction())
		self.metric='Reads'
		self.metric_column_d={"Reads":3,"Writes":4,"Read Waits":10,"Write Waits":11,"Service Time":12,"Utilisation":13}
		self.timer = QtCore.QTimer(self.centralwidget)
		self.first_time=True
		self.chosen_stats=None
		self.devices=p_devices
		self.line_graphs=True
		if self.list_of_files is None:
			self.get_prefs()
		self.retranslateUi(CellMH)
		self.to_csv_name=None
#		self.ChooseStats.triggered.connect(self.get_selected_metric)
		self.actionExit.triggered.connect(self.close_application)
		self.Save_to_PDF.triggered.connect(self.save_all_figs)
		self.actionConfigure.triggered.connect(self.get_prefs)
		self.metric_graph=dict()
		self.preferences=None
		self.it_is_bz2=True
		if self.list_of_files is None:
			self.timer.timeout.connect(self.redraw_graphs)
			self.timer.start(5000)
		else:
			self.redraw_graphs()
		QtCore.QMetaObject.connectSlotsByName(CellMH)
		self.current_metrics=None
		self.first_time=True

	def save_all_figs(self):
		save_file_name, _ =QtWidgets.QFileDialog.getSaveFileName(self.centralwidget, 'Save plots to PDF file','','*.pdf')
		if save_file_name:
			with PdfPages(save_file_name) as pdf:
				for n in self.metric_graph:
					pdf.savefig(self.metric_graph[n].figure)

	def redraw_graphs(self):
		def ts(x):
			return x.total_seconds()
		if self.list_of_files !=None:
			# get data from the list of	 files given
			# we'll open the files one by one, fetch the line
			# get the timestamp from the line contaning ===Current Time===
			# and then looking for any of the selected metrics
			# put the results in the the pandas dataframe
			#and then call the redraw events
			self.metric_column=self.metric_column_d[self.metric]
			rows_list=[]
			self.first_time=False
			priortime=None
			nfiles=len(self.list_of_files)
			pbar=ProgressBar(desc="Loading Files")
			n=.5/nfiles
			for fname in self.list_of_files:
				if fname[-3:]=="bz2":
					datfile=bz2.BZ2File(fname)
				else:
					datfile=open(fname,'r')
				
				lines=datfile.readlines()
				cellname=fname[fname.rindex('_',)+1:fname.index('.',fname.rindex('_',))]
				pbar.setDescription("opening:"+os.path.basename(fname))
				pbar.setValue(100*n)
				n+=.5/nfiles
				QtWidgets.QApplication.processEvents()
#				print ("cellname=",cellname)
				for s1 in lines:
					s=s1.rstrip().decode("utf-8")
					#print(s)
					if re.search("PM|AM$",s)!=None:
						# get the date after that
						timeint=dt.datetime.strptime(s,"%m/%d/%Y %I:%M:%S %p")
						timest=timeint.strftime("%Y-%m-%d_%H:%M:%S")
						if priortime is None:
							timedelta=0
						else:
							timedelta=(timeint-priortime).total_seconds()
						priortime=timeint
					else:
						if self.devices=='.':
							mre=re.search("^nvme|^sd[a-l] .*$",s)
						else:
							mre=re.search("^"+self.devices+" .*$",s)
#							mre=re.search("^nvme0n1 .*$",s)
						if mre!=None:
							#disk=s[0:mre.span()[0]].rstrip()
							#print(s)
							l2f=s.split()
							#print(timeint,float(l2f[3]))
							data_list={'Cell':cellname, 'Type':('Flash' if l2f[0][0]=='n' else 'Disk'), 'Disk':l2f[0],'Metric':float(l2f[self.metric_column]),'Timestamp':timeint}
							rows_list.append(data_list)
				datfile.close()
				pbar.setValue(100*n)
				n+=.5/nfiles
				QtWidgets.QApplication.processEvents()
			self.current_metrics=pd.DataFrame(rows_list)#, ignore_index=True)
			#print(self.current_metrics.head())
			pbar.close()
		for i in self.metric_graph:
			self.metric_graph[i].remove_graph()
		for i in self.current_metrics.Cell.unique():
			self.metric_graph[i]=CellGraphrtPage(self,i,False)
			self.metric_graph[i+'A']=CellGraphrtPage(self,i,True)
			self.metric_graph[i].redraw_events()
			self.metric_graph[i+'A'].redraw_events()


	def get_prefs(self):
		qt_connect = QtWidgets.QDialog()
		if self.preferences==None:
			self.preferences=Ui_cm_pref()
		self.preferences.setupUi(qt_connect, self)
		qt_connect.exec_()
		qt_connect.show()
		qt_connect.close()
		self.metric=self.preferences.metric
		self.devices=self.preferences.devices
		self.redraw_graphs()

	def close_application(self):
		choice = QtWidgets.QMessageBox.question(self.centralwidget, 'Confirm Exit',
													"Exit the tool?",
													QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No)
		if choice == QtWidgets.QMessageBox.Yes:
					print("Exiting")
					sys.exit()
		else:
					pass

	def retranslateUi(self, CellMH):
		CellMH.setWindowTitle(_translate("CellMH", "MainWindow", None))
#		self.ChooseStats.setText(_translate("CellMH", "Pick Stats to graph ...", None))
		self.menuFile.setTitle(_translate("CellMH", "File", None))
		self.Save_to_PDF.setText(_translate("CellMH", "Save Plots to PDF ...", None))
		self.actionConfigure.setText(_translate("CellMH", "Configure ...", None))
		self.actionExit.setText(_translate("CellMH", "Exit", None))

def get_args(argv):
	try:
		opts, args = getopt.getopt(argv,"f:s:h")
	except getopt.GetoptError:
		  print ('python cellstats.py -h -s -f filename (wild cards accepted) ')
		  sys.exit(2)
	if len(opts)>0:
		devices='.'
		filename=None
		for opt,arg in opts:
				#print(opt,arg)
				if opt == '-h':
					print ('python cellstats.py -h -s device_wild_card -f filename (wild cards accepted)')
					sys.exit()
				elif opt=="-s":
					devices=arg
				elif opt =="-f":
					filename=arg
		try:
			list_of_files=[]
			#print("devices ",devices)
			if filename!=None:
				list_of_files=sorted(glob.glob(filename))
				#print(list_of_files)
				#print(filename)
				if len(list_of_files)==0:
					print ("No files found for ",filename,", please verify")
					sys.exit(2)
				else:
					return list_of_files, devices
			else:
				return list_of_files,devices
		except :
			print ("exception",sys.exc_info()[0]," on glob for",filename,", please verify")
			sys.exit(2)


if __name__ == "__main__":
	app = QtWidgets.QApplication(sys.argv)
	GraphingDynViews = QtWidgets.QMainWindow()
	if len(sys.argv)>1:
		list_of_files,devices=get_args(sys.argv[1:])
	else:
		list_of_files=None
		devices="."
	ui = Ui_CellMH()
	ui.setupUi(GraphingDynViews, list_of_files, devices)
	GraphingDynViews.show()
	sys.exit(app.exec_())
