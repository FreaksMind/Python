import socket
import struct

def parse_http_payload(tcp_payload):
    """
    Function to parse the bytes array that contains the http packet headers and payload 

    Args:
        tcp_payload (bytes array): The bytes that should be parsed

    Returns:
        tuple: A tuple that contains the request method of the packet, a list of headers and the payload of the packet 
    """

    headers, body = tcp_payload.split(b'\r\n\r\n', 1)

    headers_list = []
    for header_line in headers.split(b'\r\n'):
        headers_list.append(header_line.decode('windows-1252', errors='replace'))

    first_header = headers_list[0]
    method = first_header.split()[0]

    return (method, headers_list, body.decode('windows-1252', errors='replace'))

def is_http_packet(tcp_payload):
    """
    Function to verify if a packet is a http packet

    Args:
        tcp_payload (bytes array): The bytes that should be checked

    Returns:
        bool: true if tcp_payload has HTTP in its bytes, false otherwise
    """
    return b'HTTP' in tcp_payload

def parse_tcp_header(tcp_h):
    """
    Function to parse the bytes array that contains the tcp header

    Args:
        tcp_h (bytes array): The bytes that should be parsed

    Returns:
        header: A dictionary that contains the source's port, destination's port and the length of the header
    """

    header = {}
    tcp_header = struct.unpack('!HHLLBBHHH', tcp_h[:20])
    header['src_port'] = tcp_header[0]
    header['dest_port'] = tcp_header[1]
    header['header_length'] = (tcp_header[4] >> 4) * 4
    return header

def parse_ip_header(packet):
    """
    Function to parse the bytes array that contains the ip header

    Args:
        packet (bytes array): The bytes that should be parsed

    Returns:
        header: A dictionary that contains the version of the protocol, the length of the header, time to live of the packet, the protocol, source's ip address and destination's ip address
    """
    
    header = {}
    ip_header = struct.unpack('!BBHHHBBH4s4s', packet[:20])

    version_ihl = ip_header[0]
    version = version_ihl >> 4
    ihl = (version_ihl & 0xF) * 4
    ttl = ip_header[5]
    protocol = ip_header[6]
    src_ip = socket.inet_ntoa(ip_header[8])
    dest_ip = socket.inet_ntoa(ip_header[9])

    header['version'] = version
    header['ihl'] = ihl
    header['ttl'] = ttl
    header['protocol'] = protocol
    header['src_ip'] = src_ip
    header['dest_ip'] = dest_ip
    return header