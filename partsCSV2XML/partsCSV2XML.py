#!/usr/bin/env python

'''
  generate dataset xml file similar to the imglab tool from dlib
  it takes a csv file created by get_faces tool in tis repo

  run:
    ./partsCSV2XML 0,1,2,3,... csv_file

  the numbers are the part points in the csv, if none given, tthen
  all of them.
'''

import csv
import lxml.etree as xml
import sys

elroot = xml.Element('dataset')
elname = xml.Element('name')
elcomment = xml.Element('comment')
elimages = xml.Element('images')

elname.text = "partsCSV2XML dataset"
elcomment.text = "Created by partsCSV2XML tool"
elroot.append(elname)
elroot.append(elcomment)
elroot.append(elimages)

part_name = {0: 'j0', 1: 'j1', 2: 'j2', 3: 'j3',
	     4: 'j4', 5: 'j5', 6: 'j6', 7: 'j7',
	     8: 'j8', 9: 'j9', 10: 'j10', 11: 'j11',
	     12: 'j12', 13: 'j13', 14: 'j14', 15: 'j15',
	     16: 'j16', 17: 'rel1', 18: 'rel2', 19: 'rel3',
	     20: 'rel4', 21: 'rel5', 22: 'lel1', 23: 'lel2',
	     24: 'lel3', 25: 'lel4', 26: 'lel5', 27: 'n1',
	     28: 'n2', 29: 'n3', 30: 'n4', 31: 'n5', 32: 'n6',
	     33: 'n7', 34: 'n5', 35: 'n6', 36: 're1', 37: 're2',
	     38: 're3', 39: 're4', 40: 're5', 41: 're6',
	     42: 'le1', 43: 'le2', 44: 'le3', 45: 'le4',
	     46: 'le5', 47: 'le6', 48: 'm1', 49: 'm2',
	     50: 'm3', 51: 'm4', 52: 'm5', 53: 'm6', 54: 'm7',
	     55: 'm8', 56: 'm9', 57: 'm10', 58: 'm11',
	     59: 'm12', 60: 'm13', 61: 'm14', 62: 'm15',
	     63: 'm16', 64: 'm17', 65: 'm18', 66: 'm19',
	     67: 'm20'}

parts = []
csv_file = ''

if 2 == len(sys.argv):
    csv_file = sys.argv[1]

if 3 == len(sys.argv):
    print parts
    parts = sys.argv[1].split(',')
    parts = [int(i) for i in parts]
    csv_file = sys.argv[2]

print "Using CSV file: ", csv_file
print "Number of Parts: ", len(parts)
csvf = csv.reader(open(csv_file, 'r'))

for l in csvf:
    elimage = xml.Element('image', {'file': l[0]})
    elbox = xml.Element('box', {'top': '0', 'left': '0', 'width': l[1], 'height': l[2]})
    ellabel = xml.Element('label')
    ellabel.text = "face"
    elimage.append(ellabel)
    i = 0
    for p in range(3, len(l)-3, 2):
        if 0 == len(parts) or 0 != parts.count(i):
	    elpart = xml.Element('part', {'name': part_name[i], 'x': l[p], 'y': l[p+1]})
	    elbox.append(elpart)
	i += 1
    elimage.append(elbox)
    elimages.append(elimage)

et = xml.ElementTree(elroot)
et.write('dataset.xml', encoding='ISO-8859-1', pretty_print=True, xml_declaration=True)
