import os

from argparse import ArgumentParser
from hashlib import sha256

def file_checksum(checksum: str, fpath: str) -> bool:
    m = sha256()
    with open(fpath, "rb") as f:
        data = f.read()
        m.update(data)
    
    return m.hexdigest() == checksum

if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument("--path")
    parser.add_argument("--header", action="store_true", default=True)

    args = parser.parse_args()

    with open(args.path, "r") as f:
        all_lines = f.readlines()

    if args.header is True:
        start_ind = 1
    else:
        start_ind = 0

    source_dir = os.path.dirname(args.path)

    mismatched_lines = []
    for ind in range(start_ind, len(all_lines)):
        line = all_lines[ind]
        checksum, fpath = line.split()
        abs_path = os.path.join(source_dir, fpath)
        val = file_checksum(checksum=checksum, fpath=abs_path)
        if val is False:
            nline = line.strip() + " " + str(val) + "\n"
            mismatched_lines.append(nline)

    with open("comparisons.txt", "w") as f:
        f.writelines(mismatched_lines)
        