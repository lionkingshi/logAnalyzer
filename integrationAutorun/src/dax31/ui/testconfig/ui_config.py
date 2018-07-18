# configuration used in custom api test
ui_apk_folder_name = "uiapk"
ui_test_apk_file_name = "DolbyUITestCase.apk"
ui_target_apk_file_name = "DolbyInternalUI.apk"
file_name_contain_test_method = "AllTests.txt"
ui_result_name = "internalDolbyUiTest_Result.xml"
ui_xml_result_location_on_device = \
    "/sdcard/Android/data/com.dolby.daxappui.internal/files/{0}".format(ui_result_name)

# apk info
# ui_run_all_test_case = "com.dolby.qa.daxuitest.AllDaxTest"
ui_run_all_test_case = "com.dolby.qa.daxuitest.DaxConsumerUITest"
ui_target_package_name = "com.dolby.daxappui.internal"
ui_stop_package_name = "com.dolby.daxappui"
ui_start_activity_package_name = ui_stop_package_name
ui_start_activity_name = ".MainActivity"
ui_test_package_name = ui_target_package_name + ".test"
ui_run_listener_name = "com.dolby.qa.utils.customRunListener.XmlRunListener"
ui_target_apk_location_on_device = "/data/local/tmp/" + ui_target_package_name
ui_test_apk_location_on_device = "/data/local/tmp/" + ui_test_package_name
ui_activity_name = "com.dolby.daxappui.DAXApiActivity"
permission_list = [
    "android.permission.BLUETOOTH",
    "android.permission.MODIFY_AUDIO_SETTINGS",
    "android.permission.WRITE_EXTERNAL_STORAGE",
    "android.permission.READ_EXTERNAL_STORAGE"]

# re-run configuration
ui_re_run_cnt = 3
