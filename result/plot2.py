import matplotlib.pyplot as plt
import pandas as pd

# Đọc dữ liệu từ file CSV
df = pd.read_csv('result/res_iperf/lb/results.csv')

# Chuyển đổi Timestamp sang định dạng datetime
df['Timestamp'] = pd.to_datetime(df['Timestamp'], unit='s')

# Chuyển đổi dữ liệu thành numpy array
timestamps = df['Timestamp'].values
bitrate_h4 = df['Bitrate of h4'].values
bitrate_h5 = df['Bitrate of h5'].values
bitrate_h6 = df['Bitrate of h6'].values

# Vẽ biểu đồ
plt.figure(figsize=(8, 4))

plt.plot(timestamps, bitrate_h4,  label='Bitrate of h4')
plt.plot(timestamps, bitrate_h5,  label='Bitrate of h5')
plt.plot(timestamps, bitrate_h6,  label='Bitrate of h6')

plt.xlabel('Timestamp')
plt.ylabel('Bitrate (Mbps/sec)')
plt.title('Biểu đồ Bitrate theo thời gian')
plt.ylim(0, 14)
plt.legend(loc='lower right')
plt.grid(True)

# Hiển thị biểu đồ
plt.show()
