# Security report 

import subprocess 
import json # when dealing with json data import json, less headache in prasing

# cpu architecutire

architecture = subprocess.run(
    'lscpu | grep -i "Model name" | cut -d ":" -f 2| xargs',
    capture_output=True,
    shell=True,
    text=True
    
    
)

print(f"CPU MODEL: {architecture.stdout}")

# how much ram is present

ram = subprocess.run(
    ["free","-h"],
    capture_output=True,
    text=True
)

lines = ram.stdout.splitlines() # splits a string into a list of separate lines

line = lines[1].split()

total_ram = line[1]
used_ram = line[2]
free_ram = line[3]

print(f"Total RAM: {total_ram}")
print(f"Used RAM: {used_ram}")
print(f"Free RAM: {free_ram}")

# -- 
# memory 

memory = subprocess.run(
    ["df","-h","/"],
    capture_output=True,
    text=True
)

print()
#print(memory.stdout)
lines = memory.stdout.splitlines()

memory_data = lines[1].split()

disk = memory_data[0]
total_space = memory_data[1]
used_space = memory_data[2]
avaliable_space = memory_data[3]
used_percentage = memory_data[4]

print()
print(f"Disk: {disk}")
print(f"Total Space: {total_space}")
print(f"Used Space: {used_space}")
print(f"Available Space: {avaliable_space}")
print(f"Used Percentage: {used_percentage}")

# disk partition

disk_partition = subprocess.run(
    ["lsblk","-J"],
    capture_output=True,
    text=True
)
print()

#print(disk_partition.stdout)
# load -> reads the json from a file
# loads -> reads the json from a String

d = json.loads(disk_partition.stdout) # now its a proper dictionary
disk_json = d["blockdevices"]

for device in disk_json:
    print(f"Name of the device: {device["name"]}")

    if device.get("children",[]):
        print(f"Partition Exists for {device["name"]}")
        print("Listing it out....")
        print()

        for partition in device.get("children",[]):
            print(f"Name: {partition["name"]}")
            print(f"Size: {partition["size"]}")
            print(f"Mountpoints: {partition["mountpoints"]}")
            print("-"*25)

    print()


# -- 
# user / service details 
#

userandservice = subprocess.run(
    'cat /etc/passwd | cut -d ":" -f 1,6,7',
    shell=True,
    capture_output=True,
    text=True
)


data = userandservice.stdout.splitlines()

for user in data:
    info = user.split(":")
    print(f"Username: {info[0]}")
    print(f"Home: {info[1]}")
    print(f"Shell: {info[2]}")
    print()

# -- 
# getting all the network interaces ipv4 address and its interfaces

ipv4 = subprocess.run(
    ["ip","-4","-o","addr"],
    capture_output=True,
    text=True
)

print()
#print(ipv4.stdout)

ipv4_lines = ipv4.stdout.splitlines()

for line in ipv4_lines:
    interface = line.split()
    ip = interface[3]

    if ip.startswith("127."):
        continue

    print(f"Interface: {interface[1]}")
    print(f"IPV4 Address: {interface[3]}")

#--
# printing ipv6 adddress

ipv6 = subprocess.run(
    ["ip","-6","-o","addr"], # new learn
    capture_output=True,
    text=True
)

ipv6_lines = ipv6.stdout.splitlines()

for line in ipv6_lines:
    interface = line.split()

    if interface[3].startswith("::1"):
        continue

    print(f"Interface: {interface[1]}")
    print(f"IPV6: {interface[3]}")

print()

# -- 
#printing the default gateway 
gateway = subprocess.run(
    ["ip","route"],
    capture_output=True,
    text=True
)

gateway_lines = gateway.stdout.splitlines()

for line in gateway_lines:
    default = line.split()

    if default[0] == "default":
        print(f"The default Gateway is: {default[2]} of interface: {default[4]}")

print()
#-- 
# dns server resolver

dns = subprocess.run(
    ["cat", "/etc/resolv.conf"],
    capture_output=True,
    text=True 
)

dns_lines = dns.stdout.splitlines()[1:]


for line in dns_lines:
    dns_data = line.split()
    print(f"Name Server: {dns_data[1]}")



# --
# counting the tcp and udp connections
# Local Address:Port → Where MY program is listening/connected
# Peer Address:Port  → Where the OTHER endpoint is
# State              → Current TCP connection state

tcpandudp = subprocess.run(
    ["ss","-tuln"],
    capture_output=True,
    text=True
)

tcp_udp_lines = tcpandudp.stdout.splitlines()
tcp = []
udp = []


for line in tcp_udp_lines:
    data = line.split()

    # only the listning ports
    if data[1] == "LISTEN" and data[0] == "tcp":
        tcp.append(data[4])

    elif data[1] == "LISTEN" and data[0] == "udp":
        udp.append(data[4])

print()

if tcp:
    print("TCP: local <address:port>")
    for address in tcp:
        add,port = address.split(":")
        print(f"{add}:{port}")

print()
if udp:
    print("UDP: local <address:port>")
    for address in udp:
        add,port = address.split(":")
        print(f"{add}:{port}")


# mistake .counts -> counts the arg u pass to it not the cntents of the list
print(f"Total TCP: {len(tcp)}")
print(f"Total UDP: {len(udp)}")

# ---------
# counting logs

failed_pass = subprocess.run(
    'journalctl | grep -i "Failed password"',
    shell=True,
    capture_output=True,
    text=True
)

print(f"Failed Password: {len(failed_pass.stdout.splitlines())}")


authentication_failure = subprocess.run(
    'journalctl | grep -i "authentication failure"',
    shell=True,
    capture_output=True,
    text=True
)

print(f"Authentication failure: {len(authentication_failure.stdout.splitlines())}")

Permission_denied = subprocess.run(
    'journalctl | grep -i "Permission denied"',
    shell=True,
    capture_output=True,
    text=True
)

print(f"Permission_denied: {len(Permission_denied.stdout.splitlines())}")

#

sudo = subprocess.run(
    'journalctl | grep -i "sudo"',
    shell=True,
    capture_output=True,
    text=True
)

print(f"sudo: {len(sudo.stdout.splitlines())}")


#
ssh = subprocess.run(
    'journalctl | grep -i "ssh"',
    shell=True,
    capture_output=True,
    text=True
)

print(f"ssh: {len(ssh.stdout.splitlines())}")

#
error = subprocess.run(
    'journalctl | grep -i "error"',
    shell=True,
    capture_output=True,
    text=True
)

print(f"error: {len(error.stdout.splitlines())}")

#
warning = subprocess.run(
    'journalctl | grep -i "warning"',
    shell=True,
    capture_output=True,
    text=True
)

print(f"warning: {len(warning.stdout.splitlines())}")