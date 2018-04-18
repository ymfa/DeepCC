import glob, editdistance
from collections import defaultdict

if __name__ == "__main__":
  for filename in glob.glob('raw/*.tc'):
    lines = []
    num_duplicates = 0
    with open(filename, 'r') as f:
      print(filename, end=' ')
      left_lookup = defaultdict(set)
      right_lookup = defaultdict(set)
      for line in f:
        is_duplicate = False
        prefix, suffix = line[:5], line[-6:-1]
        candidates =  left_lookup[prefix] | right_lookup[suffix]
        for cand in candidates:
          if editdistance.eval(line, cand) <= 1:
            num_duplicates += 1
            is_duplicate = True
            break
        left_lookup[prefix].add(line)
        right_lookup[suffix].add(line)
        if not is_duplicate: lines.append(line)
      print(num_duplicates)
    with open(filename, 'w') as f:
      f.writelines(lines)