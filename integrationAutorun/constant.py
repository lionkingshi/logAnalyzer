# define project id info
PROJECT_ID_DAX3 = 3
PROJECT_ID_DAX2 = 2
# define sleep time before record device log
SLEEP_TIME_BEFORE_RECORD_LOG = 5
SLEEP_TIME_FOR_PUSH_MEDIA_TO_DUT = 3
SLEEP_TIME_FOR_ACTIVITY_START = 1
SLEEP_TIME_FOR_INSTALLING_APK = 3
# define play content
play_content_local_location = './featureTestContent/*'
play_content_device_parent_location = '/sdcard/dolby'
play_content_folder_name = 'featureTestContent'
play_content_device_location = '/sdcard/dolby/featureTestContent'
# define test apk location and name
test_apk_parent_location = 'apkSrc'
test_apk_file_name = 'DAXLogAnalysis.apk'
# define test case log location on device under test
logFileLocation = "./log/"
logFileNameFormat = "{functionName}_{endpoint_type}_{log_type}.txt"
# define test apk package full name
test_package_name = 'com.dolby.qa.featuretest'
test_package_main_activity_name = '.MainActivity'

# define intent action for activity broadcast receiver
test_type = 'feature_test'

# define adb broadcast base/common command
adb_broadcast_intent = 'adb shell am broadcast -a {0} -p {1} '.format(test_type, test_package_name)
# define intent type
# intent type 1 : play content
intent_play_content = '--es step play_content --es content_location {0}/'.format(play_content_device_location)
# intent type 2 : change dap api
intent_change_dap = '--es step change_dap_feature '
# intent type 2.1 : change dap status on or off
intent_change_dap_status = intent_change_dap + '--ei dap_status '
# intent type 2.2 : change dap profile id : [0,5]
intent_change_dap_profile = intent_change_dap + '--ei dap_profile '
# intent type 2.3 : invoke setParameter(type,value)
intent_change_dap_low_level_feature = intent_change_dap + '--es dap_feature_type {0} --eia dap_feature_value {1}'
# intent type 2.4 : invoke high level api except graphic equalizer band gain
intent_change_dap_high_level_feature = intent_change_dap + '--ei {0} {1}'
# intent type 2.5 : invoke high level api : set graphic equalizer band gain
intent_change_dap_gebg_feature = intent_change_dap + '--eia {0} {1}'
# intent type 2.6 : change tuning device name for specified port :
intent_change_dap_tuning_device = intent_change_dap + '--ei dap_tuning_port {0} --ei dap_tuning_device {1}'

# define adb logcat command
adb_record_log = 'adb logcat -d >'
adb_record_log_append = 'adb logcat -d >>'
adb_clear_log = 'adb logcat -b all -c'
# adb_clear_log = 'adb device'

# define dolby content category
content_type_1_channel_non_dolby = '1.0'
content_type_2_channel_non_dolby = '2.0'
content_type_51_channel_non_dolby = '5.1'
content_type_71_channel_non_dolby = '7.1'
content_type_1_dd = '1_dd'
content_type_2_dd = '2_dd'
content_type_51_dd = '51_dd'
content_type_1_ddp = '1_ddp'
content_type_2_ddp = '2_ddp'
content_type_51_ddp = '51_ddp'
content_type_71_ddp = '71_ddp'
content_type_51_ddp_joc = '51_ddp_joc'
content_type_71_ddp_joc = '71_ddp_joc'

content_type_non_dolby = [content_type_1_channel_non_dolby, content_type_2_channel_non_dolby,
                          content_type_51_channel_non_dolby, content_type_71_channel_non_dolby]
content_type_dolby = [content_type_1_dd, content_type_2_dd, content_type_51_dd,
                      content_type_1_ddp, content_type_2_ddp, content_type_51_ddp,
                      content_type_71_ddp, content_type_51_ddp_joc, content_type_71_ddp_joc]
