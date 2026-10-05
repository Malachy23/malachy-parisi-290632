import sys
from metro import Metro

def main():
    metro = Metro()

    for raw_line in sys.stdin:
        line = raw_line.rstrip("\n")
        if not line.strip():
            continue

        tokens = line.split()
        metro.dispatch(tokens)

        for output_line in metro.output:
            print(output_line)

main()