# define sleep time before record device log
SLEEP_TIME_BEFORE_RECORD_LOG = 5
SLEEP_TIME_FOR_PUSH_MEDIA_TO_DUT = 15
SLEEP_TIME_FOR_ACTIVITY_START = 1
SLEEP_TIME_FOR_INSTALLING_APK = 3
# define play content
play_content_local_location = './mediaSrc/*'
play_content_device_location = '/sdcard/featureTest'
# define test apk location and name
test_apk_location = './apkSrc/app-debug.apk'
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

# define adb logcat command
adb_record_log = 'adb logcat -d >'
adb_record_log_append = 'adb logcat -d >>'
adb_clear_log = 'adb logcat -b all -c'

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


