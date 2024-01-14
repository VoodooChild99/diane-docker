import sys

sys.path.append("/root/diane")

from diane.src.ui.core import ADBDriver

if __name__ == '__main__':
    adbd = ADBDriver(device_id=sys.argv[1], f_path=None)

    adbd.adb_su_cmd('kill -9 `pgrep -f frida-server`')
    adbd.adb_su_cmd('kill -9 `pgrep -f frd1102`')
    adbd.adb_su_cmd('rm /data/local/tmp/frida-server-11.0.2-android-arm64')
    adbd.adb_su_cmd('rm /data/local/tmp/frd1102')
    adbd.adb_cmd(['forward', '--remove-all'])
    adbd.adb_cmd(['forward', 'tcp:27047', 'tcp:9999'])
    adbd.adb_cmd(['push', '/root/frida-server-11.0.2-android-arm64', '/data/local/tmp'])
    adbd.adb_su_cmd('chmod +x /data/local/tmp/frida-server-11.0.2-android-arm64')
    adbd.adb_su_cmd('cp /data/local/tmp/frida-server-11.0.2-android-arm64 /data/local/tmp/frd1102')
    adbd.adb_su_cmd('/data/local/tmp/frd1102 -l 0.0.0.0:9999')