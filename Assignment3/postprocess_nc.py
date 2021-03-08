## Combine values per line

# folder = "C:\\Users\\Daan Roos\\iCloudDrive\\Documents\\School\\NaturalComputing\\ass3\\negative-selection\\negative-selection\\syscalls\\snd-cert\\"
# name_vals = "snd-cert.1.normal.vals"
# name_nrs = "snd-cert.1.normal.linenrs"
# name_output = "snd-cert.1.normal.lines.vals"
# vals = open(folder + name_vals, "r")
# line_nrs = open(folder + name_nrs, "r")
#
# cur_line_nr = int(line_nrs.readline().strip())
# cur_val = float(vals.readline().strip())
# cur_n = 1
#
# new_vals = []
#
# for line in line_nrs:
#     line = line.strip()
#     line_nr = int(line)
#     if cur_line_nr == line_nr:
#         cur_val += float(vals.readline().strip())
#         cur_n += 1
#     else:
#         new_vals += [cur_val / cur_n]
#         cur_line_nr = line_nr
#         cur_val = float(vals.readline().strip())
#         cur_n = 1
#
# new_vals += [cur_val / cur_n]
#
# vals.close()
# line_nrs.close()
#
#
# with open(folder + name_output, 'w') as f:
#     for item in new_vals:
#         f.write(f"{item}\n")

def combine_preds(folder, inname):
    vals = open(folder + inname + '.vals', "r")
    line_nrs = open(folder + inname + '.linenrs', "r")

    cur_line_nr = int(line_nrs.readline().strip())
    cur_val = float(vals.readline().strip())
    cur_n = 1

    new_vals = []

    for line in line_nrs:
        line = line.strip()
        line_nr = int(line)
        if cur_line_nr == line_nr:
            cur_val += float(vals.readline().strip())
            cur_n += 1
        else:
            new_vals += [cur_val / cur_n]
            cur_line_nr = line_nr
            cur_val = float(vals.readline().strip())
            cur_n = 1

    new_vals += [cur_val / cur_n]

    vals.close()
    line_nrs.close()

    with open(folder + inname + '.combined', 'w') as f:
        for item in new_vals:
            f.write(f"{item}\n")