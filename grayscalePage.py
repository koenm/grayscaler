import os

#number_of_pages = input('Hoeveel paginas?: ')
number_of_pages = 289
colorInput = input('Kleurenpaginas: ')
color = colorInput.split(',')
input_pdf = "abstracts_rev09.pdf"
gs = 'gswin64c'
mString = ''

for i in range(1, number_of_pages + 1):
    os.system(gs + ' -dQUIET -dBATCH -dSAFER -dNOPAUSE -dFirstPage=' + str(i) +' -dLastPage='+ str(i) +' -sDEVICE=pdfwrite -o e:/gs/sat/out'+ str(i) +'.pdf e:/gs/in.pdf')
    if str(i) not in color:
        mString += 'e:/gs/sat/out'+ str(i) +'G.pdf '
        os.system(gs + ' -sDEVICE=pdfwrite -dProcessColorModel=/DeviceGray -dColorConversionStrategy=/Gray -dPDFUseOldCMS=false -o e:/gs/sat/out'+ str(i) +'G.pdf -f e:/gs/sat/out'+ str(i) +'.pdf')
        dfile = 'e:\gs/sat\out'+ str(i) +'.pdf'
        os.system('del /q ' + dfile)
    else:
        mString += 'e:/gs/sat/out'+ str(i) +'.pdf '


os.system(gs + ' -dNOPAUSE -sDEVICE=pdfwrite -sOUTPUTFILE=e:/gs/sat/merge.pdf -dBATCH '+ mString)

#print (mString)

#os.system("e:/gs/gswin64c -sDEVICE=pdfwrite -dProcessColorModel=/DeviceGray -dColorConversionStrategy=/Gray -dPDFUseOldCMS=false -o e:/gs/sat/out.pdf -f e:/in.pdf")
#"C:\Program Files\gs\gs9.18\bin\gswin64c" -sDEVICE=pdfwrite -dProcessColorModel=/DeviceGray -dColorConversionStrategy=/Gray -dPDFUseOldCMS=false -o e:/gs/sat/out.pdf -f e:/in.pdf)
