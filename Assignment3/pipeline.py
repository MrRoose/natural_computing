from preprocess_nc import extract_strings_train, extract_strings_test
from postprocess_nc import combine_preds
from luna import load_files, calc_sp_se, plot_auc, print_auc
import subprocess

jar_folder = "C:/negative-selection/"
data_folder = "C:/negative-selection/syscalls/snd-cert/"
fn_train = "snd-cert.train"
fn_test_base = "snd-cert.all"
fn_test = "snd-cert.all.test"
fn_test_labels = "snd-cert.all.labels"

best_auc = 0
best_params = []

for substring_length in range(7, 7+1):
    for stride in range(1, substring_length+1):
        # Extract substrings of training data
        extract_strings_train(data_folder, fn_train, fn_train + '.substrings', substring_length, stride)
        extract_strings_test(data_folder, fn_test_base, substring_length, stride)
        for r in range(2, substring_length+1):
            # Run jar
            subprocess.run(f'java -jar C:/negative-selection/negsel2.jar -self {data_folder + fn_train} -n {substring_length} -r {r} -c -l < {data_folder + fn_test}.normal > {data_folder + fn_test}.normal.vals', shell=True)
            subprocess.run(f'java -jar C:/negative-selection/negsel2.jar -self {data_folder + fn_train} -n {substring_length} -r {r} -c -l < {data_folder + fn_test}.anom > {data_folder + fn_test}.anom.vals', shell=True)

            combine_preds(data_folder, fn_test + '.normal')
            combine_preds(data_folder, fn_test + '.anom')

            p_title = f'substring_length = {substring_length}, stride = {stride}, r = {r}'
            conc_outp, t_outp, e_outp = load_files(data_folder + fn_test + '.anom.combined', data_folder + fn_test + '.normal.combined')
            sensitivities, specificities = calc_sp_se(conc_outp, t_outp, e_outp)
            auc = print_auc(sensitivities, specificities, p_title)
            if auc > best_auc:
                best_auc = auc
                best_params = [substring_length, stride, r]

print(best_auc)
print(best_params)