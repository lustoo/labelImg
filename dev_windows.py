from PyQt5 import QtCore, QtGui, QtWidgets

from Ui_label_window import Ui_LabelWindow
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
import sys
import os
import lxml.etree
import xml.etree.ElementTree as ET

class LabelWindow(Ui_LabelWindow):
    def __init__(self,form=None,dir_path=None) -> None:
        super(LabelWindow,self).__init__()

        #setupUi中初始化父类组件
        self.setupUi(form)


        #后续提示窗体也要传入这个self.form,而不是self
        self.form=form
        
        #如有dir_path
        if dir_path is not None:
            #设置路径属性
            self.dir=dir_path

            #更新label
            self.label_showpath.setText(self.dir)
            self.label_showpath.repaint()


        self.do_openpath.clicked.connect(self.openpath)

        self.do_cal.clicked.connect(self.count)

        self.list_label.doubleClicked.connect(self.select_toreplace)

        self.do_changelabel.clicked.connect(self.change_label)

        self.do_copy.clicked.connect(self.toclip)

    #写入剪切板
    def toclip(self):
        import pyperclip
        if not hasattr(self,'clip'):
            return
    
        #写入剪切板
        pyperclip.copy(self.clip)

        #读取
        #pyperclip.paste()
        reply = QMessageBox.about(self.form, '提示','已复制到剪切板')




    def change_label(self):
    
        old=self.line_toreplace.text()
        new=self.line_replace.text()
        if old=='' or new=='' or old==new or not hasattr(self,'dir'):
            return
        
        #二次确认看框
        A = QMessageBox.question(self.form,'替换标签',old+' 将被替换为 '+new,QMessageBox.Yes | QMessageBox.No)

        if A == QMessageBox.No:
            return 
    
        files = os.listdir(self.dir)

        change_count=0

        for file in files:
            xml_path = os.path.join(self.dir, file)
            if not xml_path.endswith("xml"):
                continue

            try:
                xml = lxml.etree.parse(xml_path)
            except:
                print("error load:", xml_path)
                continue

            root = xml.getroot()
            # 遍历所有object元素
            for obj in root.findall('object'):
                if obj.find('name').text == old:
                    obj.find('name').text = new
                    change_count+=1
            xml.write(xml_path)# 保存修改后的XML文件
        
        #消息提示框
        reply = QMessageBox.about(self.form, '替换结果','完成{}个标签替换 请重新统计'.format(change_count))

        

    #双击列表,填充标签到需要更改的框里
    def select_toreplace(self):
        item = self.list_label.selectedItems()[0].text()
        item = item.split(' ')[-1]
        self.line_toreplace.setText(item)
        
        
    

    def openpath(self):
        dir = QtWidgets.QFileDialog.getExistingDirectory(None,"选择文件夹","")

        if dir =='':
            return 

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
        
        label_dict={}

        #统计有该标签的文件数
        xml_dict={}
        
        files = os.listdir(self.dir)
        for file in files:
            s=set()
            xml_path = os.path.join(self.dir, file)

            if not xml_path.endswith("xml"):
                continue

            try:
                xml = lxml.etree.parse(xml_path)
            except:
                print("error load:", xml_path)
                continue

            root = xml.getroot()
            # 遍历所有object元素
            for obj in root.findall('object'):
                labelname=obj.find('name').text
                s.add(labelname)
                if label_dict.get(labelname) is None:
                    label_dict[labelname]=1
                else:
                    label_dict[labelname]+=1
            
            #统计xml_dict
            for a in s:
                if xml_dict.get(a) is None:
                    xml_dict[a]=1
                else:
                    xml_dict[a]+=1

        
        clip_xml=str([xml_dict[x] for x in label_dict.keys()])
        #给剪切板,无排序
        self.clip=str(list(label_dict.keys()))+os.linesep+'object'+os.linesep+str(list(label_dict.values()))+os.linesep+'file'+os.linesep+clip_xml

        #按照数量排序并赋给self.label_dict,[('jyz_pl', 3), ('cysb_tg', 2), ('bmwh', 1)] 不是字典了               
        self.label_dict=sorted(label_dict.items(),key = lambda x:x[1],reverse = True)  

        self.xml_dict=xml_dict

        max_len_obj = max([len(str(x[1])) for x in self.label_dict])

        max_len_xml = max([len(str(x)) for x in list(xml_dict.values())])
        
        add=8

        #清空并展示列表
        self.list_label.clear()

        self.list_label.addItem('{}  {}  {}'.format('文件数'.ljust(4),'目标数'.ljust(4),'标签'))

        for _ in self.label_dict:
            k, v=_
            v=str(v)
            xml_count=str(xml_dict[k])

            #空格修正
            line='{}  {}  {}'.format(xml_count.ljust(add+max_len_xml-len(xml_count)),v.ljust(add+max_len_obj-len(v)),k )
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