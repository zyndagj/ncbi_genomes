import numpy as np
import matplotlib.pyplot as plt

#ftp://ftp.ncbi.nlm.nih.gov/genomes/GENOME_REPORTS/

def parseP(inFile):
	#Organism/Name, TaxID, BioProject Accession, BioProject ID, Group, SubGroup, Size (Mb), GC%, Chromosomes/RefSeq, Chromosomes/INSDC, Plasmids/RefSeq, Plasmids/INSDC, WGS, Scaffolds, Genes, Proteins, Release Date, Modify Date, Status, Center, BioSample Accession, Assembly Accession, Reference
	IF = open(inFile,'r')
	years = []
	for line in IF:
		tmp = line.rstrip('\n').split('\t')
		name = tmp[0]
		date = tmp[16]
		status = tmp[18]
		if status == "Complete" and date != "-":
			year = date.split('/')[0]
			years.append(int(year))
			#print name, date, status
	IF.close()
	return years

def parseV(inFile):
	#Organism/Name, TaxID, BioProject Accession, BioProject ID, Group, SubGroup, Size (Kb), GC%, Host, Segmemts, Genes, Proteins, Release Date, Modify Date, Status
	IF = open(inFile,'r')
	years = []
	for line in IF:
		tmp = line.rstrip('\n').split('\t')
		name = tmp[0]
		date = tmp[12]
		status = tmp[14]
		if status == "Complete" and date != '-':
			year = date.split('/')[0]
			years.append(int(year))
			#print name, date, status
	IF.close()
	return years

def parseE(inFile):
	#Organism/Name	TaxID	BioProject Accession	BioProject ID	Group	SubGroupSize (Mb)	GC%	Assembly Accession	Chromosomes	Organelles	Plasmids	WGS	Scaffolds	Genes	Proteins	Release Date	Modify Date	Status	Center	BioSample Accession
	IF = open(inFile,'r')
	years = []
	for line in IF:
		tmp = line.split('\t')
		name = tmp[0]
		chroms = tmp[9]
		date = tmp[16]
		status = tmp[18]
		if status == "Chromosomes":
			year = date.split('/')[0]
			years.append(int(year))
			#print name,chroms,date,status
	IF.close()
	return years

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

Eyears = parseE('eukaryotes.txt')
Vyears = parseV('viruses.txt')
Pyears = parseP('prokaryotes.txt')
plt.figure(0)
plotType(Eyears, "Eukaryotes")
plotType(Vyears, "Viruses")
plotType(Pyears, "Prokaryotes")
plt.xlabel("Year")
plt.ylabel("Genomes")
plt.legend(loc=2)
plt.title("Complete Genomes in NCBI")
plt.savefig("genome_completed.svg")
plt.savefig("genome_completed.jpg")
plt.savefig("genome_completed.png")
