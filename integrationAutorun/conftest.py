import time

import pytest

from tools.common import *


@pytest.fixture(scope="session", autouse=True)
def move_test_content(request):
    # first move all test content to device
    print '\n move all test content to device directory: /sdcard/feature/'
    execute('adb shell mkdir {0}'.format(play_content_device_location))
    # execute('adb push {0} {1}'.format(play_content_local_location, play_content_device_location))
    # time.sleep(SLEEP_TIME_FOR_PUSH_MEDIA_TO_DUT)

    # next install test application to device
    # first time installation require human to permit the permission
    print '\n install test apk to device under test'
    # execute('adb install -r {0}'.format(test_apk_location))
    time.sleep(SLEEP_TIME_FOR_INSTALLING_APK)
    # execute(adb_clear_log)

    def global_resource_release():
        # execute(adb_clear_log)
        print '\n please release global resource'

    request.addfinalizer(global_resource_release)


@pytest.fixture(scope="function", autouse=True)
def function_set_up(request):
    print '\n each test case set up now'
    execute("adb shell am start -n {0}/{1}".format(test_package_name, test_package_main_activity_name))
    execute(adb_clear_log)
    # must sleep some time because only activity is active , it will begin to receive broadcast intent
    # or activity would crash because of receiving intent on dead main activity thread
    time.sleep(SLEEP_TIME_FOR_ACTIVITY_START)

    def function_tear_down():
        print 'each test case tear down'
        execute(adb_broadcast_intent + intent_change_dap_high_level_feature.format(
            dap_feature_type_reset_universal_para, dap_feature_value_reset_universal_para))
        execute(adb_broadcast_intent + intent_change_dap_high_level_feature.format(
            dap_feature_type_reset_profile, dap_feature_value_reset_profile_all))
        time.sleep(3)
        execute(adb_clear_log)
        execute("adb shell am force-stop {0}".format(test_package_name))
        # time.sleep(3)

    request.addfinalizer(function_tear_down)
