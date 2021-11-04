import sys
import re

input_file = sys.argv[1]

#Everything above this threshold does not get filled in
max_indel_size = 10

with open(input_file, 'r') as sam:
    for line in sam:
        splitted_line = line.split('\t')
        if splitted_line[1] == '16' or splitted_line[1] == '0':
            cigar_with_none = re.split('(\d+)', splitted_line[5])
            cigar = filter(None, cigar_with_none)
            cigar_tuples = list(zip(*[iter(cigar)]*2))
            new_cigar = []
            for tuple in cigar_tuples:
                if tuple[1] == 'D' and int(tuple[0]) < max_indel_size:
                    new_cigar.append(str(tuple[0]+'M'))
                elif tuple[1] == 'I' and int(tuple[0]) < max_indel_size:
                    pass
                else:
                    new_cigar.append(''.join(tuple))

            #This prints the cigar but replaces sequence and quality with a '.'
            #All tags are ignored as they might be incoherent
            print(splitted_line[0]+'\t'+splitted_line[1]+'\t'+splitted_line[2]+'\t'+splitted_line[3]+
                  '\t'+splitted_line[4]+'\t'+''.join(new_cigar)+'\t'+splitted_line[6]+'\t'+splitted_line[7]+
                  '\t'+splitted_line[8]+'\t*\t*')

