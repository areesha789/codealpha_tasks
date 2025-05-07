from scapy.all import sniff
from scapy.layers.inet import IP, TCP, UDP

# Callback function for each captured packet
def packet_callback(packet):
    if IP in packet:
        ip_layer = packet[IP]
        print(f"\n[+] IP Packet: {ip_layer.src} -> {ip_layer.dst}")

        if TCP in packet:
            tcp_layer = packet[TCP]
            print(f"    TCP Port: {tcp_layer.sport} -> {tcp_layer.dport}")
        elif UDP in packet:
            udp_layer = packet[UDP]
            print(f"    UDP Port: {udp_layer.sport} -> {udp_layer.dport}")

# Start sniffing (change iface name if needed)
print("Starting packet capture... Press Ctrl+C to stop.\n")
sniff(prn=packet_callback, store=False)
