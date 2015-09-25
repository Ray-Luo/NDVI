import auxil.auxil as auxil
import os
from ClipRaster import CLIP

def main():

#   input directory    
    in_path = auxil.select_directory(title="Choosing the Image file directory")
    shp = auxil.select_infile()

#   imagery dataset
    lista = os.listdir(in_path)
    #print in_path
    GQ = []
    data_list=[]
    imageList = []
    outputName = ""
    i = 0
    for k in range(len(lista)):
        GQ.append(str(lista[k]))
#

    for k in GQ:
        #print k[-4:]
        try:
            if str(k[-4:]) == ".tif" or str(k[-4:]) == ".TIF":
                data_list.append(k)
        except StandardError, e:
            print "Something is going wrong!"
            
    for k in data_list:
        #print in_path+"/"+k
        outputName = k[:-4] + "_cut.tif"
        CLIP(shp,in_path+"/"+k, outputName)

        




if __name__ == '__main__':
    main()


