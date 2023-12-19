from scapy.all import *
from .scapy_additions import *
import random

alpha_hi = "ABCDEFGHIJKLMNOPQRSTUVWZYZ"
alpha_lo = alpha_hi.lower()
alpha = bytes(alpha_hi + alpha_lo, 'ascii')
alpha_hi = bytes(alpha_hi, 'ascii')
alpha_lo = bytes(alpha_lo, 'ascii')

class Proto1(Packet):
    """
    Header, Fixed-Len Cstr, Footer
    Ratio 4:5 of fixed to variable values, and wrapped on either side
    Literally can't mess this up
    """
    name = "Protocol 1"
    fields_desc = [
        XIntField("header", 0xff8eade4),
        StrFixedLenField("rand_str", RandString(10, alpha), length=10),
        XIntField("footer", 0xfff007e4)
    ]
    def guess_payload_class(self, s):
        return None

class Proto2(Packet):
    """
    Header, Variable-Len Cstr, Footer
    Length ranges 6 to 26 bytes (incl nullbyte)
    Expect to have actual gaps in our output
    """
    name = "Protocol 2"
    fields_desc = [
        XIntField("header", 0xff8eade4),
        StrNullField("rand_str", RandString(RandNum(6,25), alpha)),
        XIntField("footer", 0xfff007e4)
    ]
    def guess_payload_class(self, s):
        return None

class Proto3(Packet):
    """
    Header, Varstr, Int, Varstr, Footer; Varstr is a Choice length, falling into Cases! independently
    Shorter lengths for these var strs to not muck things up too bad, and a bit less variation
    Ideal here would be to have thoughts of distinguishing value ranged, though nibbles hurt these chances anyways
    Expect to have actual gaps in our output
    """
    name = "Protocol 3"
    len_options = [1,3,7]
    
    fields_desc = [
            XIntField("header", 0xff8eade4),
            StrNullField("str1", RandString(RandNumChoice(len_options), alpha)),
            XIntField("mid_int", RandInt()),
            StrNullField("str2", RandString(RandNumChoice(len_options), alpha)),
            XIntField("footer", 0xfff007e4)
    ]
    
    def guess_payload_class(self, s):
        return None
        
class Proto4(Packet):
    """
    Header, Age, Firstname, Lastname, Footer
    """
    name = "Protocol 4"
    
    fields_desc = [
            XIntField("header", 0xff8eade4),
            XByteField("age", RandEnum(16,55)),
            ByteField("f_firstname", RandNumChoice(list(alpha_hi))),
            StrNullField("rem_firstname", RandString(RandEnum(2,9), alpha_lo)),
            ByteField("f_lastname", RandNumChoice(list(alpha_hi))),
            StrNullField("rem_lastname", RandString(RandEnum(2,9), alpha_lo)),
            XIntField("footer", 0xfff007e4)
    ]
    
    def guess_payload_class(self, s):
        return None

class Proto5(Packet):
    """
    Header, Age, Firstname, Middle Initial, Dot, Lastname, Footer
    """
    name = "Protocol 5"
    
    fields_desc = [
            XIntField("header", 0xff8eade4),
            XByteField("age", RandEnum(16,55)),
            ByteField("f_firstname", RandNumChoice(list(alpha_hi))),
            StrNullField("rem_firstname", RandString(RandEnum(2,9), alpha_lo)),
            ByteField("middle_initial", RandNumChoice(list(alpha_hi))),
            ByteField("dot", ord('.')),
            ByteField("mi_nullbyte", 0x00),
            ByteField("f_lastname", RandNumChoice(list(alpha_hi))),
            StrNullField("rem_lastname", RandString(RandEnum(2,9), alpha_lo)),
            XIntField("footer", 0xfff007e4)
    ]
    
    def guess_payload_class(self, s):
        return None

