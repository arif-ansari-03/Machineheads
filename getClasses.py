from xml.dom import minidom
import os
import glob

def getClasses():
    cl_list = []
    print("1")
    for fname in glob.glob("*.xml"):
        xmldoc = minidom.parse(fname)
        itemlist = xmldoc.getElementsByTagName('object')
        for item in itemlist:
            classid =  (item.getElementsByTagName('name')[0]).firstChild.data
            if (classid not in cl_list):
                cl_list.append(classid)
            
    print(cl_list)
            

def main():
    getClasses()
    


if __name__ == '__main__':
    print(os.getcwd())
    main()
