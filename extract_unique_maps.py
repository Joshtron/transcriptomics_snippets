import sys
import re

input_file = sys.argv[1]

max_score_line = []
discard = False

with open(input_file, 'r') as sam:
    for line in sam:
        if line.startswith('@'):
            print(line.strip())
        else:
            if len(max_score_line) == 0:
                max_score_line.append(line)
            else:
                if max_score_line[0].split('\t')[0] != line.split('\t')[0]:
                    if not discard:
                        print(max_score_line[0].strip())
                    discard = False
                    max_score_line[0] = line
                else:
                    score_1 = re.search(r'AS:i:(\d+)', max_score_line[0])
                    score_2 = re.search(r'AS:i:(\d+)', line)
                    if int(score_1.group(1)) < int(score_2.group(1)):
                        max_score_line[0] = line
                        discard = False
                    elif int(score_1.group(1)) == int(score_2.group(1)):
                        discard = True
if not discard:
    print(max_score_line[0].strip())