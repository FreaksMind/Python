import threading
import socket
import utils

class Sniffer(threading.Thread):
    def __init__(self, app):
        threading.Thread.__init__(self)
        self.app = app
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_IP)
        self.socket.bind(("192.168.100.13", 0))
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.socket.setsockopt(socket.IPPROTO_IP, socket.IP_HDRINCL, 1)
        self.socket.ioctl(socket.SIO_RCVALL, 1)

        self.can_run = threading.Event()
        self.done = threading.Event()
        self.done.set()
        self.can_run.set()    

    def run(self):
        while True:
            self.can_run.wait()
            try:
                self.done.clear()
                packet, _ = self.socket.recvfrom(65535)

                ip_info = utils.parse_ip_header(packet)

                if ip_info['protocol'] == socket.IPPROTO_TCP:
                    tcp_payload = packet[ip_info['ihl']:]
                    
                if utils.is_http_packet(tcp_payload):
                    self.app.add_packet(packet)

            finally:
                self.done.set()

    def pause(self):
        self.can_run.clear()
        self.done.wait()

    def resume(self):
        self.can_run.set()