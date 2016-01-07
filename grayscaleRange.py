import os
import PyPDF2

#colorInput = input('Kleurenpaginas: ')
#color = colorInput.split(',')
color = ['2','8']
inputPdf = 'in.pdf'
file = PyPDF2.PdfFileReader(inputPdf)
numberOfPages = file.getNumPages()
outputFolder = 'temp'
#gs = 'gs'
gs = 'gswin64c'
mergeString = ''
g = ''
firstPage = ''
lastPage = ''
ranges = []
for i in range(0, len(color)):

    if i == 0 and '1' not in color:             #EERSTE ELEMENT
        firstPage = '1'
        lastPage = str(int(color[0]) - 1)
        ranges.append([firstPage,lastPage,'gray'])
    else:
        if str(int(color[i - 1]) + 1) not in color:
            firstPage = str(int(color[i - 1]) + 1)
        if str(int(color[i]) - 1) not in color:
            lastPage = str(int(color[i]) - 1)
            ranges.append([firstPage,lastPage,'gray'])
        #continue
        #lastPage = str(int(color[i + 1]) - 1)


    ranges.append([color[i],color[i],'color'])

    if i == len(color) - 1:                         #LAATSTE ELEMENT
        firstPage = str(int(color[len(color) - 1]) + 1)
        lastPage = str(numberOfPages)
        ranges.append([firstPage,lastPage,'gray'])


for range in ranges:
    firstPage = range[0]
    lastPage = range[1]
    color = range[2]
    file = PyPDF2.PdfFileMerger()

    output = firstPage + '-' + lastPage  + '.pdf'
    os.system(gs + ' -dQUIET -dBATCH -dSAFER -dNOPAUSE -dFirstPage=' + firstPage +' -dLastPage='+ lastPage +' -sDEVICE=pdfwrite -o ' +  outputFolder + '/' + output + ' ' + inputPdf)

    if color == 'gray':
        outputGray = firstPage + '-' + lastPage  + '-' + color + '.pdf'
        os.system(gs + ' -sDEVICE=pdfwrite -dProcessColorModel=/DeviceGray -dColorConversionStrategy=/Gray -dPDFUseOldCMS=false -o ' +  outputFolder + '/' + outputGray + ' -f ' + outputFolder + '/' + output)
        os.system('del /Q ' + outputFolder + '\\' + output)
        file = file.append(outputFolder + '/' + outputGray)
        print (outputFolder + '/' + outputGray +' GEMERGED')
    else:
        outputColor = firstPage + '-' + lastPage  + '-' + color + '.pdf'
        file = file.append(outputFolder + '/' + output)
        print (outputFolder + '/' + outputColor +' GEMERGED')

file.write(outputFolder + '/merge.pdf')

print(ranges)
