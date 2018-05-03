from constant import *

# define test data
# ************************************************************************************
# ************************************************************************************
# *****************     test data for be feature        ******************************
# ************************************************************************************
# ************************************************************************************
be_on_test_data = [
    ('stereo_channel_id.wav', content_type_2_channel_non_dolby, dap_status_on, dap_profile_custom_dax3,
     dap_feature_type_be_dax3, dap_feature_value_be_on),
    ('stereo_dd_25fps_channel_id.m4a', content_type_2_dd, dap_status_on, dap_profile_custom_dax3,
     dap_feature_type_be_dax3, dap_feature_value_be_on)
]
be_on_expected_value_speaker_endpoint = {'beon': '1', 'vbon': '1'}
be_on_expected_value_except_speaker_endpoint = {'beon': '1', 'vbon': '0'}
be_off_test_data = [
    ('stereo_dd_25fps_channel_id.m4a', content_type_2_dd, dap_status_on, dap_profile_custom_dax3,
     dap_feature_type_be_dax3, dap_feature_value_be_off),
    ('stereo_channel_id.wav', content_type_2_channel_non_dolby, dap_status_on, dap_profile_custom_dax3,
     dap_feature_type_be_dax3, dap_feature_value_be_off)
]
be_off_expected_value = {'beon': '0', 'vbon': '0'}

# ************************************************************************************
# ************************************************************************************
# *****************     test data for mi feature        ******************************
# ************************************************************************************
# ************************************************************************************
mi_on_2_channel_dolby_test_data = [
    ('1ch_ddp_25fps_acmod_1.mp4', content_type_1_ddp, dap_status_on, dap_profile_dynamic, None, None),
    ('stereo_dd_25fps_channel_id.m4a', content_type_2_dd, dap_status_on, dap_profile_dynamic, None, None)
]
mi_on_2_channel_expected_result = {'msce': '1', 'mdee': '1', 'miee': '1', 'mdle': '1', 'mave': '1'}

mi_on_multi_channel_dolby_test_data = [
    ('7ch_ddp_25fps_diff_music_01.mp4', content_type_71_ddp, dap_status_on, dap_profile_dynamic, None, None)
]
mi_on_multi_channel_expected_result = {'msce': '1', 'mdee': '1', 'miee': '1', 'mdle': '1', 'mave': '1'}

mi_on_non_dolby_test_data = [
    ('2ch_channel_id.wav', content_type_2_channel_non_dolby, dap_status_on, dap_profile_dynamic, None, None)
]
mi_on_non_dolby_content_expected_result = {'msce': '1', 'mdee': '1', 'miee': '1', 'mdle': '1', 'mave': '1'}

mi_off_test_data = [
    ('stereo_dd_25fps_channel_id.m4a', content_type_2_dd, dap_status_on, dap_profile_movie, None, None),
    ('2ch_channel_id.wav', content_type_2_channel_non_dolby, dap_status_on, dap_profile_music, None, None),
    ('7ch_ddp_25fps_diff_music_01.mp4', content_type_71_ddp, dap_status_on, dap_profile_custom_dax3, None, None)
]
mi_off_expected_result = {'msce': '0', 'mdee': '0', 'miee': '0', 'mdle': '0', 'mave': '0'}

