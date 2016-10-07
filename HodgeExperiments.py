import numpy as np
from Hodge import *

def printConsistencyRatios(Y, I, H, W):
    normD0s = getWNorm(Y-H-I, W)
    
    [normY, normI, normH] = [getWNorm(Y, W), getWNorm(I, W), getWNorm(H, W)]
    a = (normD0s/normY)**2
    b = (normI/normY)**2
    c = (normH/normY)**2
    print "|D0s/Y| = ", a
    print "Local Inconsistency = ", b
    print "Global Inconsistency = ", c
    print "a + b + c = ", a + b + c    

#Do an experiment comparing binary weights on a total order
#to real weights
def doTotalOrderExperiment(N, binaryWeights = False):
    I, J = np.meshgrid(np.arange(N), np.arange(N))
    I = I[np.triu_indices(N, 1)]
    J = J[np.triu_indices(N, 1)]
    #[I, J] = [I[0:N-1], J[0:N-1]]
    NEdges = len(I)
    R = np.zeros((NEdges, 2))
    R[:, 0] = J
    R[:, 1] = I
    
    #W = np.random.rand(NEdges)
    W = np.ones(NEdges)
    
    #Note: When using binary weights, Y is not necessarily a cocycle
    Y = I - J
    if binaryWeights:
        Y = np.ones(NEdges)
        
    (s, I, H) = doHodge(R, W, Y, verbose = True)
    printConsistencyRatios(Y, I, H, W)

#Random flip experiment with linear order
def doRandomFlipExperiment(N, PercentFlips):
    I, J = np.meshgrid(np.arange(N), np.arange(N))
    I = I[np.triu_indices(N, 1)]
    J = J[np.triu_indices(N, 1)]
    NEdges = len(I)
    R = np.zeros((NEdges, 2))
    R[:, 0] = J
    R[:, 1] = I
    
#    toKeep = int(NEdges/200)
#    R = R[np.random.permutation(NEdges)[0:toKeep], :]
#    NEdges = toKeep
    
    W = np.random.rand(NEdges)
    #W = np.ones(NEdges)
    
    Y = np.ones(NEdges)
    NFlips = int(PercentFlips*len(Y))
    Y[np.random.permutation(NEdges)[0:NFlips]] = -1
    
    (s, I, H) = doHodge(R, W, Y)
    [INorm, HNorm] = [getWNorm(I, W), getWNorm(H, W)]
    return (INorm, HNorm)

#Do a bunch of random flip experiments, varying the percentage
#of flips, and take the mean consistency norms for each percentage
#over a number of trials
def doRandomFlipExperimentsVaryPercent(N, AllPercentFlips, NTrials):
    M = len(AllPercentFlips)
    INorm = np.zeros((M, NTrials))
    HNorm = np.zeros((M, NTrials))
    for i in range(M):
        print "%i of %i"%(i, M)
        for k in range(NTrials):
            [INorm[i, k], HNorm[i, k]] = doRandomFlipExperiment(N, AllPercentFlips[i])
    INorm = np.mean(INorm, 1)
    HNorm = np.mean(HNorm, 1)
    plt.subplot(211)
    plt.plot(AllPercentFlips, INorm)
    plt.title('I Norm')
    plt.subplot(212)
    plt.plot(AllPercentFlips, HNorm)
    plt.title('H Norm')
    plt.show()

if __name__ == '__main__':
    doTotalOrderExperiment(600)

#Do random flip experiments
if __name__ == '__main__2':
    np.random.seed(100)
    N = 20
    doRandomFlipExperimentsVaryPercent(N, np.linspace(0, 1, 100), 50)

if __name__ == '__main__2':
    np.random.seed(17)
    R = sio.loadmat('R.mat')['R']
    [R, Y] = [R[:, 0:2], R[:, 2]]
    W = np.random.rand(len(Y))
    #W = np.ones(len(Y))
    (s, I, H) = doHodge(R, W, Y)
    print np.argsort(s)
    
    printConsistencyRatios(Y, I, H, W)
