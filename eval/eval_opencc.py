#!/usr/bin/env python3
import pandas as pd
import os, sys, subprocess
from collections import Counter, defaultdict

try:
  dataset = sys.argv[1]
  if dataset.endswith('.csv'): dataset = dataset[:-4]
except:
  print('Usage: ./eval_opencc.py csv_file')
  sys.exit()

# read dictionary
trad2simp, var2norm = dict(), dict()
with open('chars_of_interest.txt', 'r') as f:
  for line in f:
    simp, trad = line.strip().split('\t')
    variant_mode, prev_trad = False, None
    for char in trad:
      if char == '(': variant_mode = True
      elif char == ')': variant_mode = False
      elif variant_mode: var2norm[char] = prev_trad
      else:
        trad2simp[char] = simp
        prev_trad = char
def normalize(c): return var2norm.get(c, c)
simp2trad = defaultdict(set)
for k, v in trad2simp.items(): simp2trad[v].add(k)

# run opencc
csv = pd.read_csv(dataset + '.csv')
orig = csv['orig']
with open('test.sc', 'w') as f:
  f.writelines(s + "\n" for s in orig)
subprocess.run('opencc -i test.sc -o test.tc -c s2tw', shell=True)
with open('test.tc', 'r') as f:
  pred = [s.rstrip('\n') for s in f.readlines()]

# collect errors
trad_error_count, trad_count = Counter(), Counter()
error_list = pd.DataFrame(columns=['char_res', 'orig_char', 'gold_char', 'char_index',
                                   'res', 'orig', 'gold', 'orig_line_num'])
for i, row in csv.iterrows():
  pos = row['char_index']
  gold_char = normalize(row['gold_char'])
  pred_char = normalize(pred[i][pos])
  orig_char = row['orig_char']
  trad_count[gold_char] += 1
  if gold_char != pred_char:
    error_list.loc[len(error_list)] = [pred_char, orig_char, gold_char, pos,
                                       pred[i], row['orig'], row['gold'], row['orig_line_num']]
    trad_error_count[gold_char] += 1
    if pred_char not in simp2trad[orig_char]:
      print("%s is mapped to an out-of-table char %s" % (orig_char, pred_char))
error_list.to_csv(dataset + '_errors.csv', index=False)

# make report
report = pd.DataFrame(columns=['char_gold', 'char_orig', 'error_num', 'total', 'error_rate'])
total_error, total_count = 0, 0
for trad, simp in trad2simp.items():
  error, count = trad_error_count[trad], trad_count[trad]
  report.loc[len(report)] = [trad, simp, error, count, "%.3f" % (error/count)]
  total_error += error
  total_count += count
report.sort_values(['char_orig', 'error_rate', 'char_gold'], inplace=True)
report.loc[len(report)] = ['Avg', 'Avg', total_error, total_count, "%.3f" % (total_error/total_count)]
report.to_csv(dataset + '_report.csv', index=False)

# clean up
os.remove('test.sc')
os.remove('test.tc')