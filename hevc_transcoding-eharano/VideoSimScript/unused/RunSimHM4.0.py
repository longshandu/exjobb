from RunSimDefinitions import RunSimSamsung
import testSeqs

# configure simulation
simra = RunSimSamsung(simName              = "ra",
                                   encoderExe           = "../HM-4.0/bin/TAppEncoderStatic",
                                   decoderExe           = "../HM-4.0/bin/TAppDecoderStatic",
                                   cfgFileMain          = "../HM-4.0/cfg/encoder_randomaccess.cfg",
                                   testSet              = testSeqs.VCEGMPEG_CS1_CfP,
                                   #testSet              = testSeqs.VCEGMPEG_ClassF, 
                                   maxNumCodedFrames    = None,                                      # None: do nothing, N: restrict number of coded frames to N
                                   temporalSubsampling  = None,                                   # None: do nothing, N: temporally subsample by N before coding
                                   qpSet                = [[37], [32], [27], [22]],               # may be overriden by sequence specific configuration
                                   allowSeqOverride     = 1,
                                   cfgSeqDirOverride    = "cfg_samsung/cfg_seq_randomaccess",
                                   qpNum                = -1,                                     # -1: as in qpSet or seq cfg, 0/1/2/3: select one qp out of qpSet or seq cfg
                                   decode               = 1,
                                   removeEnc            = 2,                                      # 0: keep, 1: use project disk and remove when done, 2: use /tmp
                                   removeRec            = 2,                                      # 0: keep, 1: use project disk and remove when done, 2: use /tmp
                                   removeDec            = 2,                                      # 0: keep, 1: use project disk and remove when done, 2: use /tmp
                                   jobParamsLsfOverride = ['intel', 'sim', False])                 # only for LSF cluster: platform, queue, send results by email

                                                                                             


simld = RunSimSamsung(simName              = "ld",
                                   encoderExe           = "../HM-4.0/bin/TAppEncoderStatic",
                                   decoderExe           = "../HM-4.0/bin/TAppDecoderStatic",
                                   cfgFileMain          = "../HM-4.0/cfg/encoder_lowdelay.cfg",
                                   testSet              = testSeqs.VCEGMPEG_CS2_CfP,
                                   #testSet              = testSeqs.VCEGMPEG_ClassF,
                                   maxNumCodedFrames    = None,                                      # None: do nothing, N: restrict number of coded frames to N
                                   temporalSubsampling  = None,                                   # None: do nothing, N: temporally subsample by N before coding
                                   qpSet                = [[37], [32], [27], [22]],               # may be overriden by sequence specific configuration
                                   allowSeqOverride     = 1,
                                   cfgSeqDirOverride    = "cfg_samsung/cfg_seq_lowdelay",
                                   qpNum                = -1,                                     # -1: as in qpSet or seq cfg, 0/1/2/3: select one qp out of qpSet or seq cfg
                                   decode               = 1,
                                   removeEnc            = 2,                                      # 0: keep, 1: use project disk and remove when done, 2: use /tmp
                                   removeRec            = 2,                                      # 0: keep, 1: use project disk and remove when done, 2: use /tmp
                                   removeDec            = 2,                                      # 0: keep, 1: use project disk and remove when done, 2: use /tmp
                                   jobParamsLsfOverride = ['intel', 'sim', False])                 # only for LSF cluster: platform, queue, send results by email

simldP = RunSimSamsung(simName              = "ld_P",
                                   encoderExe           = "../HM-4.0/bin/TAppEncoderStatic",
                                   decoderExe           = "../HM-4.0/bin/TAppDecoderStatic",
                                   cfgFileMain          = "../HM-4.0/cfg/encoder_lowdelay_P.cfg",
                                   testSet              = testSeqs.VCEGMPEG_CS2_CfP,
                                   #testSet              = testSeqs.VCEGMPEG_ClassF,
                                   maxNumCodedFrames    = None,                                      # None: do nothing, N: restrict number of coded frames to N
                                   temporalSubsampling  = None,                                   # None: do nothing, N: temporally subsample by N before coding
                                   qpSet                = [[37], [32], [27], [22]],               # may be overriden by sequence specific configuration
                                   allowSeqOverride     = 1,
                                   cfgSeqDirOverride    = "cfg_samsung/cfg_seq_lowdelay",
                                   qpNum                = -1,                                     # -1: as in qpSet or seq cfg, 0/1/2/3: select one qp out of qpSet or seq cfg
                                   decode               = 1,
                                   removeEnc            = 2,                                      # 0: keep, 1: use project disk and remove when done, 2: use /tmp
                                   removeRec            = 2,                                      # 0: keep, 1: use project disk and remove when done, 2: use /tmp
                                   removeDec            = 2,                                      # 0: keep, 1: use project disk and remove when done, 2: use /tmp
                                   jobParamsLsfOverride = ['intel', 'sim', False])                 # only for LSF cluster: platform, queue, send results by email

