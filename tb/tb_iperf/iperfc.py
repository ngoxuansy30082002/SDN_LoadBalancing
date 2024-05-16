import subprocess
import threading
import re
import argparse


def connect_to_iperf(server_ip, port, time):
    # Tạo lệnh iperf3 để kết nối đến máy chủ trên cổng được chỉ định
    command = f'iperf3 -c {server_ip} -p {port} -t {time}'
    result = subprocess.run(command, shell=True,
                            capture_output=True, text=True)
    # print(f"Result for port {port}:\n{result.stdout}")
    # Tìm dòng cuối cùng chứa kết quả cuối cùng của mỗi luồng
    # Tìm dòng "[ ID] Interval..."
    interval_count = 0  # Biến đếm số lần xuất hiện của "[ ID] Interval"
    found_bitrate = False  # Biến kiểm tra xem đã tìm thấy Bitrate hay chưa

    for line in result.stdout.split('\n'):
        if line.startswith("[ ID] Interval"):
            interval_count += 1
            continue
        elif interval_count == 2 and not found_bitrate:  # Chỉ xử lý dòng sau lần xuất hiện thứ hai
            # print(line)
            match = re.search(r'(\d+(\.\d+)?)\s+([KMG]?bits/sec)', line)
            if match:
                bitrate = match.group(1)
                unit = match.group(3)  # Lấy group 3 cho đơn vị
                print(f"Result for port {port}: Bitrate = {bitrate} {unit}")
                found_bitrate = True  # Đánh dấu đã tìm thấy Bitrate
                return

    # Nếu không tìm thấy Bitrate sau lần xuất hiện thứ hai, in thông báo lỗi
    if not found_bitrate:
        print(f"Result for port {port}: Bitrate = 0 Mbps/sec")


def main():
    parser = argparse.ArgumentParser(
        description='Iperf3 client with extra arguments.')
    parser.add_argument('server_ip', type=str, help='Server IP address')
    parser.add_argument('ports', type=int, nargs='+',
                        help='Server ports (space-separated)')
    parser.add_argument('time', type=int, help='Test duration in seconds')
    args = parser.parse_args()

    threads = []

    # Tạo và khởi chạy các luồng cho 3 kết nối iperf3
    for port in args.ports:
        thread = threading.Thread(
            target=connect_to_iperf, args=(args.server_ip, port, args.time))
        thread.start()
        threads.append(thread)

    # Chờ tất cả các luồng hoàn thành
    for thread in threads:
        thread.join()


if __name__ == "__main__":
    main()
