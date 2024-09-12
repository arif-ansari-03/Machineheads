import random
from xml.dom import minidom
import os
import glob

lut = {
    "D00": 0, "D01": 1, "D10": 2, "D11": 3, "D20": 4,
    "D40": 5, "D43": 6, "D44": 7, "D50": 8
}

def convert_coordinates(size, box):
    dw = 1.0 / size[0]
    dh = 1.0 / size[1]
    x = (box[0] + box[1]) / 2.0
    y = (box[2] + box[3]) / 2.0
    w = box[1] - box[0]
    h = box[3] - box[2]
    x = x * dw
    w = w * dw
    y = y * dh
    h = h * dh
    return (x, y, w, h)

def collect_annotations(lut):
    d10_files = []
    other_files = []

    for fname in glob.glob("*.xml"):
        xmldoc = minidom.parse(fname)
        itemlist = xmldoc.getElementsByTagName('object')

        has_d10 = False
        for item in itemlist:
            classid = (item.getElementsByTagName('name')[0]).firstChild.data
            if classid == "D10":
                has_d10 = True

        if has_d10:
            d10_files.append(fname)
        else:
            other_files.append(fname)

    return d10_files, other_files

def convert_xml2yolo(lut, d10_files, other_files):
    selected_other_files = random.sample(other_files, len(d10_files))

    for fname in d10_files + selected_other_files:
        xmldoc = minidom.parse(fname)
        fname_out = (fname[:-4] + '.txt')

        with open(fname_out, "w") as f:
            itemlist = xmldoc.getElementsByTagName('object')
            size = xmldoc.getElementsByTagName('size')[0]
            width = int((size.getElementsByTagName('width')[0]).firstChild.data)
            height = int((size.getElementsByTagName('height')[0]).firstChild.data)

            for item in itemlist:
                classid = (item.getElementsByTagName('name')[0]).firstChild.data
                if classid in lut:
                    label_str = str(lut[classid])
                    xmin = ((item.getElementsByTagName('bndbox')[0]).getElementsByTagName('xmin')[0]).firstChild.data
                    ymin = ((item.getElementsByTagName('bndbox')[0]).getElementsByTagName('ymin')[0]).firstChild.data
                    xmax = ((item.getElementsByTagName('bndbox')[0]).getElementsByTagName('xmax')[0]).firstChild.data
                    ymax = ((item.getElementsByTagName('ymax')[0]).firstChild.data
                    b = (float(xmin), float(xmax), float(ymin), float(ymax))
                    bb = convert_coordinates((width, height), b)

                    f.write(label_str + " " + " ".join([("%.6f" % a) for a in bb]) + '\n')

        print("wrote %s" % fname_out)

def main():
    d10_files, other_files = collect_annotations(lut)
    convert_xml2yolo(lut, d10_files, other_files)

if __name__ == '__main__':
    main()
