import os, sys, math
import ExcelPlot, BDelta, cfgFile, testSeqs
########################################
## 
## Output files
##
########################################


########################################
##
## Configuration
##
########################################

### read config ###
assert len(sys.argv) == 2 or len(sys.argv) == 3, "expected one or two arguments"
inputFile1 = sys.argv[1]
if len(sys.argv) == 2:
    inputFile2 = inputFile1
else:
    inputFile2 = sys.argv[2]
print "reading evaluation configuration '%s'\n" % inputFile1
conf1 = cfgFile.cfgFile(inputFile=inputFile1)
print "reading evaluation configuration '%s'\n" % inputFile2
conf2 = cfgFile.cfgFile(inputFile=inputFile2)

seqs1 = []
for attr in conf1['testSequences']:
    seqs1.append(testSeqs.testSeq(*attr))
seqs2 = []
for attr in conf2['testSequences']:
    seqs2.append(testSeqs.testSeq(*attr))
seqs = []
tmpSimIds1 = conf1['simIds']
decode1 = conf1['decode']
tmpSimIds2 = conf2['simIds']
decode2 = conf2['decode']
simIds1 = []
simIds2 = []
for seqCnt1 in range(len(seqs1)):
    for seqCnt2 in range(len(seqs2)):
        if seqs1[seqCnt1].equal(seqs2[seqCnt2],ignoreName=False,ignoreYuv=True):
            for existingSeq in seqs:
                if seqs1[seqCnt1].name == existingSeq.name:
                    print "ERROR: duplicate sequence name found, check the following files:"
                    print inputFile1
                    print inputFile2
                    exit(1)
            seqs.append(seqs1[seqCnt1])
            simIds1.append(tmpSimIds1[seqCnt1])
            simIds2.append(tmpSimIds2[seqCnt2])
            break
simSettings1 = conf1['simSettings']
simSettings2 = conf2['simSettings']
[resultsDir1, dummy] = os.path.split(inputFile1)
[resultsDir2, dummy] = os.path.split(inputFile2) 
resultsSubDir1 = resultsDir1+'/'+conf1['resultsSubDir']
resultsSubDir2 = resultsDir2+'/'+conf2['resultsSubDir']
if len(simIds1) == 0:
    print "ERROR: no matching sequences found"
    exit(1)
numQps = len(simIds1[0])
if(len(simIds2[0])<numQps):
 numQps = len(simIds2[0])

#### do some checks ###
for seqCnt in range(len(seqs)):
    assert len(simIds1[seqCnt]) >= numQps
    assert len(simIds2[seqCnt]) >= numQps


########################################

results = {}
results2 = {}
resultslog = {}
resultslog2 = {}
TimeData = {}
BDData = {}
BDDataU = {}
BDDataV = {}
BDDataOverlap = {}
BDDataUOverlap = {}
BDDataVOverlap = {}
BDPSNRData = {}
BDPSNRDataU = {}
BDPSNRDataV = {}
BDPSNRDataOverlap = {}
BDPSNRDataUOverlap = {}
BDPSNRDataVOverlap = {}
rangepsnrY2 = {}
rangepsnrU2 = {}
rangepsnrV2 = {}
rangepsnrY = {}
rangepsnrU = {}
rangepsnrV = {}
avgbitrate = {}
avgpsnr = {}
setavgBDY = [0, 0, 0]
setavgBDU = [0, 0, 0]
setavgBDV = [0, 0, 0]
setavgBDYOverlap = [0, 0, 0]
setavgBDUOverlap = [0, 0, 0]
setavgBDVOverlap = [0, 0, 0]
setavgBDPSNRY = [0, 0, 0]
setavgBDPSNRU = [0, 0, 0]
setavgBDPSNRV = [0, 0, 0]
setavgBDPSNRYOverlap = [0, 0, 0]
setavgBDPSNRUOverlap = [0, 0, 0]
setavgBDPSNRVOverlap = [0, 0, 0]
setavgbitrate = [0, 0]
setavgpsnr = [0, 0]
setavgtime = [[0,0,0], [0,0,0]]
seqOK = []

BDSSIMRateData = {}
BDSSIMRateDataU = {}
BDSSIMRateDataV = {}
BDSSIMRateDataOverlap = {}
BDSSIMRateDataUOverlap = {}
BDSSIMRateDataVOverlap = {}
BDSSIMData = {}
BDSSIMDataU = {}
BDSSIMDataV = {}
BDSSIMDataOverlap = {}
BDSSIMDataUOverlap = {}
BDSSIMDataVOverlap = {}
setavgBDSSIMRateY = [0, 0, 0]
setavgBDSSIMRateU = [0, 0, 0]
setavgBDSSIMRateV = [0, 0, 0]
setavgBDSSIMRateYOverlap = [0, 0, 0]
setavgBDSSIMRateUOverlap = [0, 0, 0]
setavgBDSSIMRateVOverlap = [0, 0, 0]
setavgBDSSIMY = [0, 0, 0]
setavgBDSSIMU = [0, 0, 0]
setavgBDSSIMV = [0, 0, 0]
setavgBDSSIMYOverlap = [0, 0, 0]
setavgBDSSIMUOverlap = [0, 0, 0]
setavgBDSSIMVOverlap = [0, 0, 0]
avgssim = {}
setavgssim = [0, 0]

