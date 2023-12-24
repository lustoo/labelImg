from PyQt5 import QtCore, QtGui, QtWidgets

from Ui_label_window import Ui_LabelWindow
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
import sys

class LabelWindow(Ui_LabelWindow):
    def __init__(self,form=None,dir_path=None) -> None:
        super(LabelWindow,self).__init__()

        #setupUi中初始化父类组件
        self.setupUi(form)
        
        #如有dir_path
        if dir_path is not None:
            #设置路径属性
            self.dir=dir_path

            #更新label
            self.label_showpath.setText(self.dir)
            self.label_showpath.repaint()


        self.do_openpath.clicked.connect(self.openpath)
        self.do_cal.clicked.connect(self.count)
        

    
    def openpath(self):
        dir = QtWidgets.QFileDialog.getExistingDirectory(None,"选择文件夹","")

        #设置路径属性
        self.dir=dir

        #更新label
        self.label_showpath.setText(self.dir)
        self.label_showpath.repaint()
        
        #设置悬停提示
        self.label_showpath.setToolTip(dir)

    
    def count(self):

        #判断类内是否存在属性
        if not hasattr(self,'dir') :

            return
        import os
        import lxml.etree
        import glob
        import xml.etree.ElementTree as ET

        label_dict={}
        
        files = os.listdir(self.dir)
        for file in files:
            xml_path = os.path.join(self.dir, file)

            if not xml_path.endswith("xml"):
                continue

            try:
                xml = lxml.etree.parse(xml_path)
            except:
                print("error load:", xml_path)

            root = xml.getroot()
            # 遍历所有object元素
            for obj in root.findall('object'):
                labelname=obj.find('name').text
                if label_dict.get(labelname) is None:
                    label_dict[labelname]=1
                else:
                    label_dict[labelname]+=1

        #按照数量排序并赋给self.label_dict,[('jyz_pl', 3), ('cysb_tg', 2), ('bmwh', 1)] 不是字典了               
        self.label_dict=sorted(label_dict.items(),key = lambda x:x[1],reverse = True)  

        #print(self.label_dict)

        
        max_len = max([len(str(x[1])) for x in self.label_dict])

        for _ in self.label_dict:
            k, v=_
            line='{}  {}'.format(str(v).rjust(max_len),k )
            print(line)
            self.list_label.addItem(line)
            #self.list_num.addItem(str(v))




        

        



if __name__ == '__main__':
    app = QApplication(sys.argv)
    MainWindow = QMainWindow()
    ui =LabelWindow()  
    ui.initUI()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())