def extract_substrings_line(line, substring_length, stride, cur_substrings):
    line = line.strip()
    line_length = len(line)
    idx = 0

    substrings = []

    if len(line) < substring_length:
        print("Error: found line with length < substring_length. Padding with 0's.")
        substrings += line.ljust(substring_length, '0')
        return substrings


    while idx < line_length - substring_length:
        substring = line[idx:idx+substring_length]
        if substring not in cur_substrings:
            substrings.append(substring)
        idx += stride

    final_substring = line[line_length-substring_length:]
    if final_substring not in cur_substrings:
        substrings.append(final_substring)
    return substrings

def extract_strings_train(folder, inname, outname, substring_length, stride):
    substrings = []
    with open(folder + inname, "r") as f:
        for line in f:
            line_substrings = extract_substrings_line(line, substring_length, stride, substrings)
            substrings += line_substrings


    with open(folder + outname, 'w') as f:
        for item in substrings:
            f.write(f"{item}\n")


def extract_strings_test(folder, inname, substring_length, stride):

    fn_test = folder + inname + ".test"
    fn_labels = folder + inname + ".labels"

    test_file = open(fn_test, 'r')
    labels = open(fn_labels, 'r')

    substrings_normal = []
    line_nrs_normal = []

    substrings_anom = []
    line_nrs_anom = []

    line_idx = 1

    for line in test_file:
        label = int(labels.readline())
        line_substrings = extract_substrings_line(line, substring_length, stride, [])
        line_nrs = [line_idx] * len(line_substrings)
        if label == 0:
            substrings_normal += line_substrings
            line_nrs_normal += line_nrs
        elif label == 1:
            substrings_anom += line_substrings
            line_nrs_anom += line_nrs
        else:
            print("Can't interpret label.")

        line_idx += 1

    with open(fn_test+'.normal', 'w') as f:
        for item in substrings_normal:
            f.write(f"{item}\n")

    with open(fn_test+'.anom', 'w') as f:
        for item in substrings_anom:
            f.write(f"{item}\n")

    with open(fn_test+'.normal.linenrs', 'w') as f:
        for item in line_nrs_normal:
            f.write(f"{item}\n")

    with open(fn_test+'.anom.linenrs', 'w') as f:
        for item in line_nrs_anom:
            f.write(f"{item}\n")


