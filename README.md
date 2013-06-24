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