# ************************************************************************************
# ************************************************************************************
# *****************     test data for up mix feature    ******************************
# ************************************************************************************
# ************************************************************************************
up_mix_and_vsv_off_test_data = [
    ('chopper_1.0_180_420_02.wav', content_type_1_channel_non_dolby, dap_status_on, dap_profile_custom_dax3,
     dap_feature_type_vsv, dap_feature_value_vsv_off),
    ('chopper_2.0_180_420_02.wav', content_type_2_channel_non_dolby, dap_status_on, dap_profile_custom_dax3,
     dap_feature_type_vsv, dap_feature_value_vsv_off),
    ('chopper_5.1_180_420.wav', content_type_51_channel_non_dolby, dap_status_on, dap_profile_custom_dax3,
     dap_feature_type_vsv, dap_feature_value_vsv_off),
    ('7ch_25fps.wav', content_type_71_channel_non_dolby, dap_status_on, dap_profile_custom_dax3,
     dap_feature_type_vsv, dap_feature_value_vsv_off),
    ('1ch_dd_25fps_acmod_1.mp4', content_type_1_dd, dap_status_on, dap_profile_custom_dax3,
     dap_feature_type_vsv, dap_feature_value_vsv_off),
    ('2ch_dd_25fps_channel_id.mp4', content_type_2_dd, dap_status_on, dap_profile_custom_dax3,
     dap_feature_type_vsv, dap_feature_value_vsv_off),
    ('Pearl_Harbour_French_5.1_dd_448Kbps.mp4', content_type_51_dd, dap_status_on, dap_profile_custom_dax3,
     dap_feature_type_vsv, dap_feature_value_vsv_off),
    ('1ch_ddp_25fps_acmod_1.mp4', content_type_1_ddp, dap_status_on, dap_profile_custom_dax3,
     dap_feature_type_vsv, dap_feature_value_vsv_off),
    ('2ch_ddp_25fps_ref_level.mp4', content_type_2_ddp, dap_status_on, dap_profile_custom_dax3,
     dap_feature_type_vsv, dap_feature_value_vsv_off),
    ('Eragon_5.1_ddp_128Kbps.mp4', content_type_51_ddp, dap_status_on, dap_profile_custom_dax3,
     dap_feature_type_vsv, dap_feature_value_vsv_off),
    ('7ch_ddp_25fps_diff_music_01.mp4', content_type_71_ddp, dap_status_on, dap_profile_custom_dax3,
     dap_feature_type_vsv, dap_feature_value_vsv_off),
    ('ChID_voices_51_384_ddp_joc.mp4', content_type_51_ddp_joc, dap_status_on, dap_profile_custom_dax3,
     dap_feature_type_vsv, dap_feature_value_vsv_off),
    ('Leaf_5P1JOC.mp4', content_type_51_ddp_joc, dap_status_on, dap_profile_custom_dax3,
     dap_feature_type_vsv, dap_feature_value_vsv_off),
    ('ChID_voices_71_640_ddp_joc.mp4', content_type_71_ddp_joc, dap_status_on, dap_profile_custom_dax3,
     dap_feature_type_vsv, dap_feature_value_vsv_off)
]

up_mix_and_hv_off_test_data = [
    ('chopper_1.0_180_420_02.wav', content_type_1_channel_non_dolby, dap_status_on, dap_profile_custom_dax3,
     dap_feature_type_hv, dap_feature_value_hv_off),
    ('chopper_2.0_180_420_02.wav', content_type_2_channel_non_dolby, dap_status_on, dap_profile_custom_dax3,
     dap_feature_type_hv, dap_feature_value_hv_off),
    ('chopper_5.1_180_420.wav', content_type_51_channel_non_dolby, dap_status_on, dap_profile_custom_dax3,
     dap_feature_type_hv, dap_feature_value_hv_off),
    ('7ch_25fps.wav', content_type_71_channel_non_dolby, dap_status_on, dap_profile_custom_dax3,
     dap_feature_type_hv, dap_feature_value_hv_off),
    ('1ch_dd_25fps_acmod_1.mp4', content_type_1_dd, dap_status_on, dap_profile_custom_dax3,
     dap_feature_type_hv, dap_feature_value_hv_off),
    ('2ch_dd_25fps_channel_id.mp4', content_type_2_dd, dap_status_on, dap_profile_custom_dax3,
     dap_feature_type_hv, dap_feature_value_hv_off),
    ('Pearl_Harbour_French_5.1_dd_448Kbps.mp4', content_type_51_dd, dap_status_on, dap_profile_custom_dax3,
     dap_feature_type_hv, dap_feature_value_hv_off),
    ('1ch_ddp_25fps_acmod_1.mp4', content_type_1_ddp, dap_status_on, dap_profile_custom_dax3,
     dap_feature_type_hv, dap_feature_value_hv_off),
    ('2ch_ddp_25fps_ref_level.mp4', content_type_2_ddp, dap_status_on, dap_profile_custom_dax3,
     dap_feature_type_hv, dap_feature_value_hv_off),
    ('Eragon_5.1_ddp_128Kbps.mp4', content_type_51_ddp, dap_status_on, dap_profile_custom_dax3,
     dap_feature_type_hv, dap_feature_value_hv_off),
    ('7ch_ddp_25fps_diff_music_01.mp4', content_type_71_ddp, dap_status_on, dap_profile_custom_dax3,
     dap_feature_type_hv, dap_feature_value_hv_off),
    ('ChID_voices_51_384_ddp_joc.mp4', content_type_51_ddp_joc, dap_status_on, dap_profile_custom_dax3,
     dap_feature_type_hv, dap_feature_value_hv_off),
    ('Leaf_5P1JOC.mp4', content_type_51_ddp_joc, dap_status_on, dap_profile_custom_dax3,
     dap_feature_type_hv, dap_feature_value_hv_off),
    ('ChID_voices_71_640_ddp_joc.mp4', content_type_71_ddp_joc, dap_status_on, dap_profile_custom_dax3,
     dap_feature_type_hv, dap_feature_value_hv_off)
]

