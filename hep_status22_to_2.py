import shutil
import sys

if len(sys.argv) != 3:
    print("Usage: python script.py <src_path> <dst_path>")
    sys.exit(1)

src = sys.argv[1]
dst = sys.argv[2]

try:
    with open(src, 'r') as fin, open(dst, 'wt') as fout:
        LLP_PDG = '9900012'

        for line in fin:
            if LLP_PDG in line:
                line2 = line[:-3] + "2\n"
                fout.write(line2)
            else:
                fout.write(line)

    print(f"Conversion completed from {src} to {dst}")

except Exception as e:
    print(f"Error: {e}")
    sys.exit(1)

