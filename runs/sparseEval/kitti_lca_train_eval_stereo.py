import matplotlib
matplotlib.use('Agg')
#import matplotlib.pyplot as plt
#TODO redo structure to contain both repos into one
import sys
sys.path.append("/home/slundquist/workspace/")

from DeepGAP.dataObj.pv_image import kittiVidPvObj
from tf.lca_adam_time import LCA_ADAM_time
import numpy as np
import pdb

#Paths to list of filenames
#Since we reshape from 6 to 3x2 (3 time, 2 stereo), left/right spin fastest
trainInputs = [
            #"/home/slundquist/mountData/kitti_pv/objdet_train2/FrameLeft0.pvp",
            #"/home/slundquist/mountData/kitti_pv/objdet_train2/FrameRight0.pvp",
            #"/home/slundquist/mountData/kitti_pv/objdet_train2/FrameLeft1.pvp",
            #"/home/slundquist/mountData/kitti_pv/objdet_train2/FrameRight1.pvp",
            "/home/slundquist/mountData/kitti_pv/objdet_train2/FrameLeft2.pvp",
            "/home/slundquist/mountData/kitti_pv/objdet_train2/FrameRight2.pvp",
            ]

trainGts = [
            "/home/slundquist/mountData/kitti_pv/objdet_train2/GroundTruth2Background.pvp",
        ]
trainFilenames = [
            "/home/slundquist/mountData/kitti_pv/objdet_train2/FrameLeft2.pvp",
        ]

dncFilenames= [
            "/home/slundquist/mountData/kitti_pv/objdet_train2/DNCPixels2.pvp",
        ]

#trainFnPrefix = "/shared/KITTI/objdet/training/"

trainRangeFn = "/home/slundquist/mountData/kitti_pv/kitti_objdet_train_list.txt"
testRangeFn = "/home/slundquist/mountData/kitti_pv/kitti_objdet_test_list.txt"

trainf = open(trainRangeFn, 'r')
trainLines = trainf.readlines()
trainf.close()
trainRange = [int(l) for l in trainLines]

testf = open(testRangeFn, 'r')
testLines = testf.readlines()
testf.close()
testRange = [int(l) for l in testLines]

#Get object from which tensorflow will pull data from
trainDataObj = kittiVidPvObj(trainInputs, trainGts, trainFilenames, dncFilenames, None, shuffle=False, getGT=False)
#trainDataObj = kittiVidPvObj(trainInputs, trainGts, trainFilenames, dncFilenames, None, shuffle=True, rangeIdx=trainRange, getGT=False)
#testDataObj = kittiVidPvObj(trainInputs, trainGts, trainFilenames, dncFilenames, None, shuffle=True, rangeIdx=testRange, getGT=False)

#FISTA params
params = {
    #Base output directory
    'outDir':          "/home/slundquist/mountData/tfSparseCode/",
    #Inner run directory
    'runDir':          "/lca_adam_kitti_eval_stereo/",
    'tfDir':           "/tfout",
    #Save parameters
    'ckptDir':         "/checkpoints/",
    'saveFile':        "/save-model",
    'savePeriod':      100, #In terms of displayPeriod
    #output plots directory
    'plotDir':         "plots/",
    'plotPeriod':      100, #With respect to displayPeriod
    #Progress step
    'progress':        10,
    #Controls how often to write out to tensorboard
    'writeStep':       300,
    #Flag for loading weights from checkpoint
    'load':            True,
    'loadFile':        "/home/slundquist/mountData/tfSparseCode/saved/lca_adam_kitti_stereo.ckpt",
    #Device to run on
    'device':          '/gpu:1',
    #####FISTA PARAMS######
    'numIterations':   100000,
    'displayPeriod':   300,
    #Batch size
    'batchSize':       8,
    #Learning rate for optimizer
    'learningRateA':   1e-3,
    'learningRateW':   1,
    #Lambda in energy function
    'thresh':          .0025,
    #Number of features in V1
    'numV':            3072,
    #Stride of V1
    'VStrideT':        1,
    'VStrideY':        4,
    'VStrideX':        4,
    #Patch size
    'patchSizeT':      1,
    'patchSizeY':      15,
    'patchSizeX':      32,
    'stereo':          True,
}

#Allocate tensorflow object
tfObj = LCA_ADAM_time(params, trainDataObj)
print "Done init"
outPrefix = params["outDir"] + params["runDir"] + "kitti_lca_train_eval_stereo"
tfObj.evalSet(trainDataObj, outPrefix)
print "Done run"

tfObj.closeSess()

##Allocate tensorflow object
#tfObj = LCA_ADAM_time(params, testDataObj)
#print "Done init"
#outFilename = params["outDir"] + params["runDir"] + "kitti_lca_test_eval.pvp"
#tfObj.evalSet(testDataObj, outFilename)
#print "Done run"
#
#tfObj.closeSess()
