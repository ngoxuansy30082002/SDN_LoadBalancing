import subprocess
import threading


def run_iperf(port):
    # Tạo lệnh iperf3 để chạy máy chủ trên cổng được chỉ định
    command = f'iperf3 -s -p {port}'
    subprocess.run(command, shell=True)


def main():
    ports = [5001, 5002, 5003, 5004, 5005, 5006, 5007,
             5008, 5009]  # Các cổng cho 3 máy chủ iperf3
    threads = []

    # Tạo và khởi chạy các luồng cho 3 máy chủ iperf3
    for port in ports:
        thread = threading.Thread(target=run_iperf, args=(port,))
        thread.start()
        threads.append(thread)

    # Chờ tất cả các luồng hoàn thành
    for thread in threads:
        thread.join()


if __name__ == "__main__":
    main()