# 2 channel dolby content will be up mixed to 5.1 channel, instead of up mixing to 5.1.2 ,
content_type_2_channel_dolby = [content_type_2_dd, content_type_2_ddp]


# define change dap feature
# define dolby audio processing instance status
dap_status_on = str(1)
dap_status_off = str(0)
dap_status_unchanged = str(2)
# define profile name
dap_profile_dynamic = str(0)
dap_profile_movie = str(1)
dap_profile_music = str(2)
dap_profile_game = str(3)
dap_profile_voice = str(4)
dap_profile_custom = str(5)
dap_profile_unchanged = str(6)
# define dolby audio processing feature
# define reset profile intent
dap_feature_type_reset_profile = 'dap_reset_profile'
dap_feature_value_reset_profile_all = '10'
dap_feature_value_reset_profile_dynamic = dap_profile_dynamic
dap_feature_value_reset_profile_movie = dap_profile_movie
dap_feature_value_reset_profile_music = dap_profile_music
dap_feature_value_reset_profile_game = dap_profile_game
dap_feature_value_reset_profile_voice = dap_profile_voice
dap_feature_value_reset_profile_custom = dap_profile_custom
# define reset universal parameter
dap_feature_type_reset_universal_para = 'dap_reset_universal'
dap_feature_value_reset_universal_para = '1'
# define dialog enhancement intent
intent_change_dap_profile_de_feature = intent_change_dap_high_level_feature
dap_feature_type_de = 'dap_profile_de'
dap_feature_value_de_on = '1'
dap_feature_value_de_off = '0'
dap_feature_value_de_default = '2'
# define intelligent equalizer
dap_feature_type_ieq = 'dap_profile_ieq'
dap_feature_value_ieq_open = '1'
dap_feature_value_ieq_rich = '2'
dap_feature_value_ieq_focused = '3'
dap_feature_value_ieq_off = '0'
dap_feature_value_ieq_default = '4'
# define headphone sound virtualizer
dap_feature_type_hv = 'dap_profile_hv'
dap_feature_value_hv_on = '1'
dap_feature_value_hv_off = '0'
dap_feature_value_hv_default = '0'
# define virtual speaker virtualizer
dap_feature_type_vsv = 'dap_profile_vsv'
dap_feature_value_vsv_on = '1'
dap_feature_value_vsv_off = '0'
dap_feature_value_vsv_default = '2'
# define universal parameter - volume leveler - dvle
dap_feature_type_vl = 'dap_universal_vl'
dap_feature_value_vl_on = '1'
dap_feature_value_vl_off = '0'
dap_feature_value_vl_default = '2'
# define universal parameter - bass enable - beon
dap_feature_type_be = 'dap_universal_be'
dap_feature_value_be_on = '1'
dap_feature_value_be_off = '0'
dap_feature_value_be_default = '2'
# define universal parameter - graphic equalizer enable - geon
dap_feature_type_geq = 'dap_universal_geq'
dap_feature_value_geq_on = '1'
dap_feature_value_geq_off = '0'
dap_feature_value_geq_default = '2'
# define universal parameter - graphic equalizer band gain  - gebg
dap_feature_type_gebg = 'dap_universal_gebg'

# below is audio device info
AUDIO_DEVICE_OUT_MONO_SPEAKER = 'mono_speaker'
AUDIO_DEVICE_OUT_STEREO_SPEAKER = 'stereo_speaker'
AUDIO_DEVICE_OUT_WIRED_HEADPHONE = '35mm_headphone'
AUDIO_DEVICE_OUT_DGTL_DOCK_HEADSET = 'usb_headphone'
AUDIO_DEVICE_OUT_AUX_DIGITAL = 'hdmi'
AUDIO_DEVICE_OUT_BLUETOOTH_A2DP = 'blue_tooth'

