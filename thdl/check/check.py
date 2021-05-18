from . import reset

from . import file_info


def check(filepaths):
    num_violations = 0

    for path in filepaths:
        file_info.FILEPATH = path
        with open(path, encoding='latin-1') as fh:
            for i, line in enumerate(fh, start=1):
                file_info.LINE = line
                file_info.LINE_NUMBER = i

                # Preprocess line.
                l = line.lower().strip()
                if l.startswith("--"):
                    continue
                l = line.split("--")[0]

                if reset.check(l):
                    num_violations += 1

    print("Checked %d files." % len(filepaths))
    if num_violations > 0:
        if num_violations == 1:
            print(f"Found 1 violation.")
        else:
            print(f"Found {num_violations} violations.")
        return 1

    print(f"Found 0 violations.")
    return 0