# run encodings
mismatch1 = 0
mismatch2 = 0
for seq in range(len(seqs)):
    results[seq] = ([], [], [], [], [], [], [], [], [])
    results2[seq] = ([], [], [], [], [], [], [], [], [])
    resultslog[seq] = ([], [], [], [], [], [], [], [], [])
    resultslog2[seq] = ([], [], [], [], [], [], [], [], [])
    rangepsnrY2[seq] = [] 
    rangepsnrU2[seq] = [] 
    rangepsnrV2[seq] = [] 
    rangepsnrY[seq] = [] 
    rangepsnrU[seq] = [] 
    rangepsnrV[seq] = [] 
    avgbitrate[seq] = []
    avgbitrate[seq].append(0)
    avgbitrate[seq].append(0)
    avgpsnr[seq] = []
    avgpsnr[seq].append(0)
    avgpsnr[seq].append(0)
    avgssim[seq] = []
    avgssim[seq].append(0)
    avgssim[seq].append(0)
    theseqOK = 1
   
    index=0
    # first test
    for qpCnt in range(numQps):

        #get bitrates and psnr to check match between enc and dec 
        textEnc = resultsSubDir1 + '/rd_' + simIds1[seq][qpCnt] + ".txt"
        ok = os.path.isfile(textEnc)
        if(ok):
          afile = open(textEnc,'r')
          commandref = afile.readline()
          aline = afile.readline()
          aline = afile.readline()
          astr = str(aline)
          alist = astr.split(' ')
          bitrateEnc = float(alist[0])
          psnrYEnc = float(alist[1])
          psnrUEnc = float(alist[2])
          psnrVEnc = float(alist[3])
          aline = afile.readline()
          aline = afile.readline()
          aline = afile.readline()
          aline = afile.readline()
          aline = afile.readline()
          astr = str(aline)
          alist = astr.split(' ')
          encTime1_usr = float(alist[0])
          encTime1_sys = float(alist[1])
          encTime1_all = float(alist[2])
              
        else:
          if theseqOK == 1: theseqOK = 2
          text = textEnc + 'NOT FOUND\n'
          print text
          encTime1_usr = 0.0
          encTime1_sys = 0.0
          encTime1_all = 0.0

        if decode1:
            text = resultsSubDir1 + '/dec-rd_' + simIds1[seq][qpCnt] + ".txt"
        else:
            text = resultsSubDir1 + '/rd_' + simIds1[seq][qpCnt] + ".txt"
        text2 = "Reading anchor info %s" % text
        print text2

        ok = os.path.isfile(text)
        if(ok):
          afile = open(text,'r')
          commandref = afile.readline()
          aline = afile.readline()
          aline = afile.readline()
          astr = str(aline)
          alist = astr.split(' ')
          bitrate = float(alist[0])
          psnrY = float(alist[1])
          psnrU = float(alist[2])
          psnrV = float(alist[3])
          aline = afile.readline()
          aline = afile.readline()
          astr = str(aline)
          alist = astr.split(' ')
          maxpsnrY = float(alist[0])
          maxpsnrU = float(alist[1])
          maxpsnrV = float(alist[2])
          aline = afile.readline()
          aline = afile.readline()
          astr = str(aline)
          alist = astr.split(' ')
          minpsnrY = float(alist[0])
          minpsnrU = float(alist[1])
          minpsnrV = float(alist[2])
          if decode1:
            aline = afile.readline()
            astr = str(aline)
            alist = astr.split(' ')
            decTime1_usr = float(alist[0])
            decTime1_sys = float(alist[1])
            decTime1_all = float(alist[2])
          else:
            decTime1_usr = 0.0
            decTime1_sys = 0.0
            decTime1_all = 0.0

          afile.close()
          print bitrate
          print psnrY

          results[seq][0].append(bitrate/1000)
          #results[seq][1].append(psnrY)
          #results[seq][2].append(psnrU)
          #results[seq][3].append(psnrV)
          results[seq][4].append([encTime1_usr, encTime1_sys, encTime1_all])
          results[seq][5].append([decTime1_usr, decTime1_sys, decTime1_all])
          resultslog[seq][0].append(bitrate)
          #resultslog[seq][1].append(psnrY)
          #resultslog[seq][2].append(psnrU)
          #resultslog[seq][3].append(psnrV)
          resultslog[seq][4].append([encTime1_usr, encTime1_sys, encTime1_all])
          resultslog[seq][5].append([decTime1_usr, decTime1_sys, decTime1_all])

          rangepsnrY[seq].append(maxpsnrY-minpsnrY)
          rangepsnrU[seq].append(maxpsnrU-minpsnrU)
          rangepsnrV[seq].append(maxpsnrV-minpsnrV)
        else:
          theseqOK = 0
          text = text + 'NOT FOUND\n'
          print text

        #check if enc and dec match
        if (decode1 and theseqOK==1):
          if((psnrY!=psnrYEnc) or (psnrU!=psnrUEnc) or (psnrV!=psnrVEnc) or (bitrate!=bitrateEnc)):
            mismatch1=1

        #extract SSIM from RSM encoder logs
        textLog = "jobs/" + resultsSubDir1.split('/')[2] + '/' + simIds1[seq][qpCnt][:-3] + "/SequencePSNR.txt"
        ok = os.path.isfile(textLog)
        if(ok):
          psnrY = 0.0
          psnrU = 0.0
          psnrV = 0.0
          ssimY = 0.0
          ssimU = 0.0
          ssimV = 0.0
          for aline in open(textLog,'r'):
            if 'Avg' in aline:
              psnrY = (float)(aline.split(' ')[2].strip(','))
              psnrU = (float)(aline.split(' ')[3].strip(','))
              psnrV = (float)(aline.split(' ')[4].strip(','))
              ssimY = (float)(aline.split(' ')[5].strip(','))
              ssimU = (float)(aline.split(' ')[6].strip(','))
              ssimV = (float)(aline.split(' ')[7].strip(','))
          results[seq][1].append(psnrY)
          results[seq][2].append(psnrU)
          results[seq][3].append(psnrV)
          resultslog[seq][1].append(psnrY)
          resultslog[seq][2].append(psnrU)
          resultslog[seq][3].append(psnrV)
          results[seq][6].append(ssimY)
          results[seq][7].append(ssimU)
          results[seq][8].append(ssimV)
          resultslog[seq][6].append(ssimY)
          resultslog[seq][7].append(ssimU)
          resultslog[seq][8].append(ssimV)


    # second test
    for qpCnt in range(numQps):
        #get bitrates and psnr to check match between enc and dec 
        textEnc = resultsSubDir2 + '/rd_' + simIds2[seq][qpCnt] + ".txt"
        ok = os.path.isfile(textEnc)
        if(ok):
          afile = open(textEnc,'r')
          commandref = afile.readline()
          aline = afile.readline()
          aline = afile.readline()
          astr = str(aline)
          alist = astr.split(' ')
          bitrateEnc = float(alist[0])
          psnrYEnc = float(alist[1])
          psnrUEnc = float(alist[2])
          psnrVEnc = float(alist[3])
          aline = afile.readline()
          aline = afile.readline()
          aline = afile.readline()
          aline = afile.readline()
          aline = afile.readline()
          astr = str(aline)
          alist = astr.split(' ')
          encTime2_usr = float(alist[0])
          encTime2_sys = float(alist[1])
          encTime2_all = float(alist[2])
        else:
          text = textEnc + 'NOT FOUND\n'
          print text
          if theseqOK == 1: theseqOK = 2
          encTime2_usr = 0.0
          encTime2_sys = 0.0
          encTime2_all = 0.0

        if decode2:
            text = resultsSubDir2 + '/dec-rd_' + simIds2[seq][qpCnt] + ".txt"
        else:
            text = resultsSubDir2 + '/rd_' + simIds2[seq][qpCnt] + ".txt"
        text2 = "Reading test info %s" % text
        print text2
        ok = os.path.isfile(text)
        if(ok):
          afile = open(text,'r')
          commandtest = afile.readline()
          aline = afile.readline()
          aline = afile.readline()
          astr = str(aline)
          alist = astr.split(' ')
          bitrate = float(alist[0])
          psnrY = float(alist[1])
          psnrU = float(alist[2])
          psnrV = float(alist[3])
          aline = afile.readline()
          aline = afile.readline()
          astr = str(aline)
          alist = astr.split(' ')
          maxpsnrY = float(alist[0])
          maxpsnrU = float(alist[1])
          maxpsnrV = float(alist[2])
          aline = afile.readline()
          aline = afile.readline()
          astr = str(aline)
          alist = astr.split(' ')
          minpsnrY = float(alist[0])
          minpsnrU = float(alist[1])
          minpsnrV = float(alist[2])
          if decode2:
            aline = afile.readline()
            astr = str(aline)
            alist = astr.split(' ')
            decTime2_usr = float(alist[0])
            decTime2_sys = float(alist[1])
            decTime2_all = float(alist[2])
          else:
            decTime2_usr = 0.0
            decTime2_sys = 0.0
            decTime2_all = 0.0
          afile.close()
          print bitrate
          print psnrY

          results2[seq][0].append(bitrate/1000)
          #results2[seq][1].append(psnrY)
          #results2[seq][2].append(psnrU)
          #results2[seq][3].append(psnrV)
          results2[seq][4].append([encTime2_usr, encTime2_sys, encTime2_all])
          results2[seq][5].append([decTime2_usr, decTime2_sys, decTime2_all])
          resultslog2[seq][0].append(bitrate)
          #resultslog2[seq][1].append(psnrY)
          #resultslog2[seq][2].append(psnrU)
          #resultslog2[seq][3].append(psnrV)
          resultslog2[seq][4].append([encTime2_usr, encTime2_sys, encTime2_all])
          resultslog2[seq][5].append([decTime2_usr, decTime2_sys, decTime2_all])

          rangepsnrY2[seq].append(maxpsnrY-minpsnrY)
          rangepsnrU2[seq].append(maxpsnrU-minpsnrU)
          rangepsnrV2[seq].append(maxpsnrV-minpsnrV)
        else:
          theseqOK = 0
          text = text + 'NOT FOUND\n'
          print text

        #check if enc and dec match
        if (decode2 and theseqOK==1):
          if((psnrY!=psnrYEnc) or (psnrU!=psnrUEnc) or (psnrV!=psnrVEnc) or (bitrate!=bitrateEnc)):
            mismatch2=1

        #extract SSIM from RSM encoder logs
        textLog = "jobs/" + resultsSubDir2.split('/')[2] + '/' + simIds2[seq][qpCnt][:-3] + "/SequencePSNR.txt"
        ok = os.path.isfile(textLog)
        if(ok):
          psnrY = 0.0
          psnrU = 0.0
          psnrV = 0.0
          ssimY = 0.0
          ssimU = 0.0
          ssimV = 0.0
          for aline in open(textLog,'r'):
            if 'Avg' in aline:
              psnrY = (float)(aline.split(' ')[2].strip(','))
              psnrU = (float)(aline.split(' ')[3].strip(','))
              psnrV = (float)(aline.split(' ')[4].strip(','))
              ssimY = (float)(aline.split(' ')[5].strip(','))
              ssimU = (float)(aline.split(' ')[6].strip(','))
              ssimV = (float)(aline.split(' ')[7].strip(','))
          results2[seq][1].append(psnrY)
          results2[seq][2].append(psnrU)
          results2[seq][3].append(psnrV)
          resultslog2[seq][1].append(psnrY)
          resultslog2[seq][2].append(psnrU)
          resultslog2[seq][3].append(psnrV)
          results2[seq][6].append(ssimY)
          results2[seq][7].append(ssimU)
          results2[seq][8].append(ssimV)
          resultslog2[seq][6].append(ssimY)
          resultslog2[seq][7].append(ssimU)
          resultslog2[seq][8].append(ssimV)

    seqOK.append(theseqOK)

