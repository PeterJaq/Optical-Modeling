import csv
import scipy
import numpy as np
from scipy.interpolate import interp1d
import os
import pandas as pd

MAT = "Zn+SiO2"
MAT_DIR = "./MAT/%s/" % MAT
WRI_CSV = "./Index_Refraction_%s.csv" % MAT
MAT_PATH = []

def dataload(filename, waveLenRange):
    n = []
    k = []
    wavlen = []

    with open(filename, 'r') as file_to_read:
        while True:
            lines = file_to_read.readline()
            if not lines:
                break
            data = lines.strip().split(" ")
            data[0] = float(data[0])
            #print(data[0])

            n.append(float(data[1]))
            k.append(float(data[2]))
            if(data[0] < 10):
                wavlen.append(float(data[0])*1000)
            else:
                wavlen.append(float(data[0]))

        fn = interp1d(wavlen, n)
        fk = interp1d(wavlen, k)

        new_n = fn(waveLenRange)
        new_k = fk(waveLenRange)

    return new_n, new_k

if __name__ == '__main__':
    start_wav = 250
    end_wav = 1500
    wavlenrange = np.linspace(start_wav, end_wav, 1251)
    df = pd.DataFrame(columns=['Wavelength (nm)'], data=wavlenrange)
    file_paths = os.listdir(MAT_DIR)
    for file in file_paths:
        mat_name = os.path.splitext(file)[0]
        file_path = os.path.join(MAT_DIR, file)
        print(mat_name)
        mat_n, mat_k = dataload(file_path, wavlenrange)
        df1 = pd.concat([df, pd.DataFrame(columns=[mat_name + '_n'], data=mat_n)], axis=1)
        df2 = pd.concat([df1, pd.DataFrame(columns=[mat_name + '_k'], data=mat_k)], axis=1)
        df = df2
    df.to_csv(WRI_CSV, index=False)






