from ppadb.client import Client as AdbClient
import os

adb = AdbClient(host="127.0.0.1", port=5037)

if not adb.devices():
    port = input('Port> ')

    adb.remote_connect('192.168.0.13', int(port))

    for device in adb.devices():
        try:
            os.system('flet build apk')
            device.install('./build/apk/app-release.apk')
            device.shell(f"am startservice -n com.android.shell/.ShellCmdService -e cmd 'notify --title \"{'build end'}\" --text \"{'Build was deployed'}\"'")

        except RuntimeError:
            pass

    exit()

for device in adb.devices():
    try:
        device.get_device_path()
    except RuntimeError:
        port = int(input('Port> '))
        adb.remote_connect('192.168.0.13', port)

    for device in adb.devices():
        try:
            os.system('flet build apk')
            device.get_device_path()
            device.install('./build/apk/app-release.apk')
            device.shell(
                f"am startservice -n com.android.shell/.ShellCmdService -e cmd 'notify --title \"{'build end'}\" --text \"{'Build was deployed'}\"'")

        except RuntimeError:
            pass