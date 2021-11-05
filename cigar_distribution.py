import sys
import os.path
import re
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np

def plot_indels(input_file):
    del_counts = []
    ins_counts = []
    m_counts = []
    n_counts = []

    label_counter = 0

    ins_labels = []
    del_labels = []
    m_labels = []
    n_labels= []

    with open(input_file[:-4]+'.tsv', 'r') as indel_list:
        next(indel_list)
        for line in indel_list:
            splitted_line = line.split('\t')
            if not int(splitted_line[1]) == 0:
                ins_counts.append(int(splitted_line[1]))
                ins_labels.append(label_counter)
            if not int(splitted_line[2]) == 0:
                del_counts.append(int(splitted_line[2]))
                del_labels.append(label_counter)
            if not int(splitted_line[3]) == 0:
                m_counts.append(int(splitted_line[3]))
                m_labels.append(label_counter)
            if not int(splitted_line[4]) == 0:
                n_counts.append(int(splitted_line[4]))
                n_labels.append(label_counter)
            label_counter += 1

    labels = list(range(1,9999))

    width = 0.35

    #plt.bar(del_labels - width / 2, del_counts, align='center', color='b', alpha=0.5, label='deletions', width=width)
    #plt.bar(ins_labels + width / 2, ins_counts, align='center', color='r', alpha=0.5, label='insertions', width=width)
    plt.plot(del_labels, del_counts, marker='1', color='b', alpha=0.5, label='deletions')
    plt.plot(ins_labels, ins_counts, marker='2', color='r', alpha=0.5, label='insertions')
    plt.plot(m_labels, m_counts, marker='2', color='sienna', alpha=0.5, label='matches')
    plt.plot(n_labels, n_counts, marker='2', color='silver', alpha=0.5, label="N's")
    plt.gca().set_xticks(labels)
    plt.yscale('log')
    plt.xscale('log')
    plt.legend()
    plt.xlabel('DEL/INS/M/N size')
    plt.title('Distribution of deletions and insertions for ' + input_file + '\n', fontsize=12)
    plt.show()
    plt.savefig(input_file[:-4]+'.png', dpi=300, bbox_inches='tight')

def make_tsv(input_file):

    del_list = [0] * 1000000
    ins_list = [0] * 1000000
    n_list = [0] * 1000000
    m_list = [0] * 1000000

    with open(input_file, 'r') as sam:
        for line in sam:
            if not line.startswith('@'):
                splitted_line = line.split('\t')
                cigar = re.split('(\d+)', splitted_line[5])
                for i in range(0,len(cigar)):
                    if cigar[i] == 'D':
                        del_list[int(cigar[i-1])] += 1
                    if cigar[i] == 'I':
                        ins_list[int(cigar[i-1])] += 1
                    if cigar[i] == 'N':
                        n_list[int(cigar[i-1])] += 1
                    if cigar[i] == 'M':
                        m_list[int(cigar[i-1])] += 1



    tsv_file = open(input_file[:-4]+".tsv", "w")
    tsv_file.write('length\tINS\tDEL\tM\tN\n')
    for i in range(1, 9999):
        tsv_file.write(str(i)+'\t'+str(ins_list[i])+'\t'+str(del_list[i])+'\t'+str(m_list[i])+'\t'+str(n_list[i])+'\n')

input_file = sys.argv[1]

if os.path.isfile(input_file[:-4]+'.tsv')  == True:

    print('Yo, that is easy')
    plot_indels(input_file[:-4]+'.tsv')

else:

    print('Oof, why do we have to do it the hard way?')
    make_tsv(input_file)
    plot_indels(input_file[:-4]+'.tsv')
