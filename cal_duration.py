#coding=utf-8
import os
import subprocess
import sys


# Get video_file's duration in seconds from its ffmpeg output message
# Return 0 if error
def video_duration(video_file):
    ffmpegcmd = 'c:\Program Files (x86)\FormatFactory\\ffmpeg.exe'
    # I dont know how to set encoding when call popen(). Use temp file instead.
    temp_file = 'cal_duration.tmp'
    if len(video_file) == 0:
        return 0
    if not os.path.exists(ffmpegcmd):
        print(f"{ffmpegcmd} 文件不存在!")
        sys.exit(1)
    new_video_file = video_file.replace('【私人订制加微信：412642105 或 公众号：四小圈】', '')
    os.rename(video_file, new_video_file)
    video_file = new_video_file

    cmd = '"' + ffmpegcmd + '"' + " -i " + '"' + video_file + '"' + " > " + temp_file + " 2>&1"
    #print(cmd)

    #ps = subprocess.Popen(cmd)
    #ps.wait()

    f = os.popen(cmd)
    f.read()

    with open(temp_file, "r", encoding="utf-8") as f:
        buf = f.read()
    os.remove(temp_file)
    #print(buf)
    # Start to parser output message of ffmpeg
    # Duration: 02:07:19.31, start: 0.000000, bitrate: 19609 kb/s
    duration_keystr = "Duration: "
    duration_index = buf.find(duration_keystr)
    if duration_index == -1:
        return 0
    dot_index = buf.find(".", duration_index)
    if dot_index == -1:
        return 0
    duration_str = buf[duration_index+len(duration_keystr):dot_index]
    #print("Duration: is at %d comma is at %d" % (duration_index, dot_index))
    print(f"{duration_str} {os.path.basename(video_file)}")

    # Start to parser duration string
    duration_arr = duration_str.split(":")
    hour = int(duration_arr[0])
    min = int(duration_arr[1])
    sec = int(duration_arr[2].split(".")[0])
    total = hour*3600 + min*60 + sec
    #print("Hour is %d Min is %d Sec is %d Total is %d sec" %(hour, min, sec, total))

    return total

# Try to calculate total duration of all video files
def cal_total_duration(file_dir):
    video_exts = [".mp4", ".mkv"]
    total_duration = 0
    for root, dirs, files in os.walk(file_dir):
        for file in files:
            for video_ext in video_exts:
                if os.path.splitext(file)[1] == video_ext:
                    filename = os.path.join(root, file)
                    total_duration += video_duration(filename)
                    #print("total_duration is %d sec" %(total_duration))
                    break
    return total_duration

def main():
    video_sec = cal_total_duration(".")
    hour = int(video_sec/3600)
    min = int((video_sec - hour * 3600)/60)
    sec = video_sec - hour * 3600 - min * 60
    print("Total duration of all video files is %02d:%02d:%02d" %(hour, min, sec))


if __name__ == '__main__':
    main()

