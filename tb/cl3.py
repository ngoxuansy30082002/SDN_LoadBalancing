import requests
import time
from datetime import datetime
import multiprocessing

SERVER_URL = "http://10.0.0.100:80"
REQUEST_SIZE = 8  # Số byte gửi trong mỗi request
NUM_REQUESTS = 10  # Số lượng request gửi đồng thời
CSV_FILENAME = "response_times3.csv"


def send_request(url, size):
    start_time = time.time()
    response = requests.get(url, data=b"x" * size)
    end_time = time.time()
    response_time = end_time - start_time
    return response_time, response.text


def measure_and_log(url, size, filename):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")
    response_time, response_text = send_request(url, size)
    with open(filename, "a") as csvfile:
        csvfile.write(f"{timestamp},{response_time},{response_text}\n")
    print(f"[{timestamp}] Response time: {response_time:.4f}s, Text: {response_text}")


if __name__ == "__main__":
    with open(CSV_FILENAME, "w") as csvfile:
        csvfile.write("Timestamp,Response Time (s),Response Text\n")

    for _ in range(1000):
        processes = []
        for _ in range(1):
            process = multiprocessing.Process(
                target=measure_and_log, args=(SERVER_URL, REQUEST_SIZE, CSV_FILENAME))
            processes.append(process)
            # time.sleep(0.05)
            process.start()

        for process in processes:
            process.join()
