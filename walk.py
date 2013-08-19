import os
for root, dirs, files in os.walk("/usr/local"):
    print(root)
    print(dirs)
    print(files)