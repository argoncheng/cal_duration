#coding=utf-8
"""
统计当前目录或指定目录中所有视频文件的时长并输出总时长。

如果未提供目录参数，则分析当前目录；如果提供目录参数，则分析指定目录。
"""
import argparse
import os
import subprocess
import sys


# Get video_file's duration in seconds from its ffmpeg output message
# Return 0 if error
def video_duration(video_file):
    # ffmpegcmd = 'c:\\Program Files (x86)\\FormatFactory\\ffmpeg.exe'
    ffmpegcmd = 'C:\\Users\\Administrator\\AppData\\Local\\Microsoft\\WinGet\\Packages\\Gyan.FFmpeg_Microsoft.Winget.Source_8wekyb3d8bbwe\\ffmpeg-8.1.1-full_build\\bin\\ffmpeg.exe'
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
# 计算给定文件夹中所有视频文件的总时长。
# 参数：#     file_dir (str): 包含视频文件的文件夹路径。
# 返回：
#     int: 所有视频文件的总时长(以秒为单位)。
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
    parser = argparse.ArgumentParser(
        description='统计当前目录或指定目录中所有视频文件的时长，并输出每个文件时长与总时长。',
        epilog='如果未提供目录参数，则分析当前目录；如果提供目录参数，则分析指定目录。'
    )
    parser.add_argument(
        'directory',
        nargs='?',
        default='.',
        help='要分析的视频文件目录，默认当前目录'
    )
    args = parser.parse_args()

    target_dir = args.directory
    if not os.path.isdir(target_dir):
        print(f"目录不存在: {target_dir}")
        sys.exit(1)

    video_sec = cal_total_duration(target_dir)
    hour = int(video_sec / 3600)
    minute = int((video_sec - hour * 3600) / 60)
    sec = video_sec - hour * 3600 - minute * 60
    print("Total duration of all video files is %02d:%02d:%02d" % (hour, minute, sec))


if __name__ == '__main__':
    main()

