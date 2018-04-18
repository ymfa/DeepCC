import glob

if __name__ == "__main__":
  all_difficult_cases = []
  for filename in glob.glob('raw/*.tc'):
    test_cases = []
    char = filename[11]
    difficult_cases = []
    with open(filename, 'r') as f:
      for line_idx, line in enumerate(f):
        try:
          left, word, right = line.strip().split('\t')
        except:
          print(line, filename, line_idx)
          continue
        sentence = left + word + right
        if len(word) == 1:
          difficult_cases.append(len(test_cases))
        test_word_found = False
        for i, c in enumerate(word):
          if c == char:
            test_cases.append("%d\t%s\n" % (len(left)+i, sentence))
            test_word_found = True
        assert test_word_found
    if difficult_cases: all_difficult_cases.append((char, difficult_cases))
    with open(char + '.tc', 'w') as f:
      f.writelines(test_cases)
  with open('cases_of_interest.txt', 'w') as f:
    for char, indices in sorted(all_difficult_cases):
      f.write('%s\t%s\n' % (char, " ".join(str(i) for i in indices)))
