import numpy as np
from sklearn import metrics
import matplotlib.pyplot as plt
import subprocess

def load_files(fname_concat, fname_anom, fname_norm):
    with open(f'{fname_concat}.txt') as f:
        conc_outp = list(map(float, f.read().splitlines()))

    with open(f'{fname_anom}.txt') as g:
        a_outp = list(map(float, g.read().splitlines()))

    with open(f'{fname_norm}.txt') as h:
        n_outp = list(map(float, h.read().splitlines()))

    conc_outp = sorted(np.unique(conc_outp))

    return conc_outp, a_outp, n_outp

def calc_sp_se(conc_outp, a_outp, n_outp):
    sensitivities = []
    specificities = []
    for cutoff in conc_outp:
        # no. anomalies higher than cutoff
        sens = len([anom for anom in a_outp if anom > cutoff]) / len(a_outp)
        # no. normals lower than cutoff
        spec = len([norm for norm in n_outp if norm < cutoff]) / len(n_outp)

        sensitivities.append(sens)
        specificities.append(spec)
    return sensitivities, specificities

def plot_auc(sensitivities, specificities, p_title):
    plt.plot(specificities, sensitivities, 'r--')
    plt.plot([1,0],[0,1],'b--')
    plt.xlabel('Specificity')
    plt.ylabel('Sensitivity')
    plt.title(f'{p_title} - AUC: {metrics.auc([1 - sp for sp in specificities],sensitivities)}')
    plt.axis([1, 0, 0, 1])
    plt.show()
    return

def question_parameters(q_num):
    if q_num == 1:
        # n=1 r=4 anomaly=Tagalog normal=English
        fname_concat, fname_anom, fname_norm = ['output_te', 'output_t', 'output_e']
        p_title = 'AUC (n=10 r=4)'
    elif q_num == 2.1:
        # Change r to 1
        fname_concat, fname_anom, fname_norm = ['r1_output_te', 'r1_output_t', 'r1_output_e']
        p_title = 'AUC (n=10 r=1)'
    elif q_num == 2.2:
        # Change r to 9
        fname_concat, fname_anom, fname_norm = ['r9_output_te', 'r9_output_t', 'r9_output_e']
        p_title = 'AUC (n=10 r=9)'
    elif q_num == 3.1:
        # Change anomaly language to Hiligaynon
        fname_concat, fname_anom, fname_norm = ['output_he', 'output_h', 'output_e']
        p_title = 'AUC (n=10 r=4 Hiligaynon)'
    elif q_num == 3.2:
        # Change anomaly language to Middle-English
        fname_concat, fname_anom, fname_norm = ['output_me', 'output_m', 'output_e']
        p_title = 'AUC (n=10 r=4 Middle-English)'
    elif q_num == 3.3:
        # Change anomaly language to Plautdietsch
        fname_concat, fname_anom, fname_norm = ['output_pe', 'output_p', 'output_e']
        p_title = 'AUC (n=10 r=4 Plautdietsch)'
    elif q_num == 3.4:
        # Change anomaly language to Xhosa
        fname_concat, fname_anom, fname_norm = ['output_xe', 'output_x', 'output_e']
        p_title = 'AUC (n=10 r=4 Xhosa)'
    else:
        pass
    
    return fname_concat, fname_anom, fname_norm, p_title

if __name__ == '__main__':
    fname_concat, fname_anom, fname_norm, p_title = question_parameters(3.4)
    conc_outp, t_outp, e_outp = load_files(fname_concat, fname_anom, fname_norm)
    sensitivities, specificities = calc_sp_se(conc_outp, t_outp, e_outp)
    plot_auc(sensitivities, specificities, p_title)