up_mix_and_vsv_on_test_data = [
    ('chopper_1.0_180_420_02.wav', content_type_1_channel_non_dolby, dap_status_on, dap_profile_custom_dax3,
     dap_feature_type_vsv, dap_feature_value_vsv_off),
    ('chopper_2.0_180_420_02.wav', content_type_2_channel_non_dolby, dap_status_on, dap_profile_custom_dax3,
     dap_feature_type_vsv, dap_feature_value_vsv_off),
    ('chopper_5.1_180_420.wav', content_type_51_channel_non_dolby, dap_status_on, dap_profile_custom_dax3,
     dap_feature_type_vsv, dap_feature_value_vsv_off),
    ('7ch_25fps.wav', content_type_71_channel_non_dolby, dap_status_on, dap_profile_custom_dax3,
     dap_feature_type_vsv, dap_feature_value_vsv_off),
    ('1ch_dd_25fps_acmod_1.mp4', content_type_1_dd, dap_status_on, dap_profile_custom_dax3,
     dap_feature_type_vsv, dap_feature_value_vsv_off),
    ('2ch_dd_25fps_channel_id.mp4', content_type_2_dd, dap_status_on, dap_profile_custom_dax3,
     dap_feature_type_vsv, dap_feature_value_vsv_off),
    ('Pearl_Harbour_French_5.1_dd_448Kbps.mp4', content_type_51_dd, dap_status_on, dap_profile_custom_dax3,
     dap_feature_type_vsv, dap_feature_value_vsv_off),
    ('1ch_ddp_25fps_acmod_1.mp4', content_type_1_ddp, dap_status_on, dap_profile_custom_dax3,
     dap_feature_type_vsv, dap_feature_value_vsv_off),
    ('2ch_ddp_25fps_ref_level.mp4', content_type_2_ddp, dap_status_on, dap_profile_custom_dax3,
     dap_feature_type_vsv, dap_feature_value_vsv_off),
    ('Eragon_5.1_ddp_128Kbps.mp4', content_type_51_ddp, dap_status_on, dap_profile_custom_dax3,
     dap_feature_type_vsv, dap_feature_value_vsv_off),
    ('7ch_ddp_25fps_diff_music_01.mp4', content_type_71_ddp, dap_status_on, dap_profile_custom_dax3,
     dap_feature_type_vsv, dap_feature_value_vsv_off),
    ('ChID_voices_51_384_ddp_joc.mp4', content_type_51_ddp_joc, dap_status_on, dap_profile_custom_dax3,
     dap_feature_type_vsv, dap_feature_value_vsv_off),
    ('Leaf_5P1JOC.mp4', content_type_51_ddp_joc, dap_status_on, dap_profile_custom_dax3,
     dap_feature_type_vsv, dap_feature_value_vsv_off),
    ('ChID_voices_71_640_ddp_joc.mp4', content_type_71_ddp_joc, dap_status_on, dap_profile_custom_dax3,
     dap_feature_type_vsv, dap_feature_value_vsv_off)
]