# get BD data
avgOverlap = 0
lowOverlap = 0
highOverlap = 0
seqnr = 0
for seq in range(len(seqs)):
    # BDelta is currently reusing the input variables thats why I duplicated the result variables
    # so that the Excel plotting can use the unmodified bitrates

  if(seqOK[seq]):    
    for i in range(len(resultslog[seq][0])):
      if(resultslog[seq][0][i]!=0.0):
            resultslog[seq][0][i] = math.log10(resultslog[seq][0][i])
      if(resultslog2[seq][0][i]!=0.0):
            resultslog2[seq][0][i] = math.log10(resultslog2[seq][0][i])

    avgenctime1 = [0, 0, 0]
    for i in range(numQps):
        for j in range(3):
            avgenctime1[j] = avgenctime1[j] + results[seq][4][i][j]
    avgenctime2 = [0, 0, 0]
    for i in range(numQps):
        for j in range(3):
            avgenctime2[j] = avgenctime2[j] + results2[seq][4][i][j]
    avgdectime1 = [0, 0, 0]
    for i in range(numQps):
        for j in range(3):
            avgdectime1[j] = avgdectime1[j] + results[seq][5][i][j]
    avgdectime2 = [0, 0, 0]
    for i in range(numQps):
        for j in range(3):
            avgdectime2[j] = avgdectime2[j] + results2[seq][5][i][j]

    TimeData[seqnr] = {}
    for j in range(3):
        denctime = avgenctime2[j]-avgenctime1[j]
        if(avgenctime1[j]!=0):
          denctime = 100.0 * (float(denctime)/avgenctime1[j])
        else:
          denctime = 0.0

        ddectime = avgdectime2[j]-avgdectime1[j]
        if(avgdectime1[j]!=0):
          ddectime = 100.0 * (float(ddectime)/avgdectime1[j])
        else:
          ddectime = 0.0

        setavgtime[0][j] = setavgtime[0][j] + denctime
        setavgtime[1][j] = setavgtime[1][j] + ddectime

        TimeData[seqnr][j] = [denctime, ddectime] 

    d = BDelta.NDiff(resultslog[seq][0], resultslog[seq][1], resultslog2[seq][0], resultslog2[seq][1])
    (average,avgOverlap) = d.bitrateDiff()     
    (high,highOverlap) = d.bitrateDiffHigh()
    (low,lowOverlap) = d.bitrateDiffLow()
    BDData[seqnr] = [average, high, low]
    BDDataOverlap[seqnr] = [avgOverlap, highOverlap, lowOverlap]

    (average,avgOverlap) = d.psnrDiff()     
    (high,highOverlap) = d.psnrDiffHigh()
    (low,lowOverlap) = d.psnrDiffLow()
    BDPSNRData[seqnr] = [average, high, low]
    BDPSNRDataOverlap[seqnr] = [avgOverlap, highOverlap, lowOverlap]
   
    for i in range(3):
      setavgBDY[i] = setavgBDY[i] + BDData[seqnr][i]
      setavgBDYOverlap[i] = setavgBDYOverlap[i] + BDDataOverlap[seqnr][i]
      setavgBDPSNRY[i] = setavgBDPSNRY[i] + BDPSNRData[seqnr][i]
      setavgBDPSNRYOverlap[i] = setavgBDPSNRYOverlap[i] + BDPSNRDataOverlap[seqnr][i]

    dU = BDelta.NDiff(resultslog[seq][0], resultslog[seq][2], resultslog2[seq][0], resultslog2[seq][2])
    (averageU,avgOverlap) = dU.bitrateDiff()
    (highU,highOverlap) = dU.bitrateDiffHigh()
    (lowU,lowOverlap) = dU.bitrateDiffLow()
    BDDataU[seqnr] = [averageU, highU, lowU]
    BDDataUOverlap[seqnr] = [avgOverlap, highOverlap, lowOverlap]

    (average,avgOverlap) = dU.psnrDiff()     
    (high,highOverlap) = dU.psnrDiffHigh()
    (low,lowOverlap) = dU.psnrDiffLow()
    BDPSNRDataU[seqnr] = [average, high, low]
    BDPSNRDataUOverlap[seqnr] = [avgOverlap, highOverlap, lowOverlap]

    for i in range(3):
      setavgBDU[i] = setavgBDU[i] + BDDataU[seqnr][i]
      setavgBDUOverlap[i] = setavgBDUOverlap[i] + BDDataUOverlap[seqnr][i]
      setavgBDPSNRU[i] = setavgBDPSNRU[i] + BDPSNRDataU[seqnr][i]
      setavgBDPSNRUOverlap[i] = setavgBDPSNRUOverlap[i] + BDPSNRDataUOverlap[seqnr][i]

    dV = BDelta.NDiff(resultslog[seq][0], resultslog[seq][3], resultslog2[seq][0], resultslog2[seq][3])
    (averageV,avgOverlap) = dV.bitrateDiff()
    (highV,highOverlap) = dV.bitrateDiffHigh()
    (lowV,lowOverlap) = dV.bitrateDiffLow()
    BDDataV[seqnr] = [averageV, highV, lowV]
    BDDataVOverlap[seqnr] = [avgOverlap, highOverlap, lowOverlap]

    (average,avgOverlap) = dV.psnrDiff()     
    (high,highOverlap) = dV.psnrDiffHigh()
    (low,lowOverlap) = dV.psnrDiffLow()
    BDPSNRDataV[seqnr] = [average, high, low]
    BDPSNRDataVOverlap[seqnr] = [avgOverlap, highOverlap, lowOverlap]

    for i in range(3):
      setavgBDV[i] = setavgBDV[i] + BDDataV[seqnr][i]
      setavgBDVOverlap[i] = setavgBDVOverlap[i] + BDDataVOverlap[seqnr][i]
      setavgBDPSNRV[i] = setavgBDPSNRV[i] + BDPSNRDataV[seqnr][i]
      setavgBDPSNRVOverlap[i] = setavgBDPSNRVOverlap[i] + BDPSNRDataVOverlap[seqnr][i]
   
    d = BDelta.NDiff(resultslog[seq][0], resultslog[seq][6], resultslog2[seq][0], resultslog2[seq][6])
    (average,avgOverlap) = d.bitrateDiff()     
    (high,highOverlap) = d.bitrateDiffHigh()
    (low,lowOverlap) = d.bitrateDiffLow()
    BDSSIMRateData[seqnr] = [average, high, low]
    BDSSIMRateDataOverlap[seqnr] = [avgOverlap, highOverlap, lowOverlap]

    (average,avgOverlap) = d.psnrDiff()     
    (high,highOverlap) = d.psnrDiffHigh()
    (low,lowOverlap) = d.psnrDiffLow()
    BDSSIMData[seqnr] = [average, high, low]
    BDSSIMDataOverlap[seqnr] = [avgOverlap, highOverlap, lowOverlap]
   
    for i in range(3):
      setavgBDSSIMRateY[i] = setavgBDSSIMRateY[i] + BDSSIMRateData[seqnr][i]
      setavgBDSSIMRateYOverlap[i] = setavgBDSSIMRateYOverlap[i] + BDSSIMRateDataOverlap[seqnr][i]
      setavgBDSSIMY[i] = setavgBDSSIMY[i] + BDSSIMData[seqnr][i]
      setavgBDSSIMYOverlap[i] = setavgBDSSIMYOverlap[i] + BDSSIMDataOverlap[seqnr][i]

    dU = BDelta.NDiff(resultslog[seq][0], resultslog[seq][7], resultslog2[seq][0], resultslog2[seq][7])
    (averageU,avgOverlap) = dU.bitrateDiff()
    (highU,highOverlap) = dU.bitrateDiffHigh()
    (lowU,lowOverlap) = dU.bitrateDiffLow()
    BDSSIMRateDataU[seqnr] = [averageU, highU, lowU]
    BDSSIMRateDataUOverlap[seqnr] = [avgOverlap, highOverlap, lowOverlap]

    (average,avgOverlap) = dU.psnrDiff()     
    (high,highOverlap) = dU.psnrDiffHigh()
    (low,lowOverlap) = dU.psnrDiffLow()
    BDSSIMDataU[seqnr] = [average, high, low]
    BDSSIMDataUOverlap[seqnr] = [avgOverlap, highOverlap, lowOverlap]

    for i in range(3):
      setavgBDSSIMRateU[i] = setavgBDSSIMRateU[i] + BDSSIMRateDataU[seqnr][i]
      setavgBDSSIMRateUOverlap[i] = setavgBDSSIMRateUOverlap[i] + BDSSIMRateDataUOverlap[seqnr][i]
      setavgBDSSIMU[i] = setavgBDSSIMU[i] + BDSSIMDataU[seqnr][i]
      setavgBDSSIMUOverlap[i] = setavgBDSSIMUOverlap[i] + BDSSIMDataUOverlap[seqnr][i]

    dV = BDelta.NDiff(resultslog[seq][0], resultslog[seq][8], resultslog2[seq][0], resultslog2[seq][8])
    (averageV,avgOverlap) = dV.bitrateDiff()
    (highV,highOverlap) = dV.bitrateDiffHigh()
    (lowV,lowOverlap) = dV.bitrateDiffLow()
    BDSSIMRateDataV[seqnr] = [averageV, highV, lowV]
    BDSSIMRateDataVOverlap[seqnr] = [avgOverlap, highOverlap, lowOverlap]

    (average,avgOverlap) = dV.psnrDiff()     
    (high,highOverlap) = dV.psnrDiffHigh()
    (low,lowOverlap) = dV.psnrDiffLow()
    BDSSIMDataV[seqnr] = [average, high, low]
    BDSSIMDataVOverlap[seqnr] = [avgOverlap, highOverlap, lowOverlap]

    for i in range(3):
      setavgBDSSIMRateV[i] = setavgBDSSIMRateV[i] + BDSSIMRateDataV[seqnr][i]
      setavgBDSSIMRateVOverlap[i] = setavgBDSSIMRateVOverlap[i] + BDSSIMRateDataVOverlap[seqnr][i]
      setavgBDSSIMV[i] = setavgBDSSIMV[i] + BDSSIMDataV[seqnr][i]
      setavgBDSSIMVOverlap[i] = setavgBDSSIMVOverlap[i] + BDSSIMDataVOverlap[seqnr][i]

    #text = "%s/BD_%s_%s.txt" % (resultsSubDir1, simSettings1, simSettings2)
    #afile = open(text,'w')
    #text = "%s %s \nLuma: Average BDrate BDlow BDhigh\n" % (simSettings1, simSettings2)
    #print text
    #afile.write(text) 
    #text = "%f %f %f\n" % (average, low, high) 
    #print text
    #afile.write(text) 
    #text = "Chroma U: Average BDrate BDlow BDhigh\n"
    #print text
    #afile.write(text) 
    #text = "%f %f %f\n" % (averageU, lowU, highU) 
    #print text
    #afile.write(text) 

    #text = "Chroma V: Average BDrate BDlow BDhigh\n"
    #print text
    #afile.write(text) 
    #text = "%f %f %f\n" % (averageV, lowV, highV) 
    #print text
    #afile.write(text) 

    #text = "Anchor Average bitrate [kbps] and psnrY\n"
    #print text
    #afile.write(text) 
    avgbitrate[seqnr][0] = sum(results[seq][0])/float(len(results[seq][0]))
    setavgbitrate[0] = setavgbitrate[0] + avgbitrate[seqnr][0]

    avgpsnr[seqnr][0] = sum(results[seq][1])/float(len(results[seq][1]))
    setavgpsnr[0] = setavgpsnr[0] + avgpsnr[seqnr][0]

    avgpsnrU = sum(results[seq][2])/float(len(results[seq][2]))
    avgpsnrV = sum(results[seq][3])/float(len(results[seq][3]))
    #text = "%f %f %f %f\n" % (avgbitrate[seqnr][0], avgpsnr[seqnr][0], avgpsnrU, avgpsnrV) 
    #print text
    #afile.write(text) 

    avgssim[seqnr][0] = sum(results[seq][6])/float(len(results[seq][6]))
    setavgssim[0] = setavgssim[0] + avgssim[seqnr][0]

    #text = "Test Average bitrate [kbps] and psnrY U V\n"
    #print text
    #afile.write(text) 
    avgbitrate[seqnr][1] = sum(results2[seq][0])/float(len(results2[seq][0]))
    setavgbitrate[1] = setavgbitrate[1] + avgbitrate[seqnr][1]

    avgpsnr[seqnr][1] = sum(results2[seq][1])/float(len(results2[seq][1]))
    setavgpsnr[1] = setavgpsnr[1] + avgpsnr[seqnr][1]

    avgpsnrU = sum(results2[seq][2])/float(len(results2[seq][2]))
    avgpsnrV = sum(results2[seq][3])/float(len(results2[seq][3]))
    #text = "%f %f %f %f\n" % (avgbitrate[seqnr][1], avgpsnr[seqnr][1], avgpsnrU, avgpsnrV) 
    #print text
    #afile.write(text) 

    avgssim[seqnr][1] = sum(results2[seq][6])/float(len(results2[seq][6]))
    setavgssim[1] = setavgssim[1] + avgssim[seqnr][1]

    #for i in range(numQps):
    #    text = "%s: PSNR range Y U V\n" % simIds1[seq][i]
    #    afile.write(text) 
    #    print text
    #    text = "%f %f %f\n" % (rangepsnrY[seq][i], rangepsnrU[seq][i], rangepsnrV[seq][i]) 
    #    afile.write(text) 
    #    print text
    #for i in range(numQps):
    #    text = "%s: PSNR range Y U V\n" % simIds2[seq][i]
    #    afile.write(text)
    #    print text
    #    text = "%f %f %f\n" % (rangepsnrY2[seq][i], rangepsnrU2[seq][i], rangepsnrV2[seq][i]) 
    #    afile.write(text) 
    #    print text

    #afile.close()
    seqnr = seqnr + 1
  else:
    text = "Results for all QPs do not exist for %s" % seqs[seq].name
    print text

