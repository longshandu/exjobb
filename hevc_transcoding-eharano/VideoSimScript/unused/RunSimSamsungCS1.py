from RunSimDefinitions import RunSimSamsung
import testSeqs

# configure simulation
sim = RunSimSamsung(simName              = "JCTVCA124_CS1",
               encoderExe           = "bin/TAppEncoder.exe",
               decoderExe           = "bin/TAppDecoder.exe",
               cfgFileMain          = "cfg_samsung/cs1.cfg",
               testSet              = testSeqs.VCEGMPEG_CS1_CfP,
               maxNumCodedFrames    = None,                                      # None: do nothing, N: restrict number of coded frames to N
               temporalSubsampling  = None,                                   # None: do nothing, N: temporally subsample by N before coding
               qpSet                = [[37], [32], [27], [22]],               # may be overriden by sequence specific configuration
               allowSeqOverride     = 1,
               cfgSeqDirOverride    = "cfg_samsung/cfg_seq_CS1",
               qpNum                = -1,                                     # -1: as in qpSet or seq cfg, 0/1/2/3: select one qp out of qpSet or seq cfg
               decode               = 1,
               removeEnc            = 2,                                      # 0: keep, 1: use project disk and remove when done, 2: use /tmp
               removeRec            = 2,                                      # 0: keep, 1: use project disk and remove when done, 2: use /tmp
               removeDec            = 2,                                      # 0: keep, 1: use project disk and remove when done, 2: use /tmp 
               jobParamsLsfOverride = ['linux', 'sim', True])                 # only for LSF cluster: platform, queue, send results by email
               #jobParamsLsfOverride = ['windows', 'sim', False])                 # only for LSF cluster: platform, queue, send results by email
                                                                              # specify 'intel' platform to make sure all jobs run on similar machines (see "lshosts | grep intel"), e.g. for encoding time measurements

# optionally change config file parameters
# NOTE: sequence properties (number of frames, frame sizes etc.)
#       as well as file names, qp settings etc. should not be modified here (these will be overwritten in the script)
#sim.confMain['SearchMode'] = 1

# fast approach
#sim.confMain['commandOpts'] = '-s 64 -h 4 -1 FEN'

# below are likely all decoder tools turned off
#sim.confMain['BitIncrement'] = 0
#sim.confMain['commandOpts'] = '-0 TMI -0 CCP -0 ACS -0 IMR -0 CAD'
#sim.confMain['ALF'] = 0
#sim.confMain['AMVP'] = 0
#sim.confMain['ADI'] = 0
#sim.confMain['DIF'] = 0
#sim.confMain['AMP'] = 0
#sim.confMain['LogicalTR'] = 0
#sim.confMain['ExtremeCorrection'] = 0
#sim.confMain['MPI'] = 0
#sim.confMain['ROT'] = 0
#sim.confMain['QBO'] = 0
#sim.confMain['HAP'] = 0
#sim.confMain['HAB'] = 0

# start simulations
sim.start()