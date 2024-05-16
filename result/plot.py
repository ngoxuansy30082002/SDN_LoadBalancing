import pandas as pd
import matplotlib.pyplot as plt

# Đọc dữ liệu từ 3 file CSV
df1 = pd.read_csv('result/lb/response_times1.csv')
df2 = pd.read_csv('result/lb/response_times2.csv')
df3 = pd.read_csv('result/lb/response_times3.csv')

# Tính Response Time trung bình cho mỗi client
mean_response_time1 = df1['Response Time (s)'].mean()
mean_response_time2 = df2['Response Time (s)'].mean()
mean_response_time3 = df3['Response Time (s)'].mean()

# In kết quả
print("Client 1 - Response Time trung bình:", mean_response_time1, "giây")
print("Client 2 - Response Time trung bình:", mean_response_time2, "giây")
print("Client 3 - Response Time trung bình:", mean_response_time3, "giây")

# Chuyển đổi cột Timestamp sang dạng datetime
df1['Timestamp'] = pd.to_datetime(df1['Timestamp'])
df2['Timestamp'] = pd.to_datetime(df2['Timestamp'])
df3['Timestamp'] = pd.to_datetime(df3['Timestamp'])

# Vẽ biểu đồ đường
plt.plot(df1['Response Time (s)'].values, label='client1')
plt.plot(df2['Response Time (s)'].values, label='client2')
plt.plot(df3['Response Time (s)'].values, label='client3')

# Thiết lập nhãn cho các trục và tiêu đề
plt.xlabel('Thời gian')
plt.ylabel('Thời gian phản hồi (giây)')
plt.title('Biểu đồ thời gian phản hồi của 3 client')

# Hiển thị legend
plt.legend()
plt.ylim(ymin=0, ymax=20)
# Hiển thị biểu đồ
plt.show()
