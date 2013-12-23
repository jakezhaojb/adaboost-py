# Designed by Junbo Zhao
# 12/23/2013
# Processing the Training and Testing data. Writing them into .txt files.

from numpy import *

#You can use this simple data to Debug and validate this program
def loadSimpleData():
    data = matrix([[ 1. ,  2.1],
        [ 2. ,  1.1],
        [ 1.3,  1. ],
        [ 1. ,  1. ],
        [ 2. ,  1. ]])
    label = [1,1,-1,-1,1]
    return data, label


# Generate random data for Debug and validation.
def randomData(fname,sampleNum,option):
    import random
    if not isinstance(fname,basestring):
        print 'File cannot be built!'
        return
    filename = fname + '.txt'
    fid = open(filename,'w')
    if option == 'train':
        for i in range(sampleNum):
            fid.write('+1:%.4f,%.4f,%.4f,%.4f,%.4f\n' %(random.random(),random.random(),random.random(),random.random(),random.random()))
            fid.write('-1:%.4f,%.4f,%.4f,%.4f,%.4f\n' %(random.random(),random.random(),random.random(),random.random(),random.random()))
        fid.close()
        return
    elif option == 'test':
        for i in range(sampleNum):
            fid.write('%.4f,%.4f,%.4f,%.4f,%.4f\n' %(random.random(),random.random(),random.random(),random.random(),random.random()))
            fid.write('%.4f,%.4f,%.4f,%.4f,%.4f\n' %(random.random(),random.random(),random.random(),random.random(),random.random()))
        fid.close()
        return
    else:
        print 'Wrong input parameter!'
        return

    
# Read data from Training or Testing file
def readData(filename,option):
    if option == 'train':
        fid = open(filename,'r')
        print 'Preparing training data'
        label = []
        data = None
        while True:
            fline = fid.readline()
            if len(fline) == 0:     #EOF
                break
            label.append(int(fline[0:fline.find(':')]))
            
            dataNew = []
            i = fline.find(':') + 1
            dataNew = [float(fline[i:fline.find(',',i,-1)])]
            while True:
                i = fline.find(',',i,-1) + 1
                if not i:
                    break;
                dataNew.append(float(fline[i:fline.find(',',i,-1)])) # Excellent design of python!!! No problem of this!
            if data is None:
                data = mat(dataNew)
            else:
                data = vstack([data,mat(dataNew)])
        fid.close()
        return data,label
    elif option == 'test':
        fid = open(filename,'r')
        print 'Preparing training data'
        data = None
        while True:
            fline = fid.readline()
            if len(fline) == 0:     #EOF
                break
            
            dataNew = []
            i=0
            while True:
                dataNew.append(float(fline[i:fline.find(',',i,-1)])) # Excellent design of python!!! No problem of this!
                i = fline.find(',',i,-1) + 1
                if not i:
                    break
            if data is None:
                data = mat(dataNew)
            else:
                data = vstack([data,mat(dataNew)])
        fid.close()
        return data
    else:
        print 'Wrong input parameter!'
