import socket
import sys
import random

def send_query(server_port, qname, qtype, timeout):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.settimeout(timeout)
    qid = random.randint(0, 65535)
    message = f"{qid},{qtype},{qname}"
    server_address = ('localhost', server_port)

    try:
        print(f"Sending query ID {qid} for {qname} of type {qtype} to server on port {server_port}")
        sock.sendto(message.encode(), server_address)
        data, _ = sock.recvfrom(4096)
        print(data, _, sep='|||')
        print("Received response:")
        decoded_data = data.decode()
        print('###server.py######decoded_data:', decoded_data)  # Print raw data for debugging
        sections = decoded_data.split('||')
        if len(sections) >= 4:
            header, question_section, answer_section, authority_section, additional_section = sections
            print(f"ID: {header.split(',')[0]}\n\nQUESTION SECTION:\n{question_section}\n\nANSWER SECTION:\n{answer_section if answer_section else 'NOT FOUND'}\n\nAUTHORITY SECTION:\n{authority_section if authority_section else 'NOT FOUND'}\n\nADDITIONAL SECTION:\n{additional_section if additional_section else 'NOT FOUND'}")
        else:
            print("Error: Invalid response format.")
    except socket.timeout:
        print("The request timed out")
    finally:
        sock.close()

if __name__ == "__main__":
    if len(sys.argv) != 5:
        print("Usage: python client.py <server_port> <qname> <qtype> <timeout>")
        sys.exit(1)

    server_port = int(sys.argv[1])
    qname = sys.argv[2]
    qtype = sys.argv[3]
    timeout = int(sys.argv[4])

    send_query(server_port, qname, qtype, timeout)
