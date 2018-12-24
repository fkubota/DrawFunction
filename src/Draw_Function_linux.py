# -*- coding: utf-8 -*-
"""
関数を簡単にプロットし、
画像として出力

log
2017/07/30 作成開始
2017/07/31 プロトタイプ作成
2017/08/01 ドックウィジェットを導入
2017/08/02 線の太さを変更出来るようにした

メモ
データの読み込み
グループ化
"""


import sys
from numpy import * #sinとかを普通の入力で使えるように
import PyQt4.QtGui as QG
import PyQt4.QtCore as QC
from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt4 import NavigationToolbar2QT as NavigationToolbar
import matplotlib.pyplot as plt 
import random


class InputString_And_Plot(QG.QMainWindow):   #superclassとしてQMainWindowを継承。
    def __init__(self, parent = None):
        super(InputString_And_Plot, self).__init__(parent)  #superclassのコンストラクタを使用。   
        

        self.setWindowTitle("Draw Function")
        self.setWindowIcon(QG.QIcon('../icon_file/Drow_Function_icon.png'))    #アイコンの変更。カレントディレクトリにpng形式のデータを置く。
        self.resize(850,600)
        self.move(200,50)      
        
        self.w = QG.QWidget()
        # self.w.setSizePolicy(QG.QSizePolicy.Expanding, QG.QSizePolicy.Expanding)  #できるだけ大きくなるように命令した。
        
        #matplotlibをGUI化するためのウィジェット
        self.figure = plt.figure()
        self.ax = self.figure.add_subplot(111)
        self.canvas = FigureCanvas(self.figure)
        self.canvas.setParent(parent)
        #self.canvas.setSizePolicy( QG.QSizePolicy.Expanding, QG.QSizePolicy.Expanding)
        self.toolbar = NavigationToolbar(self.canvas, self.w)

        ##### ラベル #####
        #xmin
        self.lbl_xmin = QG.QLabel(text ="xmin")
        self.lbl_xmin.setFont(QG.QFont("Segoe", 13))
        self.lbl_xmin.setFixedHeight(15)
        #xdiv
        self.lbl_xdiv = QG.QLabel(text ="xdiv")
        self.lbl_xdiv.setFont(QG.QFont("Segoe", 13))
        self.lbl_xdiv.setFixedHeight(15)
        #xmax
        self.lbl_xmax = QG.QLabel(text ="xmax")
        self.lbl_xmax.setFont(QG.QFont("Segoe", 13))
        self.lbl_xmax.setFixedHeight(15)
        #xlim
        self.lbl_xlim = QG.QLabel("xlim")
        self.lbl_xlim.setFont(QG.QFont("Segoe", 13))
        self.lbl_xlim.setFixedHeight(15)
        self.lbl_xlim.setFixedWidth(100)
        self.lbl_xlim.setAlignment(QC.Qt.AlignCenter)
        #ylim
        self.lbl_ylim = QG.QLabel("ylim")
        self.lbl_ylim.setFont(QG.QFont("Segoe", 13))
        self.lbl_ylim.setFixedHeight(15)
        self.lbl_ylim.setFixedWidth(100)
        self.lbl_ylim.setAlignment(QC.Qt.AlignCenter)
        
        ##### ラインエディット #####
        #line_func
        self.line_func = QG.QLineEdit()
        self.line_func.setFont(QG.QFont("Arial", 20))
        self.line_func.setFixedHeight(40)
        self.line_func.editingFinished.connect(self.plot)
        #line_xmin
        self.line_xmin = QG.QLineEdit()
        self.line_xmin.setText("-7")
        self.line_xmin.setFixedHeight(30)
        self.line_xmin.editingFinished.connect(self.plot)
        #line_xdiv
        self.line_xdiv = QG.QLineEdit()
        self.line_xdiv.setText("0.1")
        self.line_xdiv.setFixedHeight(30)
        self.line_xdiv.editingFinished.connect(self.plot)
        #line_xmax
        self.line_xmax = QG.QLineEdit()
        self.line_xmax.setText("7")
        self.line_xmax.setFixedHeight(30)
        self.line_xmax.editingFinished.connect(self.plot)
        #line_xlim_min
        self.line_xlim_min = QG.QLineEdit()
        self.line_xlim_min.setText("-7")
        self.line_xlim_min.setFixedHeight(30)
        self.line_xlim_min.editingFinished.connect(self.plot)
        #line_xlim_max
        self.line_xlim_max = QG.QLineEdit()
        self.line_xlim_max.setText("7")
        self.line_xlim_max.setFixedHeight(30)
        self.line_xlim_max.editingFinished.connect(self.plot)
        #line_ylim_min
        self.line_ylim_min = QG.QLineEdit()
        self.line_ylim_min.setText("-0.4")
        self.line_ylim_min.setFixedHeight(30)
        self.line_ylim_min.editingFinished.connect(self.plot)
        #line_ylim_max
        self.line_ylim_max = QG.QLineEdit()
        self.line_ylim_max.setText("1.2")
        self.line_ylim_max.setFixedHeight(30)
        self.line_ylim_max.editingFinished.connect(self.plot)
        
        ##### ボタン #####
        self.btn_clear = QG.QPushButton(text = "Clear")
        self.btn_clear.clicked.connect(self.clear_text)
        self.btn_DoIt = QG.QPushButton(text = "Do It")
        self.btn_DoIt.clicked.connect(self.plot)
        
        ##### コンボボックス #####
        #描画モード
        self.cb = QG.QComboBox()
        self.cb.addItem("Grid None")
        self.cb.addItem("Grid Major")
        self.cb.addItem("Grid Major&Minor")
        self.cb.setCurrentIndex(0)   #初期値。2番目の値。0番目が最初。
        self.cb.currentIndexChanged.connect(self.plot)
        #スケール
        #描画モード
        self.cb_scale = QG.QComboBox()
        self.cb_scale.addItem("Linear")
        self.cb_scale.addItem("Log")
        self.cb_scale.addItem("Log-Log")
        self.cb_scale.setCurrentIndex(0)   #初期値。2番目の値。0番目が最初。
        self.cb_scale.currentIndexChanged.connect(self.plot)
        
        
        ##### チェックボックス #####
        self.check_xlim = QG.QCheckBox()
        self.check_xlim.stateChanged.connect(self.plot)
        self.check_ylim = QG.QCheckBox()
        self.check_ylim.stateChanged.connect(self.plot)
        
        ##### グループボックス #####
        self.group_box_0 = QG.QGroupBox()
        self.group_box_0.setFixedHeight(75)
        self.group_box_1 = QG.QGroupBox()
        self.group_box_1.setFixedHeight(85)
        
        ##### レイアウト #####
        self.Hbox0 = QG.QHBoxLayout()
        self.Hbox0.addWidget(self.lbl_xmin)
        self.Hbox0.addWidget(self.lbl_xdiv)
        self.Hbox0.addWidget(self.lbl_xmax)
        
        self.Hbox1 = QG.QHBoxLayout()
        self.Hbox1.addWidget(self.line_xmin)
        self.Hbox1.addWidget(self.line_xdiv)
        self.Hbox1.addWidget(self.line_xmax)
        
        self.Hbox2 = QG.QHBoxLayout()
        self.Hbox2.addWidget(self.cb)
        self.Hbox2.addWidget(self.cb_scale)
        self.Hbox2.addWidget(self.btn_clear)
        self.Hbox2.addWidget(self.btn_DoIt)
    
        self.Hbox3 = QG.QHBoxLayout()
        self.Hbox3.addWidget(self.check_xlim)
        self.Hbox3.addWidget(self.lbl_xlim)
        self.Hbox3.addWidget(self.line_xlim_min)        
        self.Hbox3.addWidget(self.line_xlim_max)
        
        self.Hbox4 = QG.QHBoxLayout()
        self.Hbox4.addWidget(self.check_ylim)
        self.Hbox4.addWidget(self.lbl_ylim)
        self.Hbox4.addWidget(self.line_ylim_min)        
        self.Hbox4.addWidget(self.line_ylim_max)
        
        self.Vbox0 = QG.QVBoxLayout()
        self.Vbox0.addLayout(self.Hbox0)
        self.Vbox0.addLayout(self.Hbox1)
        
        self.group_box_0.setLayout(self.Vbox0)
        
        self.Vbox1 = QG.QVBoxLayout()
        self.Vbox1.addLayout(self.Hbox3)
        self.Vbox1.addLayout(self.Hbox4)
        
        self.group_box_1.setLayout(self.Vbox1)
        
        self.Vbox2 = QG.QVBoxLayout()
        self.Vbox2.addWidget(self.toolbar)
        self.Vbox2.addWidget(self.canvas)
        self.Vbox2.addWidget(self.line_func)
        self.Vbox2.addLayout(self.Hbox2)
        self.Vbox2.addWidget(self.group_box_0)
        self.Vbox2.addWidget(self.group_box_1)
        
        self.w.setLayout(self.Vbox2)
        self.setCentralWidget(self.w)
        
        ##### dockwidget ####
        #graph_setting
        self.make_dock_graph_setting()
        self.dock_graph_setting = QG.QDockWidget("Dock--Graph Setting")
        self.dock_graph_setting.setWidget(self.w_gs)
        self.addDockWidget(QC.Qt.RightDockWidgetArea, self.dock_graph_setting)
        #table
        self.make_dock_table()
        self.dock_table = QG.QDockWidget("Dock--Funcion Table")
        self.dock_table.setWidget(self.table)
        self.addDockWidget(QC.Qt.RightDockWidgetArea, self.dock_table)

        #プロット
        self.first_plot()
        #self.plot()
    
    
        

    def make_dock_graph_setting(self):
        self.w_gs = QG.QTableWidget()
        self.w_gs.setWindowTitle("Graph Setting")
        
        ##### ボタン #####
        self.btn_color = QG.QPushButton()
        self.btn_color.setFixedWidth(20)
        self.btn_color.setStyleSheet("background-color: #ff3773")
        self.btn_color.clicked.connect(self.change_color)
        self.btn_save_image = QG.QPushButton("透明PNG")
        self.btn_save_image.clicked.connect(self.save_func)

        ##### ラベル #####
        #self.lbl_xlim = QG.QLabel("xlim")
        #self.lbl_ylim = QG.QLabel("ylim") 
        self.lbl_marker = QG.QLabel("Marker")         
        self.lbl_markersize = QG.QLabel("Size")  
        self.lbl_linewidth = QG.QLabel("LineWidth")
        
        ##### ラインエディット #####
        self.line_marker = QG.QLineEdit()
        self.line_marker.editingFinished.connect(self.plot)
        self.line_marker.setText("None")
        self.line_markersize = QG.QLineEdit()
        self.line_markersize.setText("5")
        self.line_markersize.editingFinished.connect(self.plot)
        self.line_linewidth = QG.QLineEdit()
        self.line_linewidth.setText("3")
        self.line_linewidth.editingFinished.connect(self.plot)
        
        ##### テーブル #####
        self.table_marker = QG.QTableWidget()
        self.table_marker.setWindowTitle("Maker Table")
        self.table_marker.setRowCount(8)
        self.table_marker.setColumnCount(5)
        self.table_marker.setColumnWidth(0,40)
        self.table_marker.setColumnWidth(1,40)
        self.table_marker.setColumnWidth(2,40)
        self.table_marker.setColumnWidth(3,40)
        self.table_marker.setItem(0,0, QG.QTableWidgetItem("None"))
        self.table_marker.setItem(0,1, QG.QTableWidgetItem("$abc$"))
        self.table_marker.setItem(0,2, QG.QTableWidgetItem("."))
        self.table_marker.setItem(0,3, QG.QTableWidgetItem(","))
        self.table_marker.setItem(1,0, QG.QTableWidgetItem("o"))
        self.table_marker.setItem(1,1, QG.QTableWidgetItem("v"))
        self.table_marker.setItem(1,2, QG.QTableWidgetItem("^"))
        self.table_marker.setItem(1,3, QG.QTableWidgetItem("<"))
        self.table_marker.setItem(2,0, QG.QTableWidgetItem(">"))
        self.table_marker.setItem(2,1, QG.QTableWidgetItem("1"))
        self.table_marker.setItem(2,2, QG.QTableWidgetItem("2"))
        self.table_marker.setItem(2,3, QG.QTableWidgetItem("3"))
        self.table_marker.setItem(3,0, QG.QTableWidgetItem("4"))
        self.table_marker.setItem(3,1, QG.QTableWidgetItem("8"))
        self.table_marker.setItem(3,2, QG.QTableWidgetItem("s"))
        self.table_marker.setItem(3,3, QG.QTableWidgetItem("p"))
        self.table_marker.setItem(4,0, QG.QTableWidgetItem("*"))
        self.table_marker.setItem(4,1, QG.QTableWidgetItem("h"))
        self.table_marker.setItem(4,2, QG.QTableWidgetItem("H"))
        self.table_marker.setItem(4,3, QG.QTableWidgetItem("+"))
        self.table_marker.setItem(5,0, QG.QTableWidgetItem("x"))
        self.table_marker.setItem(5,1, QG.QTableWidgetItem("D"))
        self.table_marker.setItem(5,2, QG.QTableWidgetItem("d"))
        self.table_marker.setItem(5,3, QG.QTableWidgetItem("|"))
        self.table_marker.setItem(6,0, QG.QTableWidgetItem("_"))
        
        self.table_marker.cellClicked.connect(self.print_marker)
        
        
        
        
        ##### レイアウト #####
        self.Hbox_gs_0 = QG.QHBoxLayout()
        self.Hbox_gs_0.addWidget(self.btn_color)
        self.Hbox_gs_0.addWidget(self.btn_save_image)  
        
        self.Hbox_gs_1 = QG.QHBoxLayout()
        self.Hbox_gs_1.addWidget(self.lbl_linewidth)
        self.Hbox_gs_1.addWidget(self.line_linewidth)   
        
        #self.Hbox_gs_2 = QG.QHBoxLayout()
        #self.Hbox_gs_2.addWidget(self.lbl_ylim)
        #self.Hbox_gs_2.addWidget(self.line_ylim_min)        
        #self.Hbox_gs_2.addWidget(self.line_ylim_max)
        
        self.Hbox_gs_3 = QG.QHBoxLayout()
        self.Hbox_gs_3.addWidget(self.lbl_marker)
        self.Hbox_gs_3.addWidget(self.line_marker)
        self.Hbox_gs_3.addWidget(self.lbl_markersize)
        self.Hbox_gs_3.addWidget(self.line_markersize)
        
        self.Vbox_gs = QG.QVBoxLayout()
        self.Vbox_gs.addLayout(self.Hbox_gs_0)
        #self.Vbox_gs.addLayout(self.Hbox_gs_1)
        #self.Vbox_gs.addLayout(self.Hbox_gs_2)
        self.Vbox_gs.addLayout(self.Hbox_gs_3)
        self.Vbox_gs.addLayout(self.Hbox_gs_1)
        self.Vbox_gs.addWidget(self.table_marker)
        
        self.w_gs.setLayout(self.Vbox_gs)
        
        
        
    def make_dock_table(self):
        self.table = QG.QTableWidget()
        self.table.setWindowTitle("Function Table")
        self.table.setRowCount(12)
        self.table.setColumnCount(10)

        self.table.setItem(0,0, QG.QTableWidgetItem("+"))
        self.table.setItem(0,1, QG.QTableWidgetItem("-"))
        self.table.setItem(0,2, QG.QTableWidgetItem("*"))
        self.table.setItem(0,3, QG.QTableWidgetItem("/"))
        self.table.setItem(1,0, QG.QTableWidgetItem("x"))
        self.table.setItem(1,1, QG.QTableWidgetItem("x**2"))
        self.table.setItem(1,2, QG.QTableWidgetItem("x**3"))
        self.table.setItem(1,3, QG.QTableWidgetItem("x**4"))
        self.table.setItem(1,4, QG.QTableWidgetItem("x**5"))
        self.table.setItem(1,5, QG.QTableWidgetItem("x**6"))
        self.table.setItem(2,0, QG.QTableWidgetItem("sin(x)"))
        self.table.setItem(2,1, QG.QTableWidgetItem("cos(x)"))
        self.table.setItem(2,2, QG.QTableWidgetItem("tan(x)"))
        self.table.setItem(3,0, QG.QTableWidgetItem("arcsin(x)"))
        self.table.setItem(3,1, QG.QTableWidgetItem("arccos(x)"))
        self.table.setItem(3,2, QG.QTableWidgetItem("arctan(x)"))
        self.table.setItem(4,0, QG.QTableWidgetItem("sinh(x)"))
        self.table.setItem(4,1, QG.QTableWidgetItem("cosh(x)"))        
        self.table.setItem(4,2, QG.QTableWidgetItem("tanh(x)"))
        self.table.setItem(5,0, QG.QTableWidgetItem("arcsinh(x)"))
        self.table.setItem(5,1, QG.QTableWidgetItem("arccosh(x)"))
        self.table.setItem(5,2, QG.QTableWidgetItem("arctanh(x)"))
        self.table.setItem(6,0, QG.QTableWidgetItem("exp(x)"))
        self.table.setItem(6,1, QG.QTableWidgetItem("log(x)"))
        self.table.setItem(6,2, QG.QTableWidgetItem("log2(x)"))
        self.table.setItem(6,3, QG.QTableWidgetItem("log10(x)"))
        self.table.setItem(7,0, QG.QTableWidgetItem("sinc(x)"))
        self.table.setItem(7,1, QG.QTableWidgetItem("exp(-(x-1)**2)"))
        self.table.setItem(7,2, QG.QTableWidgetItem("1/((x-1)**2 + 1)"))
        self.table.setItem(8,0, QG.QTableWidgetItem("pi"))
        self.table.setItem(8,1, QG.QTableWidgetItem("e"))        
        
        self.table.cellClicked.connect(self.print_text)
        
        
        
        
    def plot(self):
        global x,y
        xmin = float( self.line_xmin.text() )
        xmax = float( self.line_xmax.text() )
        xdiv = float( self.line_xdiv.text() )
        xlim_min = float( self.line_xlim_min.text() )
        xlim_max = float( self.line_xlim_max.text() )
        ylim_min = float( self.line_ylim_min.text() )
        ylim_max = float( self.line_ylim_max.text() )
        x = arange(xmin, xmax, xdiv)
        
        #読み込んだテキストをyに代入
        func_exec = "y=" + self.line_func.text()  
        exec(func_exec, globals())  #execはstrをスクリプトのように扱うことができる。exec("print("Hellow World")")とか。 
        
        #プロット
        self.ax.clear()
        self.ax.set_xlabel("x", fontsize=18)
        self.color_name = self.btn_color.palette().button().color().name()
        self.ax.plot(x,y, color = self.color_name, linewidth=float(self.line_linewidth.text()), marker=self.line_marker.text(), markersize=float(self.line_markersize.text()))   
        
        if self.cb.currentIndex()==0:
            plt.grid(which='major',color='black',linestyle='')
            plt.grid(which='minor',color='black',linestyle='')
        if self.cb.currentIndex()==1:
            plt.grid(which='major',color='black',linestyle='-')
            plt.grid(which='minor',color='black',linestyle='') 
        if self.cb.currentIndex()==2:
            plt.grid(False)
            plt.grid(which='major',color='black',linestyle='-')
            plt.grid(which='minor',color='black',linestyle=':')            
            
        
        if self.check_xlim.isChecked():        
            self.ax.set_xlim([xlim_min,xlim_max])
        if self.check_ylim.isChecked():   
            self.ax.set_ylim([ylim_min,ylim_max])
            
        if self.cb_scale.currentIndex()==0:
            plt.xscale("linear")
            plt.yscale("linear")
        if self.cb_scale.currentIndex()==1:
            plt.xscale("log")
            plt.yscale("linear")
        if self.cb_scale.currentIndex()==2:
            plt.xscale("log")
            plt.yscale("log")
        
        self.canvas.draw()
        
    
    def clear_text(self):
        self.line_func.setText("")
    
    
    def print_text(self, row, col):
        self.line_func.setText( self.line_func.text() +  self.table.item(row,col).text() ) 
    
    def print_marker(self, row, col):
        self.line_marker.setText( self.table_marker.item(row,col).text() ) 
        self.plot()
        
    def change_color(self):
        self.color = QG.QColorDialog.getColor()
        self.btn_color.setStyleSheet("background-color: %s" %self.color.name())
        self.plot()
        
        
    def save_func(self):
        #色と保存先の取得
        self.color_func = self.btn_color.palette().button().color().name()
        self.file_name = QG.QFileDialog.getSaveFileName(self, "Save File",  "FunctionImage", ".png")     #保存するファイル名を取得。
        #プロットと保存
        plt.plot(x,y, color = self.color_func)   #x,yはグローバル
        plt.axis("off")
        
        plt.savefig(self.file_name, transparent=True, dpi=600)
        
        self.plot() #plt.plotしたら少し見た目が変わるので。
        
        
    def first_plot(self):
        self.List_function = ["x","x**2","x**3","sin(x)","cos(x)","tan(x)","arcsin(x)","arccos(x)","arctan(x)","sinh(x)","cosh(x)","tanh(x)","exp(x)","log(x)","log2(x)","log10(x)","sinc(x)","exp(-(x-1)**2)","1/((x-1)**2 + 1)"]                   
        self.List_operator = ["+","-","*","/"]        

        rand_num = random.randint(1,3)
        
        
        first_text = ""
        for i in range(rand_num):
            rand_func = random.randint(0,18)   #0~5までのランダムな数()。 5も入る。
            first_text = first_text + self.List_function[rand_func] 
            
            if i == rand_num-1:  #最後の一回は演算子書かない。
                pass
            else:
                rand_ope = random.randint(0,3)
                first_text = first_text + self.List_operator[rand_ope] 
            
    
        self.line_func.setText(first_text)
        self.plot()

            
            
        
    


def main():
    app = QG.QApplication(sys.argv)
    
    myGUI = InputString_And_Plot()
    
    #time.sleep(1.0) #sleep(秒指定)
    #myGUI.www.close()
    
    myGUI.show()
    
    sys.exit(app.exec_())



if __name__ == '__main__':
    main()
