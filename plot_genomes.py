#!/usr/bin/python
try: import urllib2
except: import urllib.request as urllib2
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
		years = parse(f)
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
	plt.plot(X,Y,label=label,linewidth=3)

def parse(fName):
	years = []
	url_base = "ftp://ftp.ncbi.nlm.nih.gov/genomes/GENOME_REPORTS/"
	url = "%s/%s"%(url_base, fName)
	typeDict = {'prokaryotes.txt':(0,13,15),'viruses.txt':(0,12,14),'eukaryotes.txt':(0,14,16)}
	data = ""
	chunk = True
	resp = urllib2.urlopen(url)
	while chunk:
		chunk = resp.read()
		data += chunk
	data = data.split('\n')
	for i,line in enumerate(data):
		if line and line[0] != "#":
			tmp = line.rstrip('\n').split('\t')
			try:
				name = tmp[typeDict[fName][0]]
				date = tmp[typeDict[fName][1]]
				status = tmp[typeDict[fName][2]]
			except:
				print fName
				print line
				print data[i+1]
				for i,w in enumerate(tmp): print i,w
				break
			if fName[0] == 'p' or fName[0] == 'v':
				if 'Complete' in status and date != '-':
					year = date.split('/')[0]
					years.append(int(year))
			else:
				if ('Chromosome' in status or 'Complete' in status) and date != '-':
					year = date.split('/')[0]
					years.append(int(year))
	return years

if __name__ == "__main__":
	main()
