import os, platform


"""
if platform.system() == "Windows":
    #directory_root = os.path.abspath("//vhub.rnd.ki.sw.ericsson.se")
    directory_root = ""

elif platform.system() == "Linux":
    directory_root = ""

else:
    raise Exception("Uknown platform")
"""

#hevc_directory      = "/home/eharano/hevc_transcoding-eharano"
#hevc_directory      = "/home/harald/exjobb/hevc_transcoding-eharano"

#bitstream_folder    = os.path.abspath(directory_root + hevc_directory + "/bitstreams")
#output_folder       = os.path.abspath(directory_root + hevc_directory + "/output_data")

bitstream_folder    = os.path.abspath("bitstreams")
output_folder       = os.path.abspath("output_data")
test_data           = os.path.abspath("test_data")