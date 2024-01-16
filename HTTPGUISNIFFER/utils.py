import socket
import struct

def parse_http_payload(tcp_payload):
    headers, body = tcp_payload.split(b'\r\n\r\n', 1)

    headers_list = []
    for header_line in headers.split(b'\r\n'):
        headers_list.append(header_line.decode('windows-1252', errors='replace'))

    first_header = headers_list[0]
    method = first_header.split()[0]

    return (method, headers_list, body.decode('windows-1252', errors='replace'))

def is_http_packet(tcp_payload):
    return b'HTTP' in tcp_payload

def parse_ip_header(packet):
    ip_header = struct.unpack('!BBHHHBBH4s4s', packet[:20])

    version_ihl = ip_header[0]
    version = version_ihl >> 4
    ihl = (version_ihl & 0xF) * 4
    ttl = ip_header[5]
    protocol = ip_header[6]
    src_ip = socket.inet_ntoa(ip_header[8])
    dest_ip = socket.inet_ntoa(ip_header[9])

    return {
        'version': version,
        'ihl': ihl,
        'ttl': ttl,
        'protocol': protocol,
        'src_ip': src_ip,
        'dest_ip': dest_ip,
    }