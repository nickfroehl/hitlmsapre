# non-ambiguous amino acids: (A, R, N, D, C, Q, E, G, H, I, L, K, M, F, P, S, T, W, Y, V)
amino_map = [c for c in "ARNDCQEGHILKMFPSTWYV"]
rev_map: dict[str,str] = {a:hex(i)[2:] for i,a in enumerate(amino_map[:16])}
rev_map['-']=""
rev_map['.']=""
rev_map['_']=""

def read_as_hex(fname: str) -> str:
    with open(fname, 'rb') as f:
        hexdata = f.read().hex()
        return hexdata
def h2amino(hexdata: str) -> str:
    amino_chain = [amino_map[int(nibble,16)] for nibble in hexdata]
    return "".join(amino_chain)
def b2amino(data: bytes) -> str:
    amino_chain = []
    for b in data:
        nib_hi = (b & 0xF0) >> 4
        nib_lo = b & 0x0F
        amino_chain.append(amino_map[nib_hi])
        amino_chain.append(amino_map[nib_lo])
    return "".join(amino_chain)

def amino2hex(peptide: str) -> str:
    nibbles = []
    for c in list(peptide):
        nibbles.append(rev_map[c])
    return "".join(nibbles)

if __name__ == "__main__":
    print(h2amino(read_as_hex('ex.bin')))
