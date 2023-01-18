import sys

if __name__ == '__main__':
    filename = sys.argv[1]

    with open(filename, 'r') as f:
        lines = f.readlines()

    newlines = [lines[0]]

    t  = 0.0
    dt = 0.05

    for line in lines[1:]:
        elems = line.split(',')
        new = f'[{round(t,2)},{elems[1]},{elems[2]}'
        newlines.append(new)
        t += dt

    with open(f'{filename}.out', 'w') as f:
        f.write(''.join(newlines))

