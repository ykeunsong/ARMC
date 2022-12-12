#!/usr/bin/env python

import sys
import os
from apk_parse import apk
from collections import OrderedDict
from permissions import full_permissions, suspicious_permissions
from get_permission_info import get_permission_info
from get_api_info import get_api_info

# paths ['0-normal', '1-malware', 'test']
apk_path = '../../data/train_data/0-normal'
dex_path = '../../data/train_data/dex_0-normal'
out_path = '../../data/train_data/out/0-normal'

# constants
DELIMITER = ','

out_with_full_permissions = os.path.join(out_path, 'with_full_perm.csv')
out_with_suspicious_permissions = os.path.join(out_path, 'with_suspicious_perm.csv')

ff = open(out_with_full_permissions, 'w')
sf = open(out_with_suspicious_permissions, 'w')

for filename in os.listdir(apk_path):
    apk_abs_path = os.path.join(apk_path, filename)
    dex_abs_path = os.path.join(dex_path, filename+'.dex')

    if not os.path.exists(dex_abs_path):
        continue

    (full_perm_list, suspicious_perm_list) = get_permission_info(apk_abs_path)
    if (full_perm_list is None or suspicious_perm_list is None):
        continue

    api_list = get_api_info(dex_abs_path)

    full_hdr = 'filename' + DELIMITER
    for i in len(api_list):
        full_hdr = full_hdr + 'api' + str(i+1) + DELIMITER
    for j in len(full_perm_list):
        full_hdr = full_hdr + 'perm' + str(j+1) + DELIMITER
    full_hdr = full_hdr + 'label' + '\n'

    suspicious_hdr = 'filename' + DELIMITER
    for i in len(api_list):
        suspicious_hdr = suspicious_hdr + 'api' + str(i+1) + DELIMITER
    for j in len(suspicious_perm_list):
        suspicious_hdr = suspicious_hdr + 'perm' + str(j+1) + DELIMITER
    suspicious_hdr = suspicious_hdr + 'label' + '\n'

    full = filename + DELIMITER + str(full_perm_list)[1:-1] + DELIMITER + str(api_list)[1:-1] + '\n'
    suspicious = filename + DELIMITER + str(suspicious_perm_list)[1:-1] + DELIMITER + str(api_list)[1:-1] + '\n'

    ff.write(full_hdr)
    ff.write(full)
    sf.write(suspicious_hdr)
    sf.write(suspicious)

ff.close()
sf.close()
