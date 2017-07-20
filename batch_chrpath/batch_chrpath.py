#!/usr/bin/env python 
import os, sys

SEARCH_PATH = '/home/icog2/RPI/opencog_rpi_toolchain/opencog_rasp/usr/local'
FAKE_ROOT = ['/home/icog2/RPI/opencog_rpi_toolchain/opencog_rasp', '/home/icog2/RPI/opencog_rpi_toolchain/needed_libs']


def mod_rpath():
        s_path = SEARCH_PATH
        sin, sout = os.popen4(['find', '-P', s_path, '-type', 'f', '-name', '*.so'])
        srs = sout.readlines()
        srs = [srs[i][:-1] if srs[i].count('\n')>0 else srs[i] for i in range(len(srs))]
	for f in srs:
		sin, sout = os.popen4(['chmod', '+x', f])
	#this seems redundant but is included so that not just shared libraries but
	#executables like cogserver are included too.
	#so make all shared libs executable then search for executables
	sin, sout = os.popen4(['find', '-P', s_path, '-type', 'f', '-executable'])
	srs = sout.readlines()
	srs = [srs[i][:-1] if srs[i].count('\n')>0 else srs[i] for i in range(len(srs))]

	for f in srs:
		sin, sout = os.popen4(['chrpath', '-l', f])
		res = sout.readlines()
		res = res[0][res[0].index('RPATH=')+6:-1]
		for fr in FAKE_ROOT:
			res = res.replace(fr, '')
		sin, sout = os.popen4(['chrpath', f, '-r', res])
		chres = sout.readlines()
		print chres


if __name__ == "__main__":
	mod_rpath()
