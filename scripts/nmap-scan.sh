sudo nmap -sS -p 22 192.168.0.0/24
ssh root@192.168.0.101


# Tests with using the phone
sudo nmap -sS -p 22 172.20.10.0/24


# NODE 1
ssh root@172.20.10.6
ssh-keygen -f "/home/arturo/.ssh/known_hosts" -R "172.20.10.6"

# NODE 2
ssh root@172.20.10.5
ssh-keygen -f "/home/arturo/.ssh/known_hosts" -R "172.20.10.5"

# NODE 3
ssh root@172.20.10.7
ssh-keygen -f "/home/arturo/.ssh/known_hosts" -R "172.20.10.7"

# NODE 4
ssh root@172.20.10.8
ssh-keygen -f "/home/arturo/.ssh/known_hosts" -R "172.20.10.8"

# NODE 5
ssh root@172.20.10.9
ssh-keygen -f "/home/arturo/.ssh/known_hosts" -R "172.20.10.9"
