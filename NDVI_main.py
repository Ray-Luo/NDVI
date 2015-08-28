import os
from NDVI import calculate_ndvi
import auxil.auxil as auxil


def main():

#   input directory    
    in_path = auxil.select_directory()

#   imagery dataset
    lista = os.listdir(in_path)
    GQ = []
    i = 0
    for k in range(len(lista)):
        GQ.append(in_path+"/"+lista[k])
    for k in GQ:
        if k[-45:-38] == "MOD09GQ":
            calculate_ndvi(k)

        





if __name__ == '__main__':
    main()
