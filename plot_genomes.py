#!/usr/bin/python
import httplib
import sys
from optparse import OptionParser
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np

def main():
	helpStr = '\n'+sys.argv[0]+' downloads a record of all prokaryote, eukaryote, and virus genomes from NCBI genome and plots the number completed by year.'
	parser = OptionParser(usage = "usage: %prog -o EXT\n"+helpStr)
	parser.add_option('-o','--out',dest='outFormat',help='Output figure format [emf, eps, pdf, png, ps, raw, rgba, svg, svgz]',metavar='Ext')
	(options,args) = parser.parse_args()
	if not options.outFormat:
		parser.print_help()
		parser.error("Output figure format (-o) required")
	if not options.outFormat not in ['emf',' eps',' pdf',' png',' ps',' raw',' rgba',' svg',' svgz']:
		parser.print_help()
		parser.error("Please choose a format from [emf, eps, pdf, png, ps, raw, rgba, svg, svgz]")
	files = ('eukaryotes.txt','prokaryotes.txt','viruses.txt')
	plt.figure()
	for f in files:
		tsv = get_tsv(f)
		years = parse(tsv, f)
		name = f.split('.')[0]
		plotType(years, name.capitalize())
	plt.xlabel('Year')
	plt.ylabel('Genomes')
	plt.legend(loc=2)
	plt.title('Complete Genomes in NCBI')
	plt.savefig('genome_completed.'+options.outFormat)

def makeXY(years):
	X = np.unique(years) #these are sorted
	bc = np.bincount(years)
	Y = []
	total = 0
	for year in X:
		total += bc[year]
		Y.append(total)
	return (X,Y)

def plotType(years,label):
	X,Y = makeXY(years)
	if X[-1] == 2014:
		X = X[:-1]
		Y = Y[:-1]
	plt.plot(X,Y,label=label,linewidth=3)

def get_tsv(file):
	reportFolder = "ftp.ncbi.nlm.nih.gov"
	conn = httplib.HTTPConnection(reportFolder)
	conn.request("GET","/genomes/GENOME_REPORTS/"+file)
	r1 = conn.getresponse()
	data = r1.read()
	conn.close()
	return data

def parse(tsv, fName):
	years = []
	typeDict = {'prokaryotes.txt':(0,16,18),'viruses.txt':(0,12,14),'eukaryotes.txt':(0,16,18)}
	lines = tsv.split('\n')
	for line in lines:
		if line:
			tmp = line.split('\t')
			name = tmp[typeDict[fName][0]]
			date = tmp[typeDict[fName][1]]
			status = tmp[typeDict[fName][2]]
			if fName[0] == 'p' or fName[0] == 'v':
				if status == 'Complete' and date != '-':
					year = date.split('/')[0]
					years.append(int(year))
			else:
				if status == 'Chromosomes' and date != '-':
					year = date.split('/')[0]
					years.append(int(year))
	return years

if __name__ == "__main__":
	main()