up_mix_and_hv_on_test_data = [
    ('chopper_1.0_180_420_02.wav', content_type_1_channel_non_dolby, dap_status_on, dap_profile_custom_dax3,
     dap_feature_type_hv, dap_feature_value_hv_on),
    ('chopper_2.0_180_420_02.wav', content_type_2_channel_non_dolby, dap_status_on, dap_profile_custom_dax3,
     dap_feature_type_hv, dap_feature_value_hv_on),
    ('chopper_5.1_180_420.wav', content_type_51_channel_non_dolby, dap_status_on, dap_profile_custom_dax3,
     dap_feature_type_hv, dap_feature_value_hv_on),
    ('7ch_25fps.wav', content_type_71_channel_non_dolby, dap_status_on, dap_profile_custom_dax3,
     dap_feature_type_hv, dap_feature_value_hv_on),
    ('1ch_dd_25fps_acmod_1.mp4', content_type_1_dd, dap_status_on, dap_profile_custom_dax3,
     dap_feature_type_hv, dap_feature_value_hv_on),
    ('2ch_dd_25fps_channel_id.mp4', content_type_2_dd, dap_status_on, dap_profile_custom_dax3,
     dap_feature_type_hv, dap_feature_value_hv_on),
    ('Pearl_Harbour_French_5.1_dd_448Kbps.mp4', content_type_51_dd, dap_status_on, dap_profile_custom_dax3,
     dap_feature_type_hv, dap_feature_value_hv_on),
    ('1ch_ddp_25fps_acmod_1.mp4', content_type_1_ddp, dap_status_on, dap_profile_custom_dax3,
     dap_feature_type_hv, dap_feature_value_hv_on),
    ('2ch_ddp_25fps_ref_level.mp4', content_type_2_ddp, dap_status_on, dap_profile_custom_dax3,
     dap_feature_type_hv, dap_feature_value_hv_on),
    ('Eragon_5.1_ddp_128Kbps.mp4', content_type_51_ddp, dap_status_on, dap_profile_custom_dax3,
     dap_feature_type_hv, dap_feature_value_hv_on),
    ('7ch_ddp_25fps_diff_music_01.mp4', content_type_71_ddp, dap_status_on, dap_profile_custom_dax3,
     dap_feature_type_hv, dap_feature_value_hv_on),
    ('ChID_voices_51_384_ddp_joc.mp4', content_type_51_ddp_joc, dap_status_on, dap_profile_custom_dax3,
     dap_feature_type_hv, dap_feature_value_hv_on),
    ('Leaf_5P1JOC.mp4', content_type_51_ddp_joc, dap_status_on, dap_profile_custom_dax3,
     dap_feature_type_hv, dap_feature_value_hv_on),
    ('ChID_voices_71_640_ddp_joc.mp4', content_type_71_ddp_joc, dap_status_on, dap_profile_custom_dax3,
     dap_feature_type_hv, dap_feature_value_hv_on)
]

dap_off_test_data = [
    ('7ch_25fps.wav', content_type_71_channel_non_dolby, dap_status_on, dap_profile_custom_dax3,
     dap_feature_type_vsv, dap_feature_value_vsv_off),
    ('Eragon_5.1_ddp_128Kbps.mp4', content_type_51_ddp, dap_status_on, dap_profile_custom_dax3,
     dap_feature_type_vsv, dap_feature_value_vsv_off),
    ('7ch_ddp_25fps_diff_music_01.mp4', content_type_71_ddp, dap_status_on, dap_profile_custom_dax3,
     dap_feature_type_vsv, dap_feature_value_vsv_off),
    ('ChID_voices_71_640_ddp_joc.mp4', content_type_71_ddp_joc, dap_status_on, dap_profile_custom_dax3,
     dap_feature_type_vsv, dap_feature_value_vsv_off)
]

