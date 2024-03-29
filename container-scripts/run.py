import json
import os
import stat
import sys
import configparser

INI_FILE_NAME = "config.ini"

if __name__ == '__main__':
    try:
        proj_path = os.path.abspath(sys.argv[1])
    except:
        print "Usage: {} [Proj]".format(sys.argv[0])
        sys.exit(1)

    ini_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), os.pardir)
    ini_path = os.path.join(os.path.abspath(ini_path), INI_FILE_NAME)
    if not os.path.exists(ini_path):
        ini_config = configparser.ConfigParser()
        ini_config['global'] = {
            "android_ip": "",
            "ip_hot_spot": "",
            "pass_ap": "",
            "user_ap": "",
            "if_ap": "",
            "ip_hot_spot_cloud": "",
            "pass_ap_cloud": "",
            "user_ap_cloud": "",
            "if_ap_cloud": "",
            "device_id": "",
        }
        with open(ini_path, 'w') as f:
            ini_config.write(f)
        os.chmod(ini_path, stat.S_IROTH | stat.S_IWOTH)
        print "Prepare config.ini before running again"
        sys.exit(1)
    
    ini_config = configparser.ConfigParser()
    ini_config.read(ini_path)
    ini_config = ini_config["global"]

    init_lists = [
        'android_ip',
        'pass_ap',
        'user_ap',
        'ip_hot_spot',
        'if_ap',
        'device_id',
    ]
    for item in init_lists:
        if (item not in ini_config) or not ini_config[item]:
            print "Fillin config.ini first"
            sys.exit(1)
    
    config_path = os.path.join(proj_path, 'config.json')
    if not os.path.exists(config_path):
        # create a vanilla template
        config = {
            "skip_classes": [],
            "bad_functions": [],
            "proc_name": "",
            "reran_record_path": "",
            "skip_methods": [],
            "android_sdk_platforms": "/root/android_sdk/platforms",
            "android_ip": "{}".format(ini_config['android_ip']),
            "device_ip": "",
            "pass_ap": "{}".format(ini_config['pass_ap']),
            "results_path": "{}".format(proj_path),
            "frida_hooker_pickle": "",
            "fuzz_pcap_path": "{}/pcap_dir".format(proj_path),
            "user_ap": "{}".format(ini_config['user_ap']),
            "ip_hot_spot": "{}".format(ini_config['ip_hot_spot']),
            "leaf_pickle": "",
            "apk_path": "{}/app.apk".format(proj_path),
            "if_ap": "{}".format(ini_config['if_ap']),
            "device_id": "{}".format(ini_config['device_id']),
            "phys_ip": "",
            "ip_hot_spot_cloud": "{}".format(ini_config['ip_hot_spot_cloud']),
            "pass_ap_cloud": "{}".format(ini_config['pass_ap_cloud']),
            "user_ap_cloud": "{}".format(ini_config['user_ap_cloud']),
            "if_ap_cloud": "{}".format(ini_config['if_ap_cloud']),
            "blt": False
        }
        with open(config_path, 'w') as f:
            json.dump(config, f)
        os.chmod(config_path, stat.S_IROTH | stat.S_IWOTH)
        print "Prepare {} before running again".format(config_path)
        sys.exit(1)

    config = json.load(open(config_path))
    check_lists = [
        'proc_name',
        'reran_record_path',
        'android_sdk_platforms',
        'android_ip',
        'device_ip',
        'pass_ap',
        'results_path',
        'fuzz_pcap_path',
        'user_ap',
        'ip_hot_spot',
        'apk_path',
        'if_ap',
        'device_id',
    ]
    check_lists_cloud = [
        "phys_ip",
        "ip_hot_spot_cloud",
        "pass_ap_cloud",
        "user_ap_cloud",
        "if_ap_cloud",
    ]
    
    for item in check_lists:
        if item not in config or not config[item]:
            if item == 'reran_record_path':
                print "run record.py first"
                sys.exit(1)
            print "please fill-in {}".format(item)
            sys.exit(1)
    
    if 'phys_ip' in config:
        if not config['phys_ip']:
            print "please fill-in phys_ip"
            sys.exit(1)
        for item in check_lists_cloud:
            if item not in config or not config[item]:
                print "please fill-in {}".format(item)
                sys.exit(1)
    
    config_changed = False
    
    for item in init_lists:
        if config[item] != ini_config[item]:
            config[item] = ini_config[item]
            config_changed = True

    if 'frida_hooker_pickle' not in config or not config['frida_hooker_pickle']:
        hooker_file = os.path.join(
            os.path.dirname(config['apk_path']),
            'frida_results.pickle_{}'.format(config['proc_name']))
        if os.path.exists(hooker_file):
            os.remove(hooker_file)
    
    if 'leaf_pickle' not in config or not config['leaf_pickle']:
        leaf_file = os.path.join(
            os.path.dirname(config['apk_path']),
            'leaves_{}'.format(config['proc_name']))
        if os.path.exists(leaf_file):
            os.remove(leaf_file)
    
    if config_changed:
        print "config updated, dump to file"
        with open(config_path, 'w') as f:
            json.dump(config, f)
    
    config_changed = False
    
    # run the command
    os.system('python /root/diane/diane/run.py {}'.format(config_path))
    
    if 'frida_hooker_pickle' not in config or not config['frida_hooker_pickle']:
        # try copy the results
        hooker_file = os.path.join(
            os.path.dirname(config['apk_path']),
            'frida_results.pickle_{}'.format(config['proc_name']))
        if os.path.exists(hooker_file):
            print "Update frida_hooker_pickle to {}".format(hooker_file)
            config['frida_hooker_pickle'] = hooker_file
            config_changed = True

    if 'leaf_pickle' not in config or not config['leaf_pickle']:
        leaf_file = os.path.join(
            os.path.dirname(config['apk_path']),
            'leaves_{}'.format(config['proc_name']))
        if os.path.exists(leaf_file):
            print "Update leaf_file to {}".format(leaf_file)
            config['leaf_pickle'] = leaf_file
            config_changed = True
    
    if config_changed:
        print "config updated, dump to file"
        with open(config_path, 'w') as f:
            json.dump(config, f)
    


