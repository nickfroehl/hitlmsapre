from utils.convert import amino_map

# DIST_FUNC: lambda (x:int,y:int) -> int
def absdiff_or_bonus(x,y,z):
    if x != y:
        return -1 * abs(x-y)
    else:
        return z

def apply_bonus(z):
    return lambda x,y: absdiff_or_bonus(x,y,z)

def range_wrap(x,y,dist_func):
    if x < 16 and y < 16 and x >= 0 and y >= 0:
        return dist_func(x,y)
    else:
        return 0

def apply_wrap(dist_func):
    return lambda x,y: range_wrap(x,y,dist_func)

def compute_matrix(dist_func):
    return [[dist_func(x,y) for y in range(20)] for x in range(20)]
def print_matrix(matrix):
    spaced_map = '  '.join(amino_map)
    header_line = f"{' '*3}{spaced_map}"
    rows = [header_line]
    for x in range(len(matrix)):
        # screw max-size based alignment and multiple spaces
        # it should just process space-separated, and it'll get that; deal with it
        row_char = amino_map[x]
        spaced_vals = ' '.join([str(y) for y in matrix[x]])
        row = f"{row_char}{' '*1}{spaced_vals}"
        rows.append(row)
    print('\n'.join(rows))

if __name__ == "__main__":
    print_matrix(compute_matrix(apply_wrap(apply_bonus(12))))
