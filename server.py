import socket
import random
import time
import datetime
import sys


def get_time():
    now = datetime.datetime.now()
    formatted_time = now.strftime('%Y-%m-%d %H:%M:%S') + f".{now.microsecond // 1000:03d}"
    return formatted_time


def ServerLog(state, client_port, qid, qname, qtype, delay=None):
    print("Server log:", end='\n\n')


def SingleLog(state, client_port, qid, qname, qtype, delay=None) -> str:
    current_time = get_time()
    delay_info = f" (delay: {delay}s)" if state == 'rcv' else ""
    log = f"{current_time} {state} {client_port}: {qid} {qname} {qtype} {delay_info}"
    return log


def standardized_txt(file_name) -> list:
    """
    [['foo.example.com.', 'CNAME', 'bar.example.com.'],
 ['d.gtld-servers.net.', 'A', '192.31.80.30'],
 ['foobar.example.com.', 'A', '192.0.2.23'],
 ['bar.example.com.', 'CNAME', 'foobar.example.com.'],
 ['.', 'NS', 'b.root-servers.net.'],
 ['a.root-servers.net.', 'A', '198.41.0.4'],
 ['example.com.', 'A', '93.184.215.14'],
 ['foobar.example.com.', 'A', '192.0.2.24'],
 ['com.', 'NS', 'd.gtld-servers.net.'],
 ['www.metalhead.com.', 'CNAME', 'metalhead.com.'],
 ['.', 'NS', 'a.root-servers.net.']]
    :param file_name: master.txt
    :return: list
    """
    records = []
    with open(file_name, 'r') as file:
        for line in file:
            parts = line.strip().split()
            records.append(parts)
    return records


def parse_master_file():
    records = {}
    with open('sample_master.txt', 'r') as file:
        for line in file:
            parts = line.strip().split()
            domain, rtype, data = parts[0], parts[1], ' '.join(parts[2:])
            if domain not in records:
                records[domain] = {}
            if rtype not in records[domain]:
                records[domain][rtype] = []
            records[domain][rtype].append(data)
    return records


def handle_client(data, addr, sock, records):
    qid, qtype, qname = data.decode().split(',')
    time.sleep(random.randint(0, 4))  # Simulating processing delay

    answer_section = records.get(qname.strip('.'), {}).get(qtype, [])
    authority_section = records.get('.', {}).get('NS', [])
    additional_section = [addr for ns in authority_section for addr in records.get(ns, {}).get('A', [])]

    response = f"{qid},{qname},{qtype}||{qname} {qtype}||{' '.join(answer_section)}||{' '.join(authority_section)}||{' '.join(additional_section)}"
    sock.sendto(response.encode(), addr)


def server(port):
    records = parse_master_file()
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
        s.bind(('localhost', port))
        print("Server log:", end='\n\n')
        while True:
            data, addr = s.recvfrom(1024)
            client_port = addr[1]
            qid, qtype, qname = data.decode().split(',')
            delay = random.randint(0, 4)
            print(SingleLog('rcv', client_port, qid, qname, qtype, delay))
            handle_client(data, addr, s, records)
            print(SingleLog('snd', client_port, qid, qname, qtype))


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python server.py <port>")
        sys.exit(1)
    port = int(sys.argv[1])
    server(port)
