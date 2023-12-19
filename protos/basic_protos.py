from scapy.all import *

class Disney(Packet):
    name = "DisneyPacket "
    fields_desc=[ ShortField("mickey",5),
                 XByteField("minnie",3) ,
                 IntEnumField("donald" , 1 ,
                      { 1: "happy", 2: "cool" , 3: "angry" } ) ]
    def guess_payload_class(self, s):
        if self.donald != 3:
            return None
        else:
            return None

class Proto0(Packet):
    """
    Header, Int Data, Footer, in a 2:1 fixed-to-random ratio, all fixed-len, all bounded
    Literally can't mess this up
    """
    name = "Protocol 0"
    fields_desc = [
        XIntField("header", 0x8eade4),
        XIntField("rand_val", RandInt()),
        XIntField("footer", 0x00f007e4)
    ]
    def guess_payload_class(self, s):
        return None

def do_disney():
    a = Disney(mickey=4, minnie=0xa0034c, donald="angry")
    a.show()
    for i in range(3):
        # _a = fuzz(Disney(donald=RandEnum(1,3)))
        _a = Disney(donald=RandEnum(1,3))
        _a.show2()