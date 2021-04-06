import os
import os.path

for dirpath, dirnames, filenames in os.walk("/"):
    for filename in [f for f in filenames if f.endswith("apache2.conf" or "httdp.conf")]:
        print(os.path.join(dirpath, filename))
    for filename in [f for f in filenames if f.endswith("security.conf")]:
        print(os.path.join(dirpath, filename))


