from . import reset


def check(filepaths):
    num_violations = False

    for path in filepaths:
        with open(path, encoding='latin-1') as fh:
            for i, line in enumerate(fh, start=1):
                # Preprocess line.
                l = line.lower().strip()
                if l.startswith("--"):
                    continue
                l = line.split("--")[0]

                msg = reset.check(l)
                if msg:
                    num_violations += 1
                    print(f"{path}:{i}")
                    print(line, end="")
                    print(msg + "\n")

    if num_violations > 0:
        if num_violations == 1:
            print(f"Found 1 violation.")
        else:
            print(f"Found {num_violations} violations.")
        return 1

    return 0
