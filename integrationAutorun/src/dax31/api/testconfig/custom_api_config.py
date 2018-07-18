# configuration used in custom api test
custom_api_apk_folder_name = "customapiapk"
custom_api_test_apk_file_name = "DolbyEffectApiTest.apk"
custom_api_target_apk_file_name = "DolbyEffectApi.apk"
file_name_contain_test_method = "AllTests.txt"
custom_api_result_name = "DAXApiTest_Result.xml"
custom_api_xml_result_location_on_device = "/sdcard/Android/data/com.dolby.qa.dax31api/files/DAXApiTest_Result.xml"

# apk info
custom_api_target_package_name = "com.dolby.qa.dax31api"
custom_api_test_package_name = custom_api_target_package_name + ".test"
custom_api_target_apk_location_on_device = "/data/local/tmp/" + custom_api_target_package_name
custom_api_test_apk_location_on_device = "/data/local/tmp/" + custom_api_test_package_name
custom_api_activity_name = "com.dolby.qa.dolbyeffecttest.DAXApiActivity"
permission_list = [
    "android.permission.WRITE_EXTERNAL_STORAGE",
    "com.dolby.dax.api.permission.Write",
    "com.dolby.dax.api.permission.Read",
    "android.permission.MODIFY_AUDIO_SETTINGS",
    "android.permission.RECORD_AUDIO",
    "com.dolby.permission.DOLBY_UPDATE_BROADCAST"]

# re-run configuration
custom_api_re_run_cnt = 3