from tkinter import *
import os, PyPDF2, sys, time
from tkinter import filedialog as tkFileDialog
from tkinter import messagebox as tkMessageBox
from tkinter import ttk

#s = ttk.Style()
#s.theme_use('clam')
master = Tk()

def openFile():
	master.filename = tkFileDialog.askopenfilename(filetypes = (('PDF Files', '*.pdf'),('All Files','*.*')))
	filename.set(master.filename)

def go():
	cps = cp.get().split(',')
	inputPdf = master.filename
	file = PyPDF2.PdfFileReader(inputPdf)

	numberOfPages = file.getNumPages()
	outputFolder = 'temp'
	os.system('mkdir ' + outputFolder)
	#gs = 'gs'
	gs = 'gswin64c'
	mergeString = ''
	g = ''
	firstPage = ''
	lastPage = ''
	ranges = []
	for i in range(len(cps)):
		if i == 0 and '1' not in cps:
			firstPage = '1'
			lastPage = str(int(cps[0]) - 1)
			ranges.append([firstPage,lastPage,'gray'])
		else:
			if str(int(cps[i - 1]) + 1) not in cps:
				firstPage = str(int(cps[i - 1]) + 1)
			if str(int(cps[i]) - 1) not in cps:
				lastPage = str(int(cps[i]) - 1)
				ranges.append([firstPage,lastPage,'gray'])

		ranges.append([cps[i],cps[i],'color'])

		if i == len(cps) - 1:                         #LAATSTE ELEMENT
			firstPage = str(int(cps[len(cps) - 1]) + 1)
			lastPage = str(numberOfPages)
			ranges.append([firstPage,lastPage,'gray'])
	if cps[0] == '1':
		del ranges[0]
	print(ranges)
	merger = PyPDF2.PdfFileMerger()
	pageRange = []
	i = 0
	for pageRange in ranges:
	    i += int((10/len(ranges)) * 10)
	    updateProgress(i)
	    progressLbl = Label(master,textvariable = progress)
	    progressLbl.grid(row = 7, column = 0)
	    firstPage = pageRange[0]
	    lastPage = pageRange[1]
	    color = pageRange[2]

	    output = firstPage + '-' + lastPage  + '.pdf'
	    os.system(gs + ' -dQUIET -dBATCH -dSAFER -dNOPAUSE -dFirstPage=' + firstPage +' -dLastPage='+ lastPage +' -sDEVICE=pdfwrite -o ' +  outputFolder + '/' + output + ' ' + inputPdf)

	    if color == 'gray':
	        outputGray = firstPage + '-' + lastPage  + '-' + color + '.pdf'
	        os.system(gs + ' -sDEVICE=pdfwrite -dProcessColorModel=/DeviceGray -dColorConversionStrategy=/Gray -dPDFUseOldCMS=false -o ' +  outputFolder + '/' + outputGray + ' -f ' + outputFolder + '/' + output)
	        os.system('del /Q ' + outputFolder + '\\' + output)
	        #os.system('rm ' + outputFolder + '/' + output)
	        merger.append(outputFolder + '/' + outputGray)
	        print (outputFolder + '/' + outputGray +' GEMERGED')
	        #file.write(outputFolder + '/merge.pdf')
	    else:
	        outputColor = firstPage + '-' + lastPage  + '-' + color + '.pdf'
	        merger.append(outputFolder + '/' + output)
	        print (outputFolder + '/' + outputColor +' GEMERGED')

	merger.write(mergedFilename.get() + '.pdf')
	merger.close()
	os.system('rmdir /Q /S ' + outputFolder)
	tkMessageBox.showinfo('Grayscaler', mergedFilename.get() + '.pdf omgezet!')


def updateProgress(i):
	progress.set(str(i) + '%')
	master.update()

filename = StringVar()
master.filename = 'e:\gs\in.pdf'
filename.set('e:\gs\in.pdf')

#master.geometry('450x450+400+200')
master.title('Grayscaler')
fileBtn = Button(master, text = 'Kies een bestand', command = lambda: openFile())
fileBtn.grid(row = 0, column = 0)

fileLbl = Label(master, textvariable=filename)
fileLbl.grid(row = 1, column = 0)

colorPagesLbl = Label(text = 'Kleurenpagina\'s (gescheiden door komma): ')
colorPagesLbl.grid(row = 2, column = 0)

cp = StringVar()
colorPages = Entry(master, textvariable = cp)
cp.set('1,3,6')
colorPages.grid(row = 3, column = 0)

mergedFilenameLbl = Label(text = 'Samgengestelde bestandsnaam: ')
mergedFilenameLbl.grid(row = 4, column = 0)

mergedFilename = StringVar()
mergedFilenameEntry = Entry(master, textvariable = mergedFilename)
mergedFilename.set('merged')
mergedFilenameEntry.grid(row = 5, column = 0)

goBtn = Button(master, text = 'Go!', command = lambda: go())
goBtn.grid(row = 6, column = 0)

progress = StringVar()
progress.set('0%')
progressLbl = Label(master,textvariable = progress)
progressLbl.grid(row = 7, column = 0)

master.mainloop()
