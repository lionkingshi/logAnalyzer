# configuration used in full api test
full_api_apk_folder_name = "fullapiapk"
full_api_test_apk_file_name = "DolbyEffectApiTest.apk"
full_api_target_apk_file_name = "DolbyEffectApi.apk"
file_name_contain_test_method = "AllTests.txt"
full_api_result_name = "DAX31EffectApiTest_Result.xml"
full_api_xml_result_location_on_device = \
    "/sdcard/Android/data/com.dolby.qa.dax31effecttest/files/DAX31EffectApiTest_Result.xml"

# apk info
full_api_run_all_test_case = "com.dolby.qa.dax31effecttest.AllTest"
full_api_target_package_name = "com.dolby.qa.dax31effecttest"
full_api_test_package_name = full_api_target_package_name + ".test"
full_api_target_apk_location_on_device = "/data/local/tmp/" + full_api_target_package_name
full_api_test_apk_location_on_device = "/data/local/tmp/" + full_api_test_package_name
full_api_activity_name = "com.dolby.qa.dolbyeffecttest.DAXApiActivity"
permission_list = [
    "android.permission.WRITE_EXTERNAL_STORAGE",
    "com.dolby.dax.api.permission.Write",
    "com.dolby.dax.api.permission.Read",
    "android.permission.MODIFY_AUDIO_SETTINGS",
    "android.permission.RECORD_AUDIO",
    "com.dolby.permission.DOLBY_UPDATE_BROADCAST"]

# re-run configuration
full_api_re_run_cnt = 3
