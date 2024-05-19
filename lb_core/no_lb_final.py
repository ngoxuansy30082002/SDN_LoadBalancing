from operator import attrgetter
import random
import json
from ryu.base import app_manager
from ryu.controller import ofp_event
from ryu.controller.handler import CONFIG_DISPATCHER, MAIN_DISPATCHER, DEAD_DISPATCHER
from ryu.controller.handler import set_ev_cls
from ryu.ofproto import ofproto_v1_3
from ryu.lib.packet import packet
from ryu.lib.packet import ethernet
from ryu.lib.packet import ether_types, arp, tcp, ipv4
from ryu.ofproto import ether, inet
from ryu.lib import hub
from collections import defaultdict


class SimpleMonitor13(app_manager.RyuApp):
    OFP_VERSIONS = [ofproto_v1_3.OFP_VERSION]

    def __init__(self, *args, **kwargs):
        super(SimpleMonitor13, self).__init__(*args, **kwargs)
        self.mac_to_port = {}
        self.serverlist = []  # Creating a list of servers
        self.virtual_lb_ip = "10.0.0.100"  # Virtual Load Balancer IP
        self.virtual_lb_mac = "AB:BC:CD:EF:AB:BC"  # Virtual Load Balancer MAC Address
        self.counter = 1  # counter index server
        self.datapaths = {}
        self.monitor_thread = hub.spawn(self._monitor)
        self.flow_stats = {}
        self.port_stats = {}
        self.port_diffs = defaultdict(
            lambda: {'packet_diff': 0, 'byte_diff': 0})
        self.threshold = 1200000  # Set your desired byte threshold here
        self.lbFlag = False

        # Appending all given IP's, assumed MAC's and ports of switch to which servers are connected to the list created
        self.serverlist.append({})
        self.serverlist.append(
            {'ip': "10.0.0.1", 'mac': "00:00:00:00:00:01", "outport": "1"})
        self.serverlist.append(
            {'ip': "10.0.0.2", 'mac': "00:00:00:00:00:02", "outport": "2"})
        self.serverlist.append(
            {'ip': "10.0.0.3", 'mac': "00:00:00:00:00:03", "outport": "3"})
        print("Done with initial setup related to server list creation.")

    @set_ev_cls(ofp_event.EventOFPSwitchFeatures, CONFIG_DISPATCHER)
    def switch_features_handler(self, ev):
        datapath = ev.msg.datapath
        ofproto = datapath.ofproto
        parser = datapath.ofproto_parser

        # install table-miss flow entry
        match = parser.OFPMatch()
        actions = [parser.OFPActionOutput(ofproto.OFPP_CONTROLLER,
                                          ofproto.OFPCML_NO_BUFFER)]
        self.add_flow(datapath, 0, match, actions)

    def add_flow(self, datapath, priority, match, actions, buffer_id=None):
        ofproto = datapath.ofproto
        parser = datapath.ofproto_parser

        inst = [parser.OFPInstructionActions(ofproto.OFPIT_APPLY_ACTIONS,
                                             actions)]
        if buffer_id:
            mod = parser.OFPFlowMod(datapath=datapath, buffer_id=buffer_id,
                                    priority=priority, match=match,
                                    instructions=inst)
        else:
            mod = parser.OFPFlowMod(datapath=datapath, priority=priority,
                                    match=match, instructions=inst)
        datapath.send_msg(mod)

    # Function placed here, source MAC and IP passed from below now become the destination for the reply ppacket
    def function_for_arp_reply(self, dst_ip, dst_mac):
        arp_target_ip = dst_ip
        arp_target_mac = dst_mac
        # Making the load balancers IP and MAC as source IP and MAC
        src_ip = self.virtual_lb_ip
        src_mac = self.virtual_lb_mac

        arp_opcode = 2  # ARP opcode is 2 for ARP reply
        hardware_type = 1  # 1 indicates Ethernet ie 10Mb
        arp_protocol = 2048  # 2048 means IPv4 packet
        ether_protocol = 2054  # 2054 indicates ARP protocol
        len_of_mac = 6  # Indicates length of MAC in bytes
        len_of_ip = 4  # Indicates length of IP in bytes

        pkt = packet.Packet()
        ether_frame = ethernet.ethernet(
            dst_mac, src_mac, ether_protocol)  # Dealing with only layer 2
        arp_reply_pkt = arp.arp(hardware_type, arp_protocol, len_of_mac, len_of_ip, arp_opcode, src_mac,
                                src_ip, arp_target_mac, dst_ip)  # Building the ARP reply packet, dealing with layer 3
        pkt.add_protocol(ether_frame)
        pkt.add_protocol(arp_reply_pkt)
        pkt.serialize()
        return pkt

    @set_ev_cls(ofp_event.EventOFPPacketIn, MAIN_DISPATCHER)
    def _packet_in_handler(self, ev):
        # If you hit this you might want to increase
        # the "miss_send_length" of your switch
        if ev.msg.msg_len < ev.msg.total_len:
            self.logger.debug("packet truncated: only %s of %s bytes",
                              ev.msg.msg_len, ev.msg.total_len)
        msg = ev.msg
        datapath = msg.datapath
        ofproto = datapath.ofproto
        parser = datapath.ofproto_parser
        in_port = msg.match['in_port']
        dpid = datapath.id

        pkt = packet.Packet(msg.data)
        eth = pkt.get_protocols(ethernet.ethernet)[0]

        if eth.ethertype == ether_types.ETH_TYPE_LLDP:
            # ignore lldp packet
            return

        # If the ethernet frame has eth type as 2054 indicating as ARP packet..
        if eth.ethertype == ether.ETH_TYPE_ARP:
            arp_header = pkt.get_protocols(arp.arp)[0]

            # ..and if the destination is the virtual IP of the load balancer and Opcode = 1 indicating ARP Request
            if arp_header.dst_ip == self.virtual_lb_ip and arp_header.opcode == arp.ARP_REQUEST:
                # Call the function that would build a packet for ARP reply passing source MAC and source IP
                reply_packet = self.function_for_arp_reply(
                    arp_header.src_ip, arp_header.src_mac)
                actions = [parser.OFPActionOutput(in_port)]
                packet_out = parser.OFPPacketOut(
                    datapath=datapath, in_port=ofproto.OFPP_ANY, data=reply_packet.data, actions=actions, buffer_id=0xffffffff)
                datapath.send_msg(packet_out)
            return

        ip_header = pkt.get_protocols(ipv4.ipv4)[0]
        tcp_header = pkt.get_protocols(tcp.tcp)[0]

        server_ip_selected = self.serverlist[self.counter]['ip']
        server_mac_selected = self.serverlist[self.counter]['mac']
        server_outport_selected = int(self.serverlist[self.counter]['outport'])

        # # Route to server
        # match = parser.OFPMatch(in_port=in_port, eth_type=eth.ethertype, eth_src=eth.src, eth_dst=eth.dst, ip_proto=ip_header.proto,
        #                         ipv4_src=ip_header.src, ipv4_dst=ip_header.dst)
        # actions = [parser.OFPActionSetField(ipv4_src=self.virtual_lb_ip), parser.OFPActionSetField(eth_src=self.virtual_lb_mac), parser.OFPActionSetField(
        #     eth_dst=server_mac_selected), parser.OFPActionSetField(ipv4_dst=server_ip_selected), parser.OFPActionOutput(server_outport_selected)]
        # inst = [parser.OFPInstructionActions(
        #     ofproto.OFPIT_APPLY_ACTIONS, actions)]
        # cookie = random.randint(0, 0xffffffffffffffff)
        # flow_mod = parser.OFPFlowMod(datapath=datapath, match=match, idle_timeout=7,
        #                              instructions=inst, buffer_id=msg.buffer_id, cookie=cookie, priority=1)
        # datapath.send_msg(flow_mod)

        # # Reverse route from server
        # match = parser.OFPMatch(in_port=server_outport_selected, eth_type=eth.ethertype, eth_src=server_mac_selected, eth_dst=self.virtual_lb_mac,
        #                         ip_proto=ip_header.proto, ipv4_src=server_ip_selected, ipv4_dst=self.virtual_lb_ip)
        # actions = [parser.OFPActionSetField(eth_src=self.virtual_lb_mac), parser.OFPActionSetField(ipv4_src=self.virtual_lb_ip), parser.OFPActionSetField(
        #     ipv4_dst=ip_header.src), parser.OFPActionSetField(eth_dst=eth.src), parser.OFPActionOutput(in_port)]
        # inst2 = [parser.OFPInstructionActions(
        #     ofproto.OFPIT_APPLY_ACTIONS, actions)]
        # cookie = random.randint(0, 0xffffffffffffffff)
        # flow_mod2 = parser.OFPFlowMod(
        #     datapath=datapath, match=match, idle_timeout=7, instructions=inst2, cookie=cookie, priority=1)
        # datapath.send_msg(flow_mod2)

        # Route to server
        match = parser.OFPMatch(in_port=in_port, eth_type=eth.ethertype, eth_src=eth.src, eth_dst=eth.dst, ip_proto=ip_header.proto,
                                ipv4_src=ip_header.src, ipv4_dst=ip_header.dst, tcp_src=tcp_header.src_port, tcp_dst=tcp_header.dst_port)
        actions = [parser.OFPActionSetField(ipv4_src=self.virtual_lb_ip), parser.OFPActionSetField(eth_src=self.virtual_lb_mac), parser.OFPActionSetField(
            eth_dst=server_mac_selected), parser.OFPActionSetField(ipv4_dst=server_ip_selected), parser.OFPActionOutput(server_outport_selected)]
        inst = [parser.OFPInstructionActions(
            ofproto.OFPIT_APPLY_ACTIONS, actions)]
        cookie = random.randint(0, 0xffffffffffffffff)
        flow_mod = parser.OFPFlowMod(datapath=datapath, match=match, idle_timeout=7,
                                     instructions=inst, buffer_id=msg.buffer_id, cookie=cookie, priority=1)
        datapath.send_msg(flow_mod)

        # Reverse route from server
        match = parser.OFPMatch(in_port=server_outport_selected, eth_type=eth.ethertype, eth_src=server_mac_selected, eth_dst=self.virtual_lb_mac,
                                ip_proto=ip_header.proto, ipv4_src=server_ip_selected, ipv4_dst=self.virtual_lb_ip, tcp_src=tcp_header.dst_port, tcp_dst=tcp_header.src_port)
        actions = [parser.OFPActionSetField(eth_src=self.virtual_lb_mac), parser.OFPActionSetField(ipv4_src=self.virtual_lb_ip), parser.OFPActionSetField(
            ipv4_dst=ip_header.src), parser.OFPActionSetField(eth_dst=eth.src), parser.OFPActionOutput(in_port)]
        inst2 = [parser.OFPInstructionActions(
            ofproto.OFPIT_APPLY_ACTIONS, actions)]
        cookie = random.randint(0, 0xffffffffffffffff)
        flow_mod2 = parser.OFPFlowMod(
            datapath=datapath, match=match, idle_timeout=7, instructions=inst2, cookie=cookie, priority=1)
        datapath.send_msg(flow_mod2)

    @set_ev_cls(ofp_event.EventOFPStateChange,
                [MAIN_DISPATCHER, DEAD_DISPATCHER])
    def _state_change_handler(self, ev):
        datapath = ev.datapath
        if ev.state == MAIN_DISPATCHER:
            if datapath.id not in self.datapaths:
                self.logger.debug('register datapath: %016x', datapath.id)
                self.datapaths[datapath.id] = datapath
        elif ev.state == DEAD_DISPATCHER:
            if datapath.id in self.datapaths:
                self.logger.debug('unregister datapath: %016x', datapath.id)
                del self.datapaths[datapath.id]

    def _monitor(self):
        while True:
            for dp in self.datapaths.values():
                self._request_stats(dp)
            hub.sleep(1)

    def _request_stats(self, datapath):
        self.logger.debug('send stats request: %016x', datapath.id)
        ofproto = datapath.ofproto
        parser = datapath.ofproto_parser

        req = parser.OFPFlowStatsRequest(datapath)
        datapath.send_msg(req)

        req = parser.OFPPortStatsRequest(datapath, 0, ofproto.OFPP_ANY)
        datapath.send_msg(req)

    @set_ev_cls(ofp_event.EventOFPFlowStatsReply, MAIN_DISPATCHER)
    def _flow_stats_reply_handler(self, ev):
        body = ev.msg.body
        # self.logger.info('%s', json.dumps(ev.msg.to_jsondict(), ensure_ascii=True,
        #                                   indent=3, sort_keys=True))
        # self.logger.info('datapath         '
        #                  'in-port  eth-dst           '
        #                  'out-port packets  bytes')
        # self.logger.info('---------------- '
        #                  '-------- ----------------- '
        #                  '-------- -------- --------')
        # for stat in sorted([flow for flow in body if flow.priority == 1],
        #                    key=lambda flow: (flow.match['in_port'],
        #                                      flow.match['eth_dst'])):
        #     self.logger.info('%016x %8x %17s %8x %8d %8d',
        #                      ev.msg.datapath.id,
        #                      stat.match['in_port'], stat.match['eth_dst'],
        #                      stat.instructions[0].actions[-1].port,
        #                      stat.packet_count, stat.byte_count)

        #     # key = (ev.msg.datapath.id,
        #     #        stat.match['in_port'], stat.instructions[0].actions[-1].port)
        #     # previous_stat = self.flow_stats.get(key)
        #     # if previous_stat:
        #     #     in_port = stat.match['in_port']
        #     #     packet_diff = stat.packet_count - previous_stat.packet_count
        #     #     byte_diff = stat.byte_count - previous_stat.byte_count
        #     #     self.port_diffs[in_port]['packet_diff'] += packet_diff
        #     #     self.port_diffs[in_port]['byte_diff'] += byte_diff
        #     # self.flow_stats[key] = stat

        # # Print aggregated diff per port
        # self.logger.info("_____ Aggregated Port Diff Statistics: _______")
        # for port, diffs in self.port_diffs.items():
        #     self.logger.info("In Port %d: Packet Diff: %d, Byte Diff: %d",
        #                      port, diffs['packet_diff'], diffs['byte_diff'])

        # # Loop through each server and check byte count
        # # Start from index 1 to skip the empty entry
        # for server_index, server_data in enumerate(self.serverlist[1:]):
        #     server_port = int(server_data['outport'])
        #     byte_diff = self.port_diffs[server_port]['byte_diff']

        #     if byte_diff < self.threshold:
        #         self.counter = server_index + 1  # Adjust index for actual server position
        #         break  # Exit loop if a suitable server is found
        #     else:
        #         # Find minimum byte count among the three servers
        #         byte_diff1 = self.port_diffs[1]['byte_diff']
        #         byte_diff2 = self.port_diffs[2]['byte_diff']
        #         byte_diff3 = self.port_diffs[3]['byte_diff']

        #         min_byte_diff = min(byte_diff1, byte_diff2, byte_diff3)

        #         if min_byte_diff == byte_diff1:
        #             self.counter = 1
        #         elif min_byte_diff == byte_diff2:
        #             self.counter = 2
        #         else:
        #             self.counter = 3

        # print("__1:", self.port_diffs[1]['byte_diff'])
        # print("__2:", self.port_diffs[2]['byte_diff'])
        # print("__3:", self.port_diffs[3]['byte_diff'])
        # print("__4:", self.port_diffs[4]['byte_diff'])
        # print("__5:", self.port_diffs[5]['byte_diff'])
        # print("__6:", self.port_diffs[6]['byte_diff'])

        # self.port_diffs.clear()

        # self.logger.info(
        #     "_______________________________________________________________ \n\n")

    @set_ev_cls(ofp_event.EventOFPPortStatsReply, MAIN_DISPATCHER)
    def _port_stats_reply_handler(self, ev):
        body = ev.msg.body
        # self.logger.info('%s', json.dumps(ev.msg.to_jsondict(), ensure_ascii=True,
        #                                   indent=3, sort_keys=True))
        self.logger.info('datapath         port     '
                         'rx-pkts  rx-bytes rx-error '
                         'tx-pkts  tx-bytes tx-error')
        self.logger.info('---------------- -------- '
                         '-------- -------- -------- '
                         '-------- -------- --------')
        for stat in sorted(body, key=attrgetter('port_no')):
            self.logger.info('%016x %8x %8d %8d %8d %8d %8d %8d',
                             ev.msg.datapath.id, stat.port_no,
                             stat.rx_packets, stat.rx_bytes, stat.rx_errors,
                             stat.tx_packets, stat.tx_bytes, stat.tx_errors)

            key = (stat.port_no)

            previous_stat = self.port_stats.get(key)
            if previous_stat:
                port = stat.port_no
                packet_diff = (stat.rx_packets - previous_stat.rx_packets) + \
                    (stat.tx_packets - previous_stat.tx_packets)
                byte_diff = (stat.rx_bytes - previous_stat.rx_bytes) + \
                    (stat.tx_bytes - previous_stat.tx_bytes)
                self.port_diffs[port]['packet_diff'] = packet_diff
                self.port_diffs[port]['byte_diff'] = byte_diff
            self.port_stats[key] = stat

        self.logger.info("_____ Aggregated Port Diff Statistics: _______")
        for port, diffs in self.port_diffs.items():
            self.logger.info("Port %d: Packet Diff: %d, Byte Diff: %d",
                             port, diffs['packet_diff'], diffs['byte_diff'])

        # for server_index, server_data in enumerate(self.serverlist[1:]):
        #     server_port = int(server_data['outport'])
        #     if len(self.port_diffs) != 0:
        #         byte_diff = self.port_diffs[server_port]['byte_diff']
        #     else:
        #         byte_diff = 0

        #     if byte_diff < self.threshold:
        #         self.counter = server_index + 1  # Adjust index for actual server position
        #         break  # Exit loop if a suitable server is found
        #     else:
        #         # Find minimum byte count among the three servers
        #         byte_diff1 = self.port_diffs[1]['byte_diff']
        #         byte_diff2 = self.port_diffs[2]['byte_diff']
        #         byte_diff3 = self.port_diffs[3]['byte_diff']

        #         min_byte_diff = min(byte_diff1, byte_diff2, byte_diff3)

        #         if min_byte_diff == byte_diff1:
        #             self.counter = 1
        #         elif min_byte_diff == byte_diff2:
        #             self.counter = 2
        #         else:
        #             self.counter = 3

        self.logger.info(
            "_____________________________________________________________________________________________ \n\n\n\n")
        self.port_diffs.clear()
