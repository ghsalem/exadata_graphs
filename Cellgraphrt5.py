import subprocess
import os

import pandas as pd
import numpy as np
from PyQt5 import QtCore, QtWidgets, QtWidgets
from matplotlib import pyplot as plt

from matplotlib import dates as mdates
from matplotlib.pyplot import cm
import datetime as dt
from matplotlib import rcParams
from matplotlib.backends.backend_qt5 import NavigationToolbar2QT as NavigationToolbar
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import mplcursors

class CellGraphrtPage:

	def __init__(self,obj, cell, avg):
		self.figure=""
		rcParams.update({'figure.autolayout': True})
		self.class_sql_text=""
		self.chosen_class=""
		self.lines=dict()
		self.graph=""
		self.avg=avg
		self.parent=obj
		self.qfigwidget=QtWidgets.QWidget(self.parent.ga_sa_contents)
		winWidth = 383
		winHeight = 384
		self.dpi=100
		self.figure=plt.Figure((winWidth/self.dpi, winHeight/self.dpi), dpi=self.dpi)#MplCanvas(self.parent.ga_sa_contents)#self.parent.GraphScrollArea)
		self.canvas=FigureCanvas(self.figure)
		self.canvas.setParent(self.qfigwidget)
		self.navi_toolbar = NavigationToolbar(self.canvas,self.qfigwidget)#self.parent.centralwidget)
		self.plotLayout = QtWidgets.QVBoxLayout()
		self.plotLayout.addWidget(self.canvas)
		self.plotLayout.addWidget(self.navi_toolbar)
		self.qfigwidget.setLayout(self.plotLayout)
		self.parent.ga_vert_layout.addWidget(self.qfigwidget)
		self.ax=None
		self.old_waits=""
		self.dpi=self.figure.dpi
		self.begin_date=None
		self.all_data=None
		self.sysdate=True
		self.metric_name=self.parent.metric
		self.first_time=True
		self.starting_date=(dt.datetime.now()-dt.timedelta(minutes=5)).strftime(' %Y-%m-%dT%H:%M:%S+01:00')
		self.xfmt = mdates.DateFormatter('%H:%M:%S')
		self.canvas.setMinimumSize(self.canvas.size())
		self.cell=cell
		if self.parent.list_of_files is None:
			self.redraw_events()

	def remove_graph(self):
		self.parent.ga_vert_layout.removeWidget(self.qfigwidget)

	def redraw_events(self):
				self.metric="Metric"
				#print("metric ",self.metric)
				#self.all_data=self.parent.current_metrics[self.parent.current_metrics['Cell']==self.cell].copy(deep=True)
				seconds_diff=dict()
				if self.avg:
					col='Type'
					self.all_data=self.parent.current_metrics[self.parent.current_metrics['Cell']==self.cell].groupby(['Cell','Type','Timestamp']).sum().reset_index()
					list_disks_u=list(self.all_data.Type.unique())
					lab_add='(Sum of '+self.metric+' per type)'
				else:
					col='Disk'
					self.all_data=self.parent.current_metrics[self.parent.current_metrics['Cell']==self.cell].copy(deep=True)
					list_disks_u=list(self.all_data.Disk.unique())
					lab_add='('+self.metric_name+' per device)'
				#print (current_metrics)
				#print(self.metric)
				if self.ax is None:
					self.ax=self.figure.add_axes([.06,.15,.75,.80])
					self.ax2=self.ax.twinx()
					self.ax.set_facecolor('w')
				xticklabels=list(self.all_data['Timestamp'])
				#print(list_cells_u)
				xtickmin=xticklabels[0]
				xtickmax=xticklabels[len(xticklabels)-1]
				#print(@neticks)
				xticks=np.arange(len(xticklabels))
				#print("TS: ",len(xticks))
				color=iter(cm.rainbow(np.linspace(0,1,len(list_disks_u))))
				self.ax.cla()
				self.ax2.cla()
				stacked_data=[]
				nbr_lines1=0
				nbr_lines2=0
				for n,i in enumerate(list_disks_u):
					#print("i=",i," col=",col)
					if self.all_data[self.all_data[col]==i].Metric.max()>0:
						color_n=next(color)
#						mindelta=self.all_data[self.all_data['Disk']==i]['DELTA'][1:].min()
						xticklabels=list(self.all_data[self.all_data[col]==i]['Timestamp'])
#						if mindelta<0:
						total_waits=self.all_data[self.all_data[col]==i][self.metric]
						total_waits=pd.Series(total_waits)
						if len(total_waits)>20:
							total_waits.rolling(window=5,center=True).mean()
						if i[0]=='n' or i=='Flash':
							l1=self.ax.plot(xticklabels,total_waits, color=color_n,label=i)
							mplcursors.cursor(l1)
							nbr_lines1+=1
						else:
							l2=self.ax2.plot(xticklabels,total_waits, color=color_n,label=i)
							mplcursors.cursor(l2)
							nbr_lines2+=1
				if nbr_lines1+nbr_lines2>0:
					self.ax.xaxis.set_major_formatter(self.xfmt)
					#self.ax.set_xticks(xticklabels)
					#print(xtickmin,xtickmax)
#						 self.ax.set_xticklabels(xticklabels,  rotation=45, fontsize=8, ha='center')
					self.ax.set_xlim([xtickmin,xtickmax])
					for tick in self.ax.xaxis.get_major_ticks():
						tick.label.set_fontsize(8)
						tick.label.set_rotation(40)
					for tick in self.ax.yaxis.get_major_ticks():
						tick.label.set_fontsize(8)
#					self.ax.yaxis.tick_right() #params(axis='y', direction='in')
					if nbr_lines1>0:
						self.ax.legend(loc='center right', bbox_to_anchor=(0.1,.8),
							fontsize=8, ncol=1,fancybox=True, shadow=True)
					if nbr_lines2>0:
						self.ax2.legend(loc='center left', bbox_to_anchor=(1.1,.5),
							fontsize=8, ncol=1,fancybox=True, shadow=True)
					self.ax.set_title(self.cell+lab_add, fontsize=8)
#					mplcursors.cursor()					
					self.canvas.draw()