simi = RunSimSamsung(simName              = "i",
                                   encoderExe           = "../HM-4.0/bin/TAppEncoderStatic",
                                   decoderExe           = "../HM-4.0/bin/TAppDecoderStatic",
                                   cfgFileMain          = "../HM-4.0/cfg/encoder_intra.cfg",
                                   testSet              = testSeqs.VCEGMPEG_CfP,
                                   #testSet              = testSeqs.VCEGMPEG_ClassF,
                                   maxNumCodedFrames    = None,                                      # None: do nothing, N: restrict number of coded frames to N
                                   temporalSubsampling  = None,                                   # None: do nothing, N: temporally subsample by N before coding
                                   qpSet                = [[37], [32], [27], [22]],               # may be overriden by sequence specific configuration
                                   allowSeqOverride     = 1,
                                   cfgSeqDirOverride    = "cfg_samsung/cfg_seq_intra",
                                   qpNum                = -1,                                     # -1: as in qpSet or seq cfg, 0/1/2/3: select one qp out of qpSet or seq cfg
                                   decode               = 1,
                                   removeEnc            = 2,                                      # 0: keep, 1: use project disk and remove when done, 2: use /tmp
                                   removeRec            = 2,                                      # 0: keep, 1: use project disk and remove when done, 2: use /tmp
                                   removeDec            = 2,                                      # 0: keep, 1: use project disk and remove when done, 2: use /tmp
                                   jobParamsLsfOverride = ['intel', 'sim', False])                 # only for LSF cluster: platform, queue, send results by email



# loco
simraloco = RunSimSamsung(simName              = "ra_loco",
                                   encoderExe           = "../HM-4.0/bin/TAppEncoderStatic",
                                   decoderExe           = "../HM-4.0/bin/TAppDecoderStatic",
                                   cfgFileMain          = "../HM-4.0/cfg/encoder_randomaccess_loco.cfg",
                                   testSet              = testSeqs.VCEGMPEG_CS1_CfP, 
                                   #testSet              = testSeqs.VCEGMPEG_ClassF,
                                   maxNumCodedFrames    = None,                                      # None: do nothing, N: restrict number of coded frames to N
                                   temporalSubsampling  = None,                                   # None: do nothing, N: temporally subsample by N before coding
                                   qpSet                = [[37], [32], [27], [22]],               # may be overriden by sequence specific configuration
                                   allowSeqOverride     = 1,
                                   cfgSeqDirOverride    = "cfg_samsung/cfg_seq_randomaccess",
                                   qpNum                = -1,                                     # -1: as in qpSet or seq cfg, 0/1/2/3: select one qp out of qpSet or seq cfg
                                   decode               = 1,
                                   removeEnc            = 2,                                      # 0: keep, 1: use project disk and remove when done, 2: use /tmp
                                   removeRec            = 2,                                      # 0: keep, 1: use project disk and remove when done, 2: use /tmp
                                   removeDec            = 2,                                      # 0: keep, 1: use project disk and remove when done, 2: use /tmp
                                   jobParamsLsfOverride = ['intel', 'sim', False])                 # only for LSF cluster: platform, queue, send results by email


                                                                                             


simldloco = RunSimSamsung(simName              = "ld_loco",
                                   encoderExe           = "../HM-4.0/bin/TAppEncoderStatic",
                                   decoderExe           = "../HM-4.0/bin/TAppDecoderStatic",
                                   cfgFileMain          = "../HM-4.0/cfg/encoder_lowdelay_loco.cfg",
                                   testSet              = testSeqs.VCEGMPEG_CS2_CfP, #testSeqs.RH416, 
                                   #testSet              = testSeqs.VCEGMPEG_ClassF,
                                   maxNumCodedFrames    = None,                                      # None: do nothing, N: restrict number of coded frames to N
                                   temporalSubsampling  = None,                                   # None: do nothing, N: temporally subsample by N before coding
                                   qpSet                = [[37], [32], [27], [22]],               # may be overriden by sequence specific configuration
                                   allowSeqOverride     = 1,
                                   cfgSeqDirOverride    = "cfg_samsung/cfg_seq_lowdelay",
                                   qpNum                = -1,                                     # -1: as in qpSet or seq cfg, 0/1/2/3: select one qp out of qpSet or seq cfg
                                   decode               = 1,
                                   removeEnc            = 2,                                      # 0: keep, 1: use project disk and remove when done, 2: use /tmp
                                   removeRec            = 2,                                      # 0: keep, 1: use project disk and remove when done, 2: use /tmp
                                   removeDec            = 2,                                      # 0: keep, 1: use project disk and remove when done, 2: use /tmp
                                   jobParamsLsfOverride = ['intel', 'sim', False])                 # only for LSF cluster: platform, queue, send results by email


