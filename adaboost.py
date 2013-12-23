# Designed by Junbo Zhao
# 12/23/2013
# This .py file includes the adaboost core codes.

from numpy import *

# Building weak stump function
def buildWeakStump(d,l,D):
    dataMatrix = mat(d)
    labelmatrix = mat(l).T
    m,n = shape(dataMatrix)
    numstep = 10.0
    bestStump = {}
    bestClass = mat(zeros((5,1)))
    minErr = inf
    for i in range(n):
        datamin = dataMatrix[:,i].min()
        datamax = dataMatrix[:,i].max()
        stepSize = (datamax - datamin) / numstep
        for j in range(-1,int(numstep)+1):
            for inequal in ['lt','gt']:
                threshold = datamin + float(j) * stepSize
                predict = stumpClassify(dataMatrix,i,threshold,inequal)
                err = mat(ones((m,1)))
                err[predict == labelmatrix] = 0
                weighted_err = D.T * err;
                if weighted_err < minErr:
                    minErr = weighted_err
                    bestClass = predict.copy()
                    bestStump['dim'] = i
                    bestStump['threshold'] = threshold
                    bestStump['ineq'] = inequal
    return bestStump, minErr, bestClass

# Use the weak stump to classify training data
def stumpClassify(datamat,dim,threshold,inequal):
    res = ones((shape(datamat)[0],1))
    if inequal == 'lt':
        res[datamat[:,dim] <= threshold] = -1.0
    else:
        res[datamat[:,dim] > threshold] = -1.0
    return res

# Training
def train(data,label,numIt = 1000):
    weakClassifiers = []
    m = shape(data)[0]
    D = mat(ones((m,1))/m)
    EnsembleClassEstimate = mat(zeros((m,1)))
    for i in range(numIt):
        bestStump, error, classEstimate = buildWeakStump(data,label,D)
        alpha = float(0.5*log((1.0-error) / (error+1e-15)))
        bestStump['alpha'] = alpha
        weakClassifiers.append(bestStump)
        weightD = multiply((-1*alpha*mat(label)).T,classEstimate)
        D = multiply(D,exp(weightD))
        D = D/D.sum()
        EnsembleClassEstimate += classEstimate*alpha
        EnsembleErrors = multiply(sign(EnsembleClassEstimate)!=mat(label).T,\
                                  ones((m,1)))  #Converte to float
        errorRate = EnsembleErrors.sum()/m
        print "total error:  ",errorRate
        if errorRate == 0.0:
            break
    return weakClassifiers

# Applying adaboost classifier for a single data sample
def adaboostClassify(dataTest,classifier):
    dataMatrix = mat(dataTest)
    m = shape(dataMatrix)[0]
    EnsembleClassEstimate = mat(zeros((m,1)))
    for i in range(len(classifier)):
        classEstimate = stumpClassify(dataMatrix,classifier[i]['dim'],classifier[i]['threshold'],classifier[i]['ineq'])
        EnsembleClassEstimate += classifier[i]['alpha']*classEstimate
        #print EnsembleClassEstimate
    return sign(EnsembleClassEstimate)

# Testing
def test(dataSet,classifier):
    label = []
    print '\n\n\nResults: '
    for i in range(shape(dataSet)[0]):
        label.append(adaboostClassify(dataSet[i,:],classifier))
        print('%s' %(label[0]))
    return label
