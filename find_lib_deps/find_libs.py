#!/usr/bin/env python
import sys
import os 
import numpy as np

SEARCH_PATHS = ['PATH1', 'PATH2']

name_o_path = lambda s : s[s.rfind('/')+1:]

def search_file(fname):
	f_path = ''
	print "Searching for file : <", fname,  ">"
	for path in SEARCH_PATHS:
		sin, sout = os.popen4(['find', '-P', path, '-name', fname ])
		res = sout.readlines()
		for i in range(len(res)):
			res[i] = res[i].replace('\n', '')
		#print res
		if len(res) == 0:
			print "Not found in PATH:", path
		elif len(res) == 1:
			f_path = res[0]
			print "One result found: ", f_path
		else:
			print "Multiple found!"
			for r in res:
				print '\t', r
				#print 'Reading link:'
				#print os.readlink(r)
			print "Taking the first result."
			f_path = res[0]
		return f_path

def find_deps(lib_path):
	l_deps = []
	LIB_NAME = name_o_path(lib_path)
	print 'PATH:', lib_path
	print 'NAME:', LIB_NAME
	sin, sout = os.popen4(['objdump', '-p', lib_path])
	res = sout.readlines()
	for r in res:
		if r.count('NEEDED') > 0:
			l_deps.append(r[r.rfind(' ')+1:-1])
	return l_deps


deps = {}
libs = []
l_deps = []
LIBNAME = ''
if len(sys.argv) == 3:
	LIBNAME = name_o_path(sys.argv[1])
else:
	LIBNAME = sys.argv[1]
l_path = search_file(LIBNAME)
if l_path is None:
	exit()
deps[LIBNAME] = find_deps(l_path)
libs.append(LIBNAME)
l_deps.append(find_deps(l_path))
print deps
lib = LIBNAME
for dep in deps[lib]:
	fpath = search_file(dep)
	deps[name_o_path(fpath)] = find_deps(fpath)
	libs.append(name_o_path(fpath))
	l_deps.append(find_deps(fpath))

ld_f = []
for l in l_deps:
	for m in l:
		ld_f.append(m)
for l in ld_f:
	if libs.count(l) > 0:
		continue
	libs.append(l)
	l_deps.append(find_deps(search_file(l)))

print '\n*************DONE*************\n'
print deps


#place on a file
f = open(LIBNAME+'_deps', 'w')
for i in range(len(libs)):
        f.write(libs[i]+'\n')
        for l in l_deps[i]:
                f.write('\t'+l+'\n')
f.close()


