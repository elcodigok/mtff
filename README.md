MTFF
====

MikroTik Firewall Framework


File Configuration mtff.yaml
============================

    configuration:
        product:    RB450G
        version:    0.1
        author:     Daniel Maldonado
        comment:    Comment for Firewall

    interfaces:
        ether1:
            ip:
                name:       ether1-wan
                address:    192.168.0.1
                netmask:    255.255.255.0
                network:    192.168.0.0
                comment:    Interface de la WAN

            services:
                accept:     [DNS, HTTP, PROXY]
                deny:       [SSH]

            policy:         drop

        ether2:
            ip:
                name:       ether2-lan
                address:    10.0.0.1
                netmask:    255.255.255.0
                network:    10.0.0.0
                comment:    Interface de la LAN

            services:
                accept:     [DNS, HTTP, PROXY, SSH]
                deny:       [FTP]

            policy:         drop

    router:
        ether2-to-ether1:
            inface:         ether2
            outface:        ether1
            options:        masquerade
            services:
                accept:     [DNS, HTTP, PROXY]
                deny:       [FTP, SSH]

    services:
        DNS :   { tcp: 53, udp: 53 }
        HTTP:   { tcp: 80 } 
        PROXY:  { tcp: 8080 }
        FTP:    { tcp: 21 }
        SSH:    { tcp: 22 }
        WINBOX: { tcp: 8291 }
        TELNET: { tcp: 23 }


Examples
========

    $ python mtff.py -f /home/user/mtff.yaml


