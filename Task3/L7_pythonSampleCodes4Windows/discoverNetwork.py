# Sample Source code modified from :
# 'Violent Python...' by TJ.O'conner, p.84
# By Karl Kwan July 2016
# source file: discoverNetwork.py
# Explore the window registry to discover the Wifi SSID and
# MAC address of any previously connected access points.
# To run: need administrator privilege
# open a cmd prompt "run as administrator"
# python discoverNetwork.py
#
from _winreg import *
def val2addr(val):
    if not val:
        return ''
    addr = ''
    for ch in val:
        addr += '%02x '% ord(ch)
    addr = addr.strip(' ').replace(' ', ':')[0:17]
    return addr
def printNets():
    net = "SOFTWARE\Microsoft\Windows NT\CurrentVersion"+\
"\NetworkList\Signatures\Unmanaged"
    key = OpenKey(HKEY_LOCAL_MACHINE, net)
    print '\n[*] Networks You have Joined.'
    for i in range(100):
        try:
             
            guid = EnumKey(key, i)
            netKey = OpenKey(key, str(guid))
            (n, addr, t) = EnumValue(netKey, 5)
            (n, name, t) = EnumValue(netKey, 4)
            if addr:
                macAddr = val2addr(addr)
                netName = str(name)
                print '[+] ' + netName + ' ' + macAddr
            CloseKey(netKey)
        except Exception as inst:
            #print str(inst)
            break
def main():
    printNets()
if __name__ == "__main__":
    main()
