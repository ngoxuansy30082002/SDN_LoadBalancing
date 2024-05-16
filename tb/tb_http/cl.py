import subprocess
import threading
import re
import argparse


def main():

    command = f'wrk -t 4 -c 100 -d 20s -s Project/tb/tb_http/test.lua --latency "http://10.0.0.100:9000/demo"'
    result = subprocess.run(command, shell=True,
                            capture_output=True, text=True)
    print(f"Result for port :\n{result.stdout}")
    # Tìm dòng cuối cùng chứa kết quả cuối cùng của mỗi luồng
    # Tìm dòng "[ ID] Interval..."
    # interval_count = 0  # Biến đếm số lần xuất hiện của "[ ID] Interval"
    # found_bitrate = False  # Biến kiểm tra xem đã tìm thấy Bitrate hay chưa

    # for line in result.stdout.split('\n'):
    #     if line.startswith("[ ID] Interval"):
    #         interval_count += 1
    #         continue
    #     elif interval_count == 2 and not found_bitrate:  # Chỉ xử lý dòng sau lần xuất hiện thứ hai
    #         # print(line)
    #         match = re.search(r'(\d+(\.\d+)?)\s+([KMG]?bits/sec)', line)
    #         if match:
    #             bitrate = match.group(1)
    #             unit = match.group(3)  # Lấy group 3 cho đơn vị
    #             print(f"Result for port {port}: Bitrate = {bitrate} {unit}")
    #             found_bitrate = True  # Đánh dấu đã tìm thấy Bitrate
    #             return

    # # Nếu không tìm thấy Bitrate sau lần xuất hiện thứ hai, in thông báo lỗi
    # if not found_bitrate:
    #     print(f"Result for port {port}: Bitrate = 0 Mbps/sec")


if __name__ == "__main__":
    main()
