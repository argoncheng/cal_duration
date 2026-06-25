#coding=utf-8
"""
统计当前目录或指定目录中所有视频文件的时长并输出总时长。

如果未提供目录参数，则分析当前目录；如果提供目录参数，则分析指定目录。
"""
import argparse
import os
import sys

try:
    import cv2
except ImportError:
    print('请先安装 opencv-python 库：pip install opencv-python')
    sys.exit(1)


# Get video_file's duration in seconds using OpenCV
# Return 0 if error
def video_duration(video_file):
    if len(video_file) == 0:
        return 0
    if not os.path.exists(video_file):
        print(f"视频文件不存在: {video_file}")
        return 0

    cap = cv2.VideoCapture(video_file)
    if not cap.isOpened():
        print(f"无法打开视频文件: {video_file}")
        return 0

    frame_count = cap.get(cv2.CAP_PROP_FRAME_COUNT)
    fps = cap.get(cv2.CAP_PROP_FPS)
    cap.release()

    if fps <= 0 or frame_count <= 0:
        print(f"无法获取视频时长: {video_file}")
        return 0

    duration_float = frame_count / fps
    total = int(duration_float + 0.5)
    hour = total // 3600
    minute = (total % 3600) // 60
    sec = total % 60
    print(f"{hour:02d}:{minute:02d}:{sec:02d} {os.path.basename(video_file)}")
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

