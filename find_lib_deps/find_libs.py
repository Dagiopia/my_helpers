import sys
import os 

SEARCH_PATHS = ['/home/dagiopia/rasp_root/usr/lib/', '/home/dagiopia/opencog_rasp/']

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
			return f_path
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
LIBNAME = 'libcogutil.so'
l_path = search_file(LIBNAME)
deps[LIBNAME] = find_deps(l_path)
print deps
lib = LIBNAME
for dep in deps[lib]:
	fpath = search_file(dep)
	deps[name_o_path(fpath)] = find_deps(fpath)

print '\n*************DONE*************\n'
print deps

#place on a file
f = open(LIBNAME+'_deps', 'w')
for d in deps:
	f.write(d+'\n')
	for l in deps[d]:
		f.write('\t'+l+'\n')
f.close()

