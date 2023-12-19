from scapy.all import *
from utils.convert import b2amino

def show_proto(proto: Packet, count: int = 5):
    if isinstance(proto, scapy.base_classes.Packet_metaclass):  # actual class
        inst = proto()
    else:   # already instantiated; assume it is a composed instance
        inst = proto
        proto = proto.__class__
    for i in range(count):
        cur = proto(inst.build())
        prev = cur
        dig = cur
        while dig is not None and not isinstance(dig, NoPayload) and not isinstance(dig, Padding):
            print(f"{dig.__class__.__name__} has payload {dig.payload.__class__.__name__}")
            prev = dig
            dig = dig.payload
        next_layer = prev.guess_payload_class(b'')
        # print(f"next_layer from {prev} is {next_layer}")
        # print(f"starting loop, cur is {cur}")
        while next_layer is not None and next_layer is not Raw and next_layer is not Padding:
            cur = proto((cur / next_layer()).build())
            prev = cur
            dig = cur
            while dig is not None and not isinstance(dig, NoPayload) and not isinstance(dig, Padding):
                # print(f"{dig.__class__.__name__} has payload {dig.payload.__class__.__name__}")
                prev = dig
                dig = dig.payload
            if isinstance(dig, Padding):
                break
            next_layer = prev.guess_payload_class(b'')
            # print(f"{prev.__class__.__name__} guesses payload {next_layer}")
        # print(f"cur is {cur} at end")
        cur.show2()
        # print(cur.build())
        print(cur.build())

# todo: can also make a lambda -> Packet if need higher level logic for field setting or distributions etc.
def gen_proto(proto: Packet, count: int = 5) -> list[str]:
    out: list[str] = []
    
    if isinstance(proto, scapy.base_classes.Packet_metaclass):  # actual class
        inst = proto()
    else:   # already instantiated; assume it is a composed instance
        inst = proto
        proto = proto.__class__
    for i in range(count):
        cur = proto(inst.build())
        prev = cur
        dig = cur
        while dig is not None and not isinstance(dig, NoPayload) and not isinstance(dig, Padding):
            prev = dig
            dig = dig.payload
        next_layer = prev.guess_payload_class(b'')
        while next_layer is not None and next_layer is not Raw and next_layer is not Padding:
            cur = proto((cur / next_layer()).build())
            prev = cur
            dig = cur
            while dig is not None and not isinstance(dig, NoPayload) and not isinstance(dig, Padding):
                prev = dig
                dig = dig.payload
            if isinstance(dig, Padding):
                break
            next_layer = prev.guess_payload_class(b'')
        out.append(b2amino(cur.build()))
    return out

def to_fasta(seqs: list[str]) -> str:
    pile: list[str] = []
    for i,seq in enumerate(seqs):
        pile.append(f">seq{i}\n{seq}")
    # to add trailing newline at end of file
    pile.append("")
    return "\n".join(pile)

def write_str(fname: str, s: str) -> None:
    with open(fname, "w") as f:
        f.write(s)
