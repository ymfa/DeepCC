import sys, re
import os.path
import urllib.parse, urllib.request

row_matcher = re.compile(rb"<tr><th nowrap>\d+\. </th><td nowrap>(.+?)</td><td class='mod' nowrap>(.+?)</td><td style='text-align:left'>(.+?)</td></tr>")

def urlencode(char):
  return urllib.parse.urlencode({'z': char}, encoding='big5hkscs')[2:]

def grep(ukey, char):
  url = 'http://lingcorpus.iis.sinica.edu.tw/cgi-bin/kiwi/mkiwi/kiwi.sh?ukey=%s&qtype=2&ssl=&lineLen=119&A=on&kw0=*%s*&kwd0=0&kwa0=&kwb0=&kw1=&kwd1=0&kwa1=&kwb1=&kw2=&kwd2=0&kwa2=&kwb2=' % (ukey, urlencode(char))
  with urllib.request.urlopen(url) as response:
    html = response.read()
  rows = row_matcher.findall(html)
  print(char, len(rows))
  with open('sinica_raw/%s.txt' % char, 'wb') as f:
    for row in rows:
      row = tuple(s.replace(b'\t',b'') for s in row)
      f.write(b"%s\t%s\t%s\n" % row)

if __name__ == "__main__":
  ukey = sys.argv[1]
  chars = []
  with open('../chars_of_interest.txt', 'r') as f:
    for line in f:
      _, trad = line.strip().split('\t')
      chars.extend(trad.replace('(','').replace(')', ''))
  
  for char in chars:
    if not os.path.isfile('raw/%s.txt' % char):
      try:
        grep(ukey, char)
      except Exception as e:
        print("Failed to grep %s: %s" % (char, e))