# ************************************************************************************
# ************************************************************************************
# ******     test data for decoder joc force down mix  feature    ********************
# ************************************************************************************
# ************************************************************************************

decoder_joc_force_down_mix_test_data = [
    ('1ch_dd_25fps_acmod_1.mp4', content_type_1_dd, dap_status_on, dap_profile_custom_dax3,
     dap_feature_type_vsv, dap_feature_value_vsv_off),
    ('2ch_dd_25fps_channel_id.mp4', content_type_2_dd, dap_status_on, dap_profile_custom_dax3,
     dap_feature_type_vsv, dap_feature_value_vsv_off),
    ('Pearl_Harbour_French_5.1_dd_448Kbps.mp4', content_type_51_dd, dap_status_on, dap_profile_custom_dax3,
     dap_feature_type_vsv, dap_feature_value_vsv_off),
    ('1ch_ddp_25fps_acmod_1.mp4', content_type_1_ddp, dap_status_on, dap_profile_custom_dax3,
     dap_feature_type_vsv, dap_feature_value_vsv_off),
    ('2ch_ddp_25fps_ref_level.mp4', content_type_2_ddp, dap_status_on, dap_profile_custom_dax3,
     dap_feature_type_vsv, dap_feature_value_vsv_off),
    ('Eragon_5.1_ddp_128Kbps.mp4', content_type_51_ddp, dap_status_on, dap_profile_custom_dax3,
     dap_feature_type_vsv, dap_feature_value_vsv_off),
    ('7ch_ddp_25fps_diff_music_01.mp4', content_type_71_ddp, dap_status_on, dap_profile_custom_dax3,
     dap_feature_type_vsv, dap_feature_value_vsv_off),
    ('ChID_voices_51_384_ddp_joc.mp4', content_type_51_ddp_joc, dap_status_on, dap_profile_custom_dax3,
     dap_feature_type_vsv, dap_feature_value_vsv_off),
    ('ChID_voices_71_640_ddp_joc.mp4', content_type_71_ddp_joc, dap_status_on, dap_profile_custom_dax3,
     dap_feature_type_vsv, dap_feature_value_vsv_off)
]


# ************************************************************************************
# ************************************************************************************
# *******     test data for decoder reference level feature    ***********************
# ************************************************************************************
# ************************************************************************************
reference_level_test_data = [
    ('2ch_ddp_25fps_ref_level.mp4', content_type_2_ddp, dap_status_on, dap_profile_custom_dax3,
     dap_feature_type_hv, dap_feature_value_hv_on),
    ('5ch_ddp_joc_25fps_ref_level.mp4', content_type_51_ddp_joc, dap_status_on, dap_profile_custom_dax3,
     dap_feature_type_hv, dap_feature_value_hv_on),
]
# ************************************************************************************
# ************************************************************************************
# *******     test data for profile default value verify      ************************
# ************************************************************************************
# ************************************************************************************
dynamic_profile_default_value_test_data = [
    ('7ch_25fps.wav', content_type_71_channel_non_dolby, dap_status_on, dap_profile_dynamic,
     dap_feature_type_hv, dap_feature_value_hv_on)
]
movie_profile_default_value_test_data = [
    ('7ch_25fps.wav', content_type_71_channel_non_dolby, dap_status_on, dap_profile_movie,
     dap_feature_type_hv, dap_feature_value_hv_on)
]
music_profile_default_value_test_data = [
    ('7ch_25fps.wav', content_type_71_channel_non_dolby, dap_status_on, dap_profile_music,
     dap_feature_type_hv, dap_feature_value_hv_on)
]
custom_profile_default_value_test_data = [
    ('7ch_25fps.wav', content_type_71_channel_non_dolby, dap_status_on, dap_profile_custom_dax3,
     dap_feature_type_hv, dap_feature_value_hv_on)
]