Output
======

    #
    # RB450G
    # Date: 2013-07-04
    # Author: Daniel Maldonado
    # Comment: Comment for Firewall
    #
    
    # Deleting all in NAT Rules.
    /ip firewall nat remove [/ip firewall nat find]
    
    # Deleting all in MANGLE Rules.
    /ip firewall mangle remove [/ip firewall mangle find]
    
    # Deleting all in FILTER Rules.
    /ip firewall filter remove [/ip firewall filter find]
    
    # Connection Tracking
    /ip firewall connection tracking
    set enabled=yes generic-timeout=10s icmp-timeout=10s tcp-close-timeout=10s tcp-close-wait-timeout=10s tcp-established-timeout=1d tcp-fin-wait-timeout=10s tcp-last-ack-timeout=10s tcp-syn-received-timeout=5s tcp-syn-sent-timeout=5s tcp-syncookie=no tcp-time-wait-timeout=10s udp-stream-timeout=3m udp-timeout=10s
    
    /ip firewall filter add chain=input in-interface=ether2-lan src-address=10.0.0.0/255.255.255.0 src-port=1024-65535 protocol=udp dst-port=53 action=accept comment="Access granted to DNS - ether2-lan"
    
    /ip firewall filter add chain=input in-interface=ether2-lan src-address=10.0.0.0/255.255.255.0 src-port=1024-65535 protocol=tcp dst-port=53 action=accept comment="Access granted to DNS - ether2-lan"
    
    /ip firewall filter add chain=input in-interface=ether2-lan src-address=10.0.0.0/255.255.255.0 src-port=1024-65535 protocol=tcp dst-port=80 action=accept comment="Access granted to HTTP - ether2-lan"
    
    /ip firewall filter add chain=input in-interface=ether2-lan src-address=10.0.0.0/255.255.255.0 src-port=1024-65535 protocol=tcp dst-port=8080 action=accept comment="Access granted to PROXY - ether2-lan"
    
    /ip firewall filter add chain=input in-interface=ether2-lan src-address=10.0.0.0/255.255.255.0 src-port=1024-65535 protocol=tcp dst-port=22 action=accept comment="Access granted to SSH - ether2-lan"
    
    /ip firewall filter add chain=input in-interface=ether2-lan src-address=10.0.0.0/255.255.255.0 src-port=1024-65535 protocol=tcp dst-port=21 action=drop comment="Access denied to FTP - ether2-lan"
    
    /ip firewall filter add chain=input in-interface=ether1-wan src-address=192.168.0.0/255.255.255.0 src-port=1024-65535 protocol=udp dst-port=53 action=accept comment="Access granted to DNS - ether1-wan"
    
    /ip firewall filter add chain=input in-interface=ether1-wan src-address=192.168.0.0/255.255.255.0 src-port=1024-65535 protocol=tcp dst-port=53 action=accept comment="Access granted to DNS - ether1-wan"
    
    /ip firewall filter add chain=input in-interface=ether1-wan src-address=192.168.0.0/255.255.255.0 src-port=1024-65535 protocol=tcp dst-port=80 action=accept comment="Access granted to HTTP - ether1-wan"
    
    /ip firewall filter add chain=input in-interface=ether1-wan src-address=192.168.0.0/255.255.255.0 src-port=1024-65535 protocol=tcp dst-port=8080 action=accept comment="Access granted to PROXY - ether1-wan"
    
    /ip firewall filter add chain=input in-interface=ether1-wan src-address=192.168.0.0/255.255.255.0 src-port=1024-65535 protocol=tcp dst-port=22 action=drop comment="Access denied to SSH - ether1-wan"
    
    # ether2-to-ether1
    /ip firewall filter add chain=forward in-interface=ether2-lan src-address=10.0.0.0/255.255.255.0 out-interface=ether1-wan dst-address=192.168.0.0/255.255.255.0 src-port=1024-65535 protocol=udp dst-port=53 action=accept comment="ether2-to-ether1 - DNS"
    
    /ip firewall filter add chain=forward in-interface=ether2-lan src-address=10.0.0.0/255.255.255.0 out-interface=ether1-wan dst-address=192.168.0.0/255.255.255.0 src-port=1024-65535 protocol=tcp dst-port=53 action=accept comment="ether2-to-ether1 - DNS"
    
    /ip firewall filter add chain=forward in-interface=ether2-lan src-address=10.0.0.0/255.255.255.0 out-interface=ether1-wan dst-address=192.168.0.0/255.255.255.0 src-port=1024-65535 protocol=tcp dst-port=80 action=accept comment="ether2-to-ether1 - HTTP"
    
    /ip firewall filter add chain=forward in-interface=ether2-lan src-address=10.0.0.0/255.255.255.0 out-interface=ether1-wan dst-address=192.168.0.0/255.255.255.0 src-port=1024-65535 protocol=tcp dst-port=8080 action=accept comment="ether2-to-ether1 - PROXY"
    
    /ip firewall filter add chain=forward in-interface=ether2-lan src-address=10.0.0.0/255.255.255.0 out-interface=ether1-wan dst-address=192.168.0.0/255.255.255.0 src-port=1024-65535 protocol=tcp dst-port=21 action=drop comment="ether2-to-ether1 - FTP"
    
    /ip firewall filter add chain=forward in-interface=ether2-lan src-address=10.0.0.0/255.255.255.0 out-interface=ether1-wan dst-address=192.168.0.0/255.255.255.0 src-port=1024-65535 protocol=tcp dst-port=22 action=drop comment="ether2-to-ether1 - SSH"
    
    /ip firewall nat add chain=srcnat out-interface=ether1-wan action=masquerade src-address=10.0.0.0/255.255.255.0 comment="Configuration NAT for ether2-to-ether1"
    
    /ip firewall filter add chain=input in-interface=ether2-lan action=drop comment="Default Policy to ether2-lan - INPUT"
    
    /ip firewall filter add chain=forward in-interface=ether2-lan action=drop comment="Default Policy to ether2-lan - FORWARD"
    
    /ip firewall filter add chain=forward out-interface=ether2-lan action=drop comment="Default Policy to ether2-lan - FORWARD"
    
    /ip firewall filter add chain=output out-interface=ether2-lan action=drop comment="Default Policy to ether2-lan - OUTPUT"
    
    /ip firewall filter add chain=input in-interface=ether1-wan action=drop comment="Default Policy to ether1-wan - INPUT"
    
    /ip firewall filter add chain=forward in-interface=ether1-wan action=drop comment="Default Policy to ether1-wan - FORWARD"
    
    /ip firewall filter add chain=forward out-interface=ether1-wan action=drop comment="Default Policy to ether1-wan - FORWARD"
    
    /ip firewall filter add chain=output out-interface=ether1-wan action=drop comment="Default Policy to ether1-wan - OUTPUT"