# print results into excel
if inputFile1 == inputFile2:
    outFileExcel = "%s/result_%s.xls" % (resultsDir2, simSettings1)
else:
    outFileExcel = "%s/result_%s_%s.xls" % (resultsDir2, simSettings1, simSettings2)

if(seqnr!=0):
 for i in range(3):
  setavgBDY[i] = setavgBDY[i]/seqnr 
  setavgBDU[i] = setavgBDU[i]/seqnr 
  setavgBDV[i] = setavgBDV[i]/seqnr 
  setavgBDYOverlap[i] = setavgBDYOverlap[i]/seqnr 
  setavgBDUOverlap[i] = setavgBDUOverlap[i]/seqnr 
  setavgBDVOverlap[i] = setavgBDVOverlap[i]/seqnr 
  setavgBDPSNRY[i] = setavgBDPSNRY[i]/seqnr 
  setavgBDPSNRU[i] = setavgBDPSNRU[i]/seqnr 
  setavgBDPSNRV[i] = setavgBDPSNRV[i]/seqnr 
  setavgBDPSNRYOverlap[i] = setavgBDPSNRYOverlap[i]/seqnr 
  setavgBDPSNRUOverlap[i] = setavgBDPSNRUOverlap[i]/seqnr 
  setavgBDPSNRVOverlap[i] = setavgBDPSNRVOverlap[i]/seqnr 
  setavgBDSSIMRateY[i] = setavgBDSSIMRateY[i]/seqnr 
  setavgBDSSIMRateU[i] = setavgBDSSIMRateU[i]/seqnr 
  setavgBDSSIMRateV[i] = setavgBDSSIMRateV[i]/seqnr 
  setavgBDSSIMRateYOverlap[i] = setavgBDSSIMRateYOverlap[i]/seqnr 
  setavgBDSSIMRateUOverlap[i] = setavgBDSSIMRateUOverlap[i]/seqnr 
  setavgBDSSIMRateVOverlap[i] = setavgBDSSIMRateVOverlap[i]/seqnr 
  setavgBDSSIMY[i] = setavgBDSSIMY[i]/seqnr 
  setavgBDSSIMU[i] = setavgBDSSIMU[i]/seqnr 
  setavgBDSSIMV[i] = setavgBDSSIMV[i]/seqnr 
  setavgBDSSIMYOverlap[i] = setavgBDSSIMYOverlap[i]/seqnr 
  setavgBDSSIMUOverlap[i] = setavgBDSSIMUOverlap[i]/seqnr 
  setavgBDSSIMVOverlap[i] = setavgBDSSIMVOverlap[i]/seqnr 


  
 for i in range(2):
    setavgbitrate [i] = setavgbitrate[i]/seqnr 
    setavgpsnr [i] = setavgpsnr[i]/seqnr
    setavgssim [i] = setavgssim[i]/seqnr
    for j in range(3):
        setavgtime[i][j] = setavgtime[i][j]/seqnr
 