# define constants for dax3 project
# ************************************************************************************
# ************************************************************************************
# *****************     test constant for dax3          ******************************
# ************************************************************************************
# ************************************************************************************
# define profile name
dap_profile_custom_dax3 = str(3)
dap_profile_unchanged_dax3 = str(6)
# define dolby audio effect feature
# define reset profile intent
dap_feature_value_reset_profile_custom_dax3 = dap_profile_custom_dax3
# define intelligent equalizer
dap_feature_value_ieq_detailed_dax3 = '1'
dap_feature_value_ieq_balanced_dax3 = '2'
dap_feature_value_ieq_warm_dax3 = '3'
# define dax3 profile based parameter - volume leveler - dvle
dap_feature_type_vl_dax3 = 'dap_profile_vl'
# define dax3 profile based parameter - bass enable - beon
dap_feature_type_be_dax3 = 'dap_profile_be'
# define dax3 profile based parameter - dialogue enhancer amount - dea
dap_feature_type_dea_dax3 = 'dap_profile_dea'
# define universal parameter - graphic equalizer band gain  - gebg
dap_feature_type_gebg_dax3 = 'dap_profile_gebg'
# define tuning port parameter
dap_feature_type_tuning_port_dax3 = 'dap_tuning_port'
# define detailed port information
dap_tuning_port_internal_speaker = str(0)
dap_tuning_port_hdmi = str(1)
dap_tuning_port_miracast = str(2)
dap_tuning_port_headphone_port = str(3)
dap_tuning_port_bluetooth = str(4)
dap_tuning_port_usb = str(5)
dap_tuning_port_other = str(6)
# define tuning device name parameter
dap_feature_type_tuning_device_name_dax3 = 'dap_tuning_device'
dap_tuning_device_name_speaker_portrait = str(2)
dap_tuning_device_name_speaker_landscape = str(0)
dap_tuning_device_name_internal_speaker = str(1)
dap_tuning_device_name_hdmi = str(0)
dap_tuning_device_name_miracast = str(0)
dap_tuning_device_name_headphone_port = str(0)
dap_tuning_device_name_bluetooth = str(0)
dap_tuning_device_name_headphone_bluetooth = str(1)
dap_tuning_device_name_speaker_bluetooth = str(2)
dap_tuning_device_name_usb = str(0)
dap_tuning_device_name_headphone_usb = str(1)
dap_tuning_device_name_speaker_usb = str(2)
# define tuning device name for speaker port
speaker_tuning_name = {
    dap_tuning_device_name_speaker_landscape: 'Speaker_landscape',
    dap_tuning_device_name_internal_speaker: 'internal speaker',
    dap_tuning_device_name_speaker_portrait: 'Speaker_portrait'
}

# define dap four cc expected value when dap off for dolby content
# dolby content will apply the off profile value in qmf process
# non-dolby content will bypass all dap features
dap_off_four_cc_expected_dictionary_for_dolby_content_in_dax3 = {
    'dvle': '1',
    'dvlo': '-272',
    'vol': '0',
    'deon': '0',
    'ieon': '0',
    'dvme': '0',
    'dom': '0',
    'msce': '0',
    'miee': '0',
    'mdle': '0',
    'mdee': '0',
    'mave': '0',
    'ngon': '0'
}
# endpoint type defined in dom list
# index 0 means virtualizer enable or disable
# index 1 is ,
# index 2 means endpoint type : 0-spk 1-hp 2-pass though 3-other 4-default
# index 3 is ,
# index 4 means orientation : 0-portrait 1-landscape 2-N/A
index_endpoint_type_in_dom = 2
value_of_speaker_endpoint_type_in_dom = '0'
value_of_headphone_endpoint_type_in_dom = '1'
value_of_pass_through_endpoint_type_in_dom = '2'
value_of_other_endpoint_type_in_dom = '3'
value_of_default_endpoint_type_in_dom = '4'
invalid_value_endpoint_type_in_dom = '10'