class Proto6(Packet):
    """
    Age, Firstname, Middle Initial, Dot, Lastname, Relationship, [Partner]
    """
    name = "Protocol 6"
    relationships = {0:"single",1:"dating",2:"married"}
    
    fields_desc = [
            XByteField("age", RandEnum(16,55)),
            ByteField("f_firstname", RandNumChoice(list(alpha_hi))),
            StrNullField("rem_firstname", RandString(RandEnum(2,9), alpha_lo)),
            ByteField("middle_initial", RandNumChoice(list(alpha_hi))),
            ByteField("dot", ord('.')),
            ByteField("mi_nullbyte", 0x00),
            ByteField("f_lastname", RandNumChoice(list(alpha_hi))),
            StrNullField("rem_lastname", RandString(RandEnum(2,9), alpha_lo)),
            ByteEnumField("relationship", RandEnum(0,2), relationships)
    ]
    
    def guess_payload_class(self, s):
        if self.relationship == 1:
            return Proto6_Paramour
        elif self.relationship == 2:
            return Proto6_Spouse
        elif self.relationship == 0:
            return None
        else:
            return None
            
class Proto6_Paramour(Packet):
    """
    Age, Firstname, Lastname
    """
    name = "Protocol 6 Paramour"
    
    fields_desc = [
            XByteField("age", RandEnum(16,55)),
            ByteField("f_firstname", RandNumChoice(list(alpha_hi))),
            StrNullField("rem_firstname", RandString(RandEnum(2,9), alpha_lo)),
            ByteField("f_lastname", RandNumChoice(list(alpha_hi))),
            StrNullField("rem_lastname", RandString(RandEnum(2,9), alpha_lo)),
    ]
    
    def guess_payload_class(self, s):
        return None
class Proto6_Spouse(Packet):
    """
    Age, Firstname, (Assume same last name)
    """
    name = "Protocol 6 Spouse"
    
    fields_desc = [
            XByteField("age", RandEnum(16,55)),
            ByteField("f_firstname", RandNumChoice(list(alpha_hi))),
            StrNullField("rem_firstname", RandString(RandEnum(2,9), alpha_lo)),
    ]
    
    def guess_payload_class(self, s):
        return None
class Proto6_Pets(Packet):
    """
    Count, (foreach) Name
    """
    name = "Protocol 6 Pets"
    
    fields_desc = [
            ByteField("number_of_pets", RandEnum(0,3)),
            FieldListField(
                "pet_names", 
                None,
                StrNullField("name", RandString(RandEnum(3,9), alpha_lo)),
                count_from = lambda pkt: pkt.number_of_pets,
            ),
    ]
    
    def guess_payload_class(self, s):
        return None

# DATA for TransportedProto6
class T6_Config():
    user_ips = ['50.103.237.192', '207.191.152.59', '191.202.75.143', '125.152.122.115', '69.61.244.66', '14.27.37.161', '192.32.54.40', '62.237.223.16', '28.227.89.254', '147.95.4.63', '154.54.183.96', '98.36.77.249', '107.239.127.120', '112.78.224.43', '83.215.46.127', '95.113.164.215', '6.234.93.177', '170.148.0.167', '156.100.81.113', '225.142.52.40', '192.42.133.206', '160.132.136.70', '15.9.143.147', '47.105.235.168']
    src_ip_template = RandIPChoice(user_ips)
    internal_range = '192.168.0.0/22'
    dst_ip_template = RandIP(iptemplate=internal_range)
    router_macs = ['8b:62:1e:0e:d4:82', '8a:f8:df:6b:6b:7b', '53:dc:b9:68:ae:c1', 'b4:1b:ae:3c:cd:ee', '54:88:22:e9:bd:1a', '18:0e:0c:05:98:7a', 'd3:c6:d1:c7:98:da', '7b:fa:5b:c7:b3:08']
    src_mac_template = RandMACChoice(router_macs)
    dst_mac_template = RandMAC()
    srcport_template = RandNum(2048,40000)
    dstport = 2828  # even though we explicitly build in the payload, it won't get show2()d for test_ unless also bound
bind_layers(UDP, Proto6, dport=T6_Config.dstport)
# bind_layers(Proto6, Proto6_Paramour, relationship=1)
# bind_layers(Proto6, Proto6_Spouse, relationship=2)
# composed invoked "class", to treat as already-inst instead of instantiating, within scapy_utils
TransportedProto6 = (
    Ether(
        dst=T6_Config.dst_mac_template,
        src=T6_Config.src_mac_template
    ) / IP(
        dst=T6_Config.dst_ip_template,
        src=T6_Config.src_ip_template
    ) / UDP(
        sport=T6_Config.srcport_template,
    ) / Proto6()
)