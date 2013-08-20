import re
aa = re.sub("(([0-9])\\.)", "(\\1)", "3. apple 5. 4apple")
print(aa)