plotter = ExcelPlot.ExcelPlotter(outFileExcel)
plotter.plotSummaryWithSSIM("Summary", seqOK, setavgBDY, setavgBDU, setavgBDV, setavgBDYOverlap, setavgBDUOverlap, setavgBDVOverlap, setavgBDPSNRY, setavgBDPSNRU, setavgBDPSNRV, setavgBDPSNRYOverlap, setavgBDPSNRUOverlap, setavgBDPSNRVOverlap, setavgbitrate, setavgpsnr, seqs, BDData, BDDataU, BDDataV, BDDataOverlap, BDDataUOverlap, BDDataVOverlap, BDPSNRData, BDPSNRDataU, BDPSNRDataV, BDPSNRDataOverlap, BDPSNRDataUOverlap, BDPSNRDataVOverlap, avgbitrate, avgpsnr, TimeData, setavgtime, avgssim, setavgssim, setavgBDSSIMRateY, setavgBDSSIMRateU, setavgBDSSIMRateV, setavgBDSSIMRateYOverlap, setavgBDSSIMRateUOverlap, setavgBDSSIMRateVOverlap, setavgBDSSIMY, setavgBDSSIMU, setavgBDSSIMV, setavgBDSSIMYOverlap, setavgBDSSIMUOverlap, setavgBDSSIMVOverlap, BDSSIMRateData, BDSSIMRateDataU, BDSSIMRateDataV, BDSSIMRateDataOverlap, BDSSIMRateDataUOverlap, BDSSIMRateDataVOverlap, BDSSIMData, BDSSIMDataU, BDSSIMDataV, BDSSIMDataOverlap, BDSSIMDataUOverlap, BDSSIMDataVOverlap)
seqnr = 0
for seq in range(len(seqs)):   
  if(seqOK[seq]):    
    plotter.plotWithSSIM(seqs[seq].name, results[seq][0], results[seq][1], results[seq][2], results[seq][3], results[seq][4], results[seq][5], results2[seq][0], results2[seq][1], results2[seq][2], results2[seq][3], results2[seq][4], results2[seq][5], BDData[seqnr], BDDataU[seqnr], BDDataV[seqnr], BDDataOverlap[seqnr], BDDataUOverlap[seqnr], BDDataVOverlap[seqnr], BDPSNRData[seqnr], BDPSNRDataU[seqnr], BDPSNRDataV[seqnr], BDPSNRDataOverlap[seqnr], BDPSNRDataUOverlap[seqnr], BDPSNRDataVOverlap[seqnr], avgbitrate[seqnr], avgpsnr[seqnr], results[seq][6], results[seq][7], results[seq][8], results2[seq][6], results2[seq][7], results2[seq][8], avgssim[seqnr], BDSSIMRateData[seqnr], BDSSIMRateDataU[seqnr], BDSSIMRateDataV[seqnr], BDSSIMRateDataOverlap[seqnr], BDSSIMRateDataUOverlap[seqnr], BDSSIMRateDataVOverlap[seqnr], BDSSIMData[seqnr], BDSSIMDataU[seqnr], BDSSIMDataV[seqnr], BDSSIMDataOverlap[seqnr], BDSSIMDataUOverlap[seqnr], BDSSIMDataVOverlap[seqnr])
    seqnr = seqnr + 1 

print "AVG: BDR Y %f U %f V %f\n" % (setavgBDY[0],setavgBDU[0],setavgBDV[0])
if(setavgtime[0][0]==0.0):
  print "AVG enctime user %f  dectime user %f\n" % (setavgtime[0][2],setavgtime[1][2])
else:
  print "AVG enctime all %f  dectime all %f\n" % (setavgtime[0][0],setavgtime[1][0])

plotter.save()

if(mismatch1):
  errmsg = "Encoder/Decoder mismatch: %s\n" % simSettings1
  print errmsg
if(mismatch2):
  errmsg = "Encoder/Decoder mismatch: %s\n" % simSettings2
  print errmsg
  
sumseqOK = 0;
for seq in range(len(seqs)):
  sumseqOK = sumseqOK + seqOK[seq]

if(sumseqOK != len(seqs)):
  for seq in range(len(seqs)):
    if(seqOK[seq]==0):   
      print "Results could not be determined for %s\n" % seqs[seq].name
