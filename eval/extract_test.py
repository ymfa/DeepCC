import os, glob, csv, sys

trad2simp = dict()
dir_path = os.path.dirname(os.path.realpath(__file__))
with open(os.path.join(dir_path, 'chars_of_interest.txt'), 'r') as f:
  for line in f:
    simp, trad = line.strip().split('\t')
    trad = trad.replace('(','').replace(')','')
    for char in trad:
      trad2simp[char] = simp

if __name__ == "__main__":
  try:
    dataset_name = sys.argv[1]
  except:
    print("Usage: python extract_test.py dataset_name")
    sys.exit()
  test_cases = []
  for filename in glob.glob(os.path.join(dataset_name, '*.tc')):
    char = filename[len(dataset_name)+1]
    char_simp = trad2simp[char]
    pos, trad, simp = [], [], []
    removed_ids = set()
    with open(filename, 'r') as f:
      for line in f:
        idx, sentence = line.strip().split('\t')
        pos.append(int(idx))
        trad.append(sentence)
    with open(os.path.join(dataset_name, '%s.sc' % char), 'r') as f:
      for i, line in enumerate(f):
        idx, sentence = line.strip().split('\t')
        assert int(idx) == pos[i]
        assert len(sentence) == len(trad[i])
        simp.append(sentence)
        if sentence[pos[i]] != char_simp:
          removed_ids.add(i)
    if removed_ids:
      print(char, '%d sentences excluded' % len(removed_ids))
    for i, (p, t, s) in enumerate(zip(pos, trad, simp)):
      if i in removed_ids: continue
      case = {'orig_char': char_simp, 'gold_char': char, 'char_index': p,
              'orig': s, 'gold': t, 'orig_line_num': i}
      test_cases.append(case)
  with open('%s.csv' % dataset_name, 'w', newline='') as csvfile:
    fieldnames = ['orig_char', 'gold_char', 'char_index', 'orig', 'gold', 'orig_line_num']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()
    for row in test_cases: writer.writerow(row)