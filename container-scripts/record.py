import json
import os
import sys

sys.path.append("/root/diane")

from diane.src.ui.core import ADBDriver

if __name__ == '__main__':
    try:
        proj_path = sys.argv[1]
    except:
        print "Usage: {} [Proj]".format(sys.argv[0])
        sys.exit(1)

    config_path = os.path.join(proj_path, 'config.json')
    config = json.load(open(config_path))
    adbd = ADBDriver(device_id=config['device_id'], f_path=None)

    reran_log_path = os.path.join(proj_path, 'reran.log')
    adbd.record_ui(reran_log_path)
    print "Ran stored in {}, updating config...".format(reran_log_path)
    config['reran_record_path'] = os.path.abspath(reran_log_path)
    with open(config_path, 'w') as f:
        json.dump(config, f)

    print "Done."