simldPloco = RunSimSamsung(simName              = "ld_P_loco",
                                   encoderExe           = "../HM-4.0/bin/TAppEncoderStatic",
                                   decoderExe           = "../HM-4.0/bin/TAppDecoderStatic",
                                   cfgFileMain          = "../HM-4.0/cfg/encoder_lowdelay_P_loco.cfg",
                                   testSet              = testSeqs.VCEGMPEG_CS2_CfP,
                                   #testSet              = testSeqs.VCEGMPEG_ClassF,
                                   maxNumCodedFrames    = None,                                      # None: do nothing, N: restrict number of coded frames to N
                                   temporalSubsampling  = None,                                   # None: do nothing, N: temporally subsample by N before coding
                                   qpSet                = [[37], [32], [27], [22]],               # may be overriden by sequence specific configuration
                                   allowSeqOverride     = 1,
                                   cfgSeqDirOverride    = "cfg_samsung/cfg_seq_lowdelay",
                                   qpNum                = -1,                                     # -1: as in qpSet or seq cfg, 0/1/2/3: select one qp out of qpSet or seq cfg
                                   decode               = 1,
                                   removeEnc            = 2,                                      # 0: keep, 1: use project disk and remove when done, 2: use /tmp
                                   removeRec            = 2,                                      # 0: keep, 1: use project disk and remove when done, 2: use /tmp
                                   removeDec            = 2,                                      # 0: keep, 1: use project disk and remove when done, 2: use /tmp
                                   jobParamsLsfOverride = ['intel', 'sim', False])                 # only for LSF cluster: platform, queue, send results by email



similoco = RunSimSamsung(simName              = "i_loco",
                                   encoderExe           = "../HM-4.0/bin/TAppEncoderStatic",
                                   decoderExe           = "../HM-4.0/bin/TAppDecoderStatic",
                                   cfgFileMain          = "../HM-4.0/cfg/encoder_intra_loco.cfg",
                                   testSet              = testSeqs.VCEGMPEG_CfP,
                                   #testSet              = testSeqs.VCEGMPEG_ClassF,
                                   maxNumCodedFrames    = None,                                      # None: do nothing, N: restrict number of coded frames to N
                                   temporalSubsampling  = None,                                   # None: do nothing, N: temporally subsample by N before coding
                                   qpSet                = [[37], [32], [27], [22]],               # may be overriden by sequence specific configuration
                                   allowSeqOverride     = 1,
                                   cfgSeqDirOverride    = "cfg_samsung/cfg_seq_intra",
                                   qpNum                = -1,                                     # -1: as in qpSet or seq cfg, 0/1/2/3: select one qp out of qpSet or seq cfg
                                   decode               = 1,
                                   removeEnc            = 2,                                      # 0: keep, 1: use project disk and remove when done, 2: use /tmp
                                   removeRec            = 2,                                      # 0: keep, 1: use project disk and remove when done, 2: use /tmp
                                   removeDec            = 2,                                      # 0: keep, 1: use project disk and remove when done, 2: use /tmp
                                   jobParamsLsfOverride = ['intel', 'sim', False])                 # only for LSF cluster: platform, queue, send results by email


# optionally change config file parameters
# NOTE: sequence properties (number of frames, frame sizes etc.)
#       as well as file names, qp settings etc. should not be modified here (these will be overwritten in the script)
#sim.confMain['SearchMode'] = 1

# command parameters can be modified by setting parameters to 'commandOpts'
#sim.confMain['commandOpts'] = '-s 64'

# start simulations

simra.start()
simld.start()

simraloco.start()
simldloco.start()

simi.start()
similoco.start()


# optional condition
#simldPloco.start()
#simldP.start()


