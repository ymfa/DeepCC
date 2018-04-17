import glob

if __name__ == "__main__":
  for filename in glob.glob('sinica_raw/*.tc'):
    test_cases = []
    char = filename[11]
    with open(filename, 'r') as f:
      for i, line in enumerate(f):
        try:
          left, word, right = line.strip().split('\t')
        except:
          print(line, filename, i)
          continue
        sentence = left + word + right
        for i, c in enumerate(word):
          if c == char:
            test_cases.append("%d\t%s\n" % (len(left)+i, sentence))
    with open('sinica_test/' + char + '.tc', 'w') as f:
      f.writelines(test_cases)