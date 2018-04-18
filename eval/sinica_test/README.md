### Steps to generate the test file

1. `python grep_sinica.py ukey`.

   `ukey` is your session key on their website.

2. Use iconv to convert the BIG5-encoded text files in `raw/` into UTF-8.

   e.g. `iconv -f big5-2003 -t utf-8 -c 出.txt > 出.tc`.

3. `python remove_redundancy.py`.

4. `python unsegment.py` to copy sentences into `sinica_test/`, discarding word segmentation.

5. Use OpenCC to convert `sinica_test/*.tc` into `sinica_test/*.sc`.

   e.g. `opencc -i 出.tc -o 出.sc -c tw2s`.

6. Modify `sinica_test/*.sc` to correct any conversion error.

7. `cd ..; python extract_test.py` to generate the csv file.
