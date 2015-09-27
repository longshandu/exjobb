software=/home/harald/exjobb/hevc_transcoding-eharano/software
bin=/usr/local/bin

function symlink {
    ln -s $1 $2
}

symlink $software/d65_gt/tools/downScale/bin/linux/downScale $bin/downScale

for d65 in pruning dec_order residual_reconstruct; do
    symlink $software/d65_gt/build_$d65/d65_dec $bin/d65_$d65
done

for hm in TAppEncoderStatic TAppDecoderStatic; do
    symlink $software/HM-16.6/bin/$hm $bin/$hm
done

#symlink $software/ffmpeg/ffmpeg-2.8-32bit-static/ffmpeg $bin/ffmpeg
