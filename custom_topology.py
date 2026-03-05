from mininet.net import Mininet
from mininet.node import RemoteController, OVSSwitch
from mininet.cli import CLI
from mininet.log import setLogLevel, info
import time

def start_all_outstations(net):
    """Start DNP3 outstations on hosts h2-h18"""
    
    outstation_configs = [
        ('h2', 2), ('h3', 3), ('h4', 4), ('h5', 5), ('h6', 6),
        ('h7', 7), ('h8', 8), ('h9', 9), ('h10', 10), ('h11', 11), 
        ('h12', 12), ('h13', 13), ('h14', 14), ('h15', 15), 
        ('h16', 16), ('h17', 17), ('h18', 18)
    ]
    
    for host_name, station_id in outstation_configs:
        host = net.get(host_name)
        cmd = f'/home/ubuntu/dnp3_310/bin/python3 /home/ubuntu/dnp3_scripts/simple_outstation.py --station-id {station_id}'
        
        info(f'*** Starting outstation on {host_name} (station {station_id})\n')
        host.cmd(f'{cmd} &')
        time.sleep(0.3)
    
    info('*** Waiting for outstations to initialize...\n')
    time.sleep(5)
    info('*** ✅ All outstations started\n')

def start_master(net):
    """Start DNP3 master on h1"""
    h1 = net.get('h1')
    cmd = '/home/ubuntu/dnp3_310/bin/python3 /home/ubuntu/dnp3_scripts/simple_master.py --stations 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 --poll-interval 15'
    
    info('*** Starting DNP3 master on h1...\n')
    h1.cmd(f'{cmd} &')
    time.sleep(2)
    info('*** ✅ Master started\n')

def create_star_mesh_distributed_sdn():
    """
    Topology:
    - 3 ONOS controllers
    - 9 switches (3 per controller)
    - 18 hosts: h1 (DNP3 master) + h2-h18 (DNP3 outstations)
    - Intra-group: first switch connects to other two (mini-star)
    - Inter-group mesh: s1-s4-s7-s1
    """
    net = Mininet(controller=RemoteController, switch=OVSSwitch, autoSetMacs=True)
    
    info('*** Adding 3 ONOS Controllers\n')
    c1 = net.addController('c1', ip='172.20.0.5', port=6653)
    c2 = net.addController('c2', ip='172.20.0.6', port=6653)
    c3 = net.addController('c3', ip='172.20.0.7', port=6653)
    controllers = [c1, c2, c3]
    
    info('*** Adding 9 switches (OpenFlow 1.3)\n')
    switches = []
    for i in range(1, 10):
        sw = net.addSwitch(f's{i}', cls=OVSSwitch, protocols='OpenFlow13')
        switches.append(sw)
    
    info('*** Adding 18 hosts (h1=master, h2-h18=outstations)\n')
    hosts = []
    for i in range(1, 19):
        host_ip = f"10.0.0.{i}/24"
        host = net.addHost(f'h{i}', ip=host_ip)
        hosts.append(host)
    
    info('*** Linking hosts to switches\n')
    for i, sw in enumerate(switches):
        net.addLink(sw, hosts[2*i])
        net.addLink(sw, hosts[2*i + 1])
    
    info('*** Connecting switches within each controller group (mini-star)\n')
    # Group 1: s1-s2, s1-s3
    net.addLink(switches[0], switches[1])
    net.addLink(switches[0], switches[2])
    # Group 2: s4-s5, s4-s6
    net.addLink(switches[3], switches[4])
    net.addLink(switches[3], switches[5])
    # Group 3: s7-s8, s7-s9
    net.addLink(switches[6], switches[7])
    net.addLink(switches[6], switches[8])
    
    info('*** Connecting representative switches in inter-group mesh\n')
    net.addLink(switches[0], switches[3])  # s1-s4
    net.addLink(switches[3], switches[6])  # s4-s7
    net.addLink(switches[6], switches[0])  # s7-s1
    
    info('*** Starting the network\n')
    net.start()
    
    info('*** Assigning switches to controllers\n')
    # Each controller manages its 3 switches
    for sw in switches[0:3]:
        sw.start([c1])
    for sw in switches[3:6]:
        sw.start([c2])
    for sw in switches[6:9]:
        sw.start([c3])
    
    # Wait for network to stabilize
    info('*** Waiting for network to stabilize...\n')
    time.sleep(3)
    
    # Start DNP3 services automatically
    info('*** Starting DNP3 services...\n')
    start_all_outstations(net)
    start_master(net)
    
    info('*** Network Ready — Starting CLI\n')
    info('*** DNP3 Master: h1 (10.0.0.1)\n')
    info('*** DNP3 Outstations: h2-h18 (10.0.0.2-10.0.0.18)\n')
    info('*** Use "pingall" to test connectivity\n')
    info('*** Use "h1 pkill python3" to stop master\n')
    info('*** Use "h2 pkill python3" to stop outstations\n')
    CLI(net)
    
    info('*** Stopping network\n')
    net.stop()

if __name__ == '__main__':
    setLogLevel('info')
    create_star_mesh_distributed_sdn()
