from mininet.net import Mininet
from mininet.node import Controller, RemoteController
from mininet.cli import CLI
from mininet.log import setLogLevel, info
from mininet.link import TCLink
from mininet.topo import Topo
from mininet.node import CPULimitedHost
import threading
import time
import csv
import re

ryu_ip = '127.0.0.1'
ryu_port = 6653


class MyTopo(Topo):
    "Simple topology with 6 hosts and 1 switch."

    def build(self):
        # Add hosts
        # Add hosts and switches
        h1 = self.addHost('h1', mac='00:00:00:00:00:01')
        h2 = self.addHost('h2', mac='00:00:00:00:00:02')
        h3 = self.addHost('h3', mac='00:00:00:00:00:03')
        h4 = self.addHost('h4', mac='00:00:00:00:00:04')
        h5 = self.addHost('h5', mac='00:00:00:00:00:05')
        h6 = self.addHost('h6', mac='00:00:00:00:00:06')
        h7 = self.addHost('h7', mac='00:00:00:00:00:07')
        h8 = self.addHost('h8', mac='00:00:00:00:00:08')
        h9 = self.addHost('h9', mac='00:00:00:00:00:09')
        h10 = self.addHost('h10', mac='00:00:00:00:00:10')
        h11 = self.addHost('h11', mac='00:00:00:00:00:11')
        h12 = self.addHost('h12', mac='00:00:00:00:00:12')
        s1 = self.addSwitch('s1')
        # Add links
        self.addLink(h1, s1,  cls=TCLink, bw=10)
        self.addLink(h2, s1,  cls=TCLink, bw=10)
        self.addLink(h3, s1,  cls=TCLink, bw=10)
        self.addLink(h4, s1,  cls=TCLink, bw=10)
        self.addLink(h5, s1,  cls=TCLink, bw=10)
        self.addLink(h6, s1,  cls=TCLink, bw=10)
        self.addLink(h7, s1,  cls=TCLink, bw=10)
        self.addLink(h8, s1,  cls=TCLink, bw=10)
        self.addLink(h9, s1,  cls=TCLink, bw=10)
        self.addLink(h10, s1,  cls=TCLink, bw=10)
        self.addLink(h11, s1,  cls=TCLink, bw=10)
        self.addLink(h12, s1,  cls=TCLink, bw=10)


def run_wrk(host, script_file, results):
    info(f' _____ Running {script_file} on {host.name} _____\n')
    result = host.cmd(f'{script_file}')
    print(result)


def customNet():
    topo = MyTopo()
    net = Mininet(topo=topo, build=False)
    info('Adding Ryu controller \n')
    net.addController('c0', controller=RemoteController,
                      ip=ryu_ip, port=ryu_port, protocols='OpenFlow13')
    net.start()
    # h1, h2, h3, h4, h5, h6, h7, h8, h9, h10, h11, h12 = net.get(
    #     'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'h7', 'h8', 'h9', 'h10', 'h11', 'h12')

    # # Ánh xạ host với file script tương ứng
    # host_script_map = {
    #     h4: 'python3 Project/tb/tb_http/cl.py',
    #     h5: 'python3 Project/tb/tb_http/cl.py',
    #     h6: 'python3 Project/tb/tb_http/cl.py'
    #     # h7: 'python3 Project/tb/tb_http/cl.py',
    #     # h8: 'python3 Project/tb/tb_http/cl.py',
    #     # h9: 'python3 Project/tb/tb_http/cl.py',
    #     # h10: 'python3 Project/tb/tb_http/cl.py',
    #     # h11: 'python3 Project/tb/tb_http/cl.py',
    #     # h12: 'python3 Project/tb/tb_http/cl.py'
    # }

    # for index in range(10):
    #     print(f"Lần: {index+1} \n\r")

    #     info('\n _____ h1 h2 h3 Initialize the iperf3 server ____ \n')
    #     # Chạy iperfs.py trên h1, h2, h3
    #     h1.cmd('python3 Project/tb/tb_http/sv.py &')
    #     h2.cmd('python3 Project/tb/tb_http/sv.py &')
    #     h3.cmd('python3 Project/tb/tb_http/sv.py &')

    #     time.sleep(3)

    #     results = {}  # Lưu kết quả theo port
    #     threads = []
    #     for host, script_file in host_script_map.items():
    #         thread = threading.Thread(
    #             target=run_wrk, args=(host, script_file, results))
    #         threads.append(thread)
    #         thread.start()

    #         # Đợi các thread kết thúc
    #     for thread in threads:
    #         thread.join()

    #     h1.cmd('pkill -f sv.py')
    #     h2.cmd('pkill -f sv.py')
    #     h3.cmd('pkill -f sv.py')
    #     time.sleep(5)

    info('\n _____ Running CLI ____ \n')
    CLI(net)
    info('\n _____ Stopping network _____ \n')
    net.stop()


if __name__ == '__main__':
    setLogLevel('info')
    customNet()
exit(0)
