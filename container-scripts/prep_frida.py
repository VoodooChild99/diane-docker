import sys
import argparse

sys.path.append("/root/diane")

from diane.src.ui.core import ADBDriver

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Prepare Frida in your phone')
    parser.add_argument('device_id')
    parser.add_argument('--arm32', action='store_true', default=False)
    parser.add_argument('--enable-bypass', action='store_true', default=False)
    args = parser.parse_args()

    adbd = ADBDriver(device_id=args.device_id, f_path=None)

    adbd.adb_su_cmd('kill -9 `pgrep -f frida-server`')
    adbd.adb_su_cmd('kill -9 `pgrep -f frd1102`')
    frida_prog = 'frida-server-11.0.2-android-arm' if args.arm32 else 'frida-server-11.0.2-android-arm64'
    adbd.adb_su_cmd('rm /data/local/tmp/{}'.format(frida_prog))
    adbd.adb_su_cmd('rm /data/local/tmp/frd1102')
    adbd.adb_cmd(['forward', '--remove-all'])
    if args.enable_bypass:
        adbd.adb_cmd(['forward', 'tcp:27047', 'tcp:9999'])
    adbd.adb_cmd(['push', '/root/{}'.format(frida_prog), '/data/local/tmp'])
    adbd.adb_su_cmd('chmod +x /data/local/tmp/{}'.format(frida_prog))
    adbd.adb_su_cmd('cp /data/local/tmp/{} /data/local/tmp/frd1102'.format(frida_prog))
    if args.enable_bypass:
        adbd.adb_su_cmd('/data/local/tmp/frd1102 -l 0.0.0.0:9999')
    else:
        adbd.adb_su_cmd('/data/local/tmp/frd1102')