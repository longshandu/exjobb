import sys, os, re, subprocess, shutil
import downscaling, filenames, paths

from definitions import *
from binaries import *


paths.assert_hevc_directory()

if len(sys.argv) != 2:
    print "Usage: %s <hq_bitstream>" % os.path.basename(sys.argv[0])
    sys.exit(1)


hq_bitstream = sys.argv[1]

hq_bitstream_base = os.path.basename(hq_bitstream)
hq_bitstream_shortpath = os.path.splitext(hq_bitstream_base)[0]

(width, height) = filenames.extract_dimensions(hq_bitstream_base)

if height != 1080:
	raise Exception("Expected 1080p video")


#paths.create_if_needed(output_folder)

sequence_folder = "%s/%s" % (output_folder, hq_bitstream_shortpath)
paths.remove_and_recreate_directory(sequence_folder)

hq_bitstream_decoded_shortpath = "%s_dec" % hq_bitstream_shortpath
hq_bitstream_decoded = "%s/%s.yuv" % (sequence_folder, hq_bitstream_decoded_shortpath)

hq_bitstream_decoded_dec_order_shortpath = "%s_dec_dec_order" % hq_bitstream_shortpath
hq_bitstream_decoded_dec_order = "%s/%s.yuv" % (sequence_folder, hq_bitstream_decoded_dec_order_shortpath)

# Logs

err_log = "%s/err.txt" % sequence_folder
err_log_file = open(err_log, 'a+')

# Preprocessing

## Decode HQ bitstream
hq_decode_cmd = "%s -b %s -o %s" % (hm_decoder, hq_bitstream, hq_bitstream_decoded)
subprocess.call(hq_decode_cmd, shell=True, stderr=err_log_file)

print hq_decode_cmd
sys.exit(0)

## Decode HQ bitstream in decoding order
dec_order_cmd = "%s -i %s -o %s" % (d65_gt_dec_order, hq_bitstream, hq_bitstream_decoded_dec_order)
subprocess.call(dec_order_cmd, shell=True, stderr=err_log_file)


"""
[1], [0], [1,0] means two-thirds, half and one-third downscaling.
This corresponds to 720p, 536p and 360p for a 1080p video.
"""

downscale_parameter_set = [[1], [0], [1,0]]
#downscale_parameter_set = [[0], [0,0]]

for downscale_parameter in downscale_parameter_set:
    
    (downscaled_width, downscaled_height) = downscaling.convert_dimensions(width, height, downscale_parameter)
    downscaled_height = downscaling.height_divisible_by_eight(downscaled_height)

    downscale_folder = "%s/%d" % (sequence_folder, downscaled_height)

    paths.create_if_needed(downscale_folder)


    # Set up transcoding filenames

    downscaled_file_shortpath = filenames.replace_dimensions(hq_bitstream_decoded_shortpath, downscaled_width, downscaled_height)
    downscaled_file = "%s/%s.yuv" % (downscale_folder, downscaled_file_shortpath)

    rdoq_0_file_shortpath = "%s_rdoq_0" % (downscaled_file_shortpath)
    rdoq_0_file = "%s/%s.bin" % (downscale_folder, rdoq_0_file_shortpath)

    pruned_file_shortpath = "%s_pruned" % rdoq_0_file_shortpath
    pruned_file = "%s/%s.bin" % (downscale_folder, pruned_file_shortpath)

    hq_bitstream_decoded_dec_order_downscaled_shortpath = filenames.replace_dimensions(hq_bitstream_decoded_dec_order_shortpath, downscaled_width, downscaled_height)
    hq_bitstream_decoded_dec_order_downscaled = "%s/%s.yuv" % (downscale_folder, hq_bitstream_decoded_dec_order_downscaled_shortpath)

    reconstructed_file_shortpath = "%s_transcoded" % filenames.replace_dimensions(hq_bitstream_shortpath, downscaled_width, downscaled_height)
    reconstructed_file = "%s/%s.bin" % (downscale_folder, reconstructed_file_shortpath)

    reconstructed_file_decoded_shortpath = "%s_dec" % reconstructed_file_shortpath
    reconstructed_file_decoded = "%s/%s.yuv" % (downscale_folder, reconstructed_file_decoded_shortpath)


    # Perform transcoding

    ## Branch 1
    
    ### Downscale decoded HQ bistream
    downscaling.perform_downscaling(width, height, hq_bitstream_decoded, downscaled_file, downscale_parameter)

    ### Re-encode with RDOQ=0
    rdoq_0_cmd = "%s -c %s -i %s -b %s -fr %d -f %d -wdt %d -hgt %d --RDOQ=0 -SBH 0 --RDOQTS=0" % (hm_encoder, cfg_file, downscaled_file, rdoq_0_file, framerate, frames, downscaled_width, downscaled_height)
    subprocess.call(rdoq_0_cmd, shell=True, stderr=err_log_file)

    #sys.exit(0)

    ### Prune
    prune_cmd = "%s -i %s -n %s" % (d65_gt_pruning, rdoq_0_file, pruned_file)
    subprocess.call(prune_cmd, shell=True, stderr=err_log_file)

    ## Branch 2

    ### Downscale decoding order HQ bitstream
    downscaling.perform_downscaling(width, height, hq_bitstream_decoded_dec_order, hq_bitstream_decoded_dec_order_downscaled, downscale_parameter)


    ## Put together the branches ##

    ### Reconstruct residual
    res_reconstruct_cmd = "%s -i %s -u %s -n %s" % (d65_gt_res_reconstruct, pruned_file, hq_bitstream_decoded_dec_order_downscaled, reconstructed_file)
    subprocess.call(res_reconstruct_cmd, shell=True, stderr=err_log_file)

    ### Decode transcoded video
    res_reconstruct_decode_cmd = "%s -b %s -o %s" % (hm_decoder, reconstructed_file, reconstructed_file_decoded)
    subprocess.call(res_reconstruct_decode_cmd, shell=True, stderr=err_log_file)


    # Cleanup
    #os.remove(downscaled_file)
    #os.remove(rdoq_0_file)
    #os.remove(pruned_file)
    #os.remove(hq_bitstream_decoded_dec_order_downscaled)
    #os.remove(reconstructed_file)

    # Play transcoded file
    ffplay_cmd = "%s -i %s -video_size %dx%d -vcodec rawvideo -autoexit" % (ffplay, reconstructed_file_decoded, downscaled_width, downscaled_height)
    subprocess.call(ffplay_cmd, shell=True)


# Cleanup
#os.remove(hq_bitstream_decoded)
#os.remove(hq_bitstream_decoded_dec_order)

err_log_file.close()