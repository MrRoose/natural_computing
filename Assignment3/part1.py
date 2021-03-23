from preprocess_nc import extract_strings_train, extract_strings_test
from postprocess_nc import combine_preds
from luna import load_files, calc_sp_se, plot_auc, print_auc
import subprocess

jar_folder = "C:/negative-selection/"
data_folder = "C:/negative-selection/"
results_folder = "C:/negative-selection/"
fn_train = "english.train"

fn_test_norm = "english.test"
fn_test_anom = "tagalog.txt"
#fn_test_anom = "plautdietsch.txt"

best_auc = 0
best_params = []
best_plt = []

substring_length = 10

for r in range(1, substring_length):
    # Run jar
    subprocess.run(f'java -jar negsel2.jar -self {data_folder + fn_train} -n {substring_length} -r {r} -c -l < {data_folder + fn_test_norm} > {data_folder + fn_test_norm}.vals', shell=True)
    subprocess.run(f'java -jar negsel2.jar -self {data_folder + fn_train} -n {substring_length} -r {r} -c -l < {data_folder + fn_test_anom} > {data_folder + fn_test_anom}.vals', shell=True)

    p_title = f'substring_length = {substring_length}, r = {r}, anomaly = {fn_test_anom.split(".")[0]}'
    conc_outp, t_outp, e_outp = load_files(data_folder + fn_test_anom + '.vals', data_folder + fn_test_norm + '.vals')
    sensitivities, specificities = calc_sp_se(conc_outp, t_outp, e_outp)
    auc = print_auc(sensitivities, specificities, p_title)
    if auc > best_auc:
        best_auc = auc
        best_params = [substring_length, r]
        best_sens = sensitivities
        best_spec = specificities
        best_title = p_title
    # plot every AUC
    #path = f'{results_folder}auc_{fn_test_anom.split(".")[0]}_n{substring_length}_r{r}'
    #plotauc = plot_auc(sensitivities, specificities, p_title, path)

print(best_auc)
print(best_params)
# only plot best AUC
path = f'{results_folder}bestauc_{fn_test_anom.split(".")[0]}_n{best_params[0]}_r{best_params[1]}'
plotauc = plot_auc(best_sens, best_spec, best_title, path)
