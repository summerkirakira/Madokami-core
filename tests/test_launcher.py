from madokami.drivers.madokami import MadokamiApp
import threading
import time
import pytest



def auto_restart(launcher: MadokamiApp):
    time.sleep(5)
    launcher.restart()


@pytest.mark.skip(reason="This test is not working properly")
def test_launcher(database):
    launcher = MadokamiApp()
    launcher_thread = threading.Thread(target=launcher.start)
    restart_thread = threading.Thread(target=auto_restart, args=(launcher,))
    launcher_thread.start()
    restart_thread.start()

    launcher_thread.join()
    restart_thread.join()

    assert True