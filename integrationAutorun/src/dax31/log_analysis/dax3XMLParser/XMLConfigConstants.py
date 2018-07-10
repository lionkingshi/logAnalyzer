from tools.filter_para_config import PARA_LIST_IN_GLOBAL_PROCESS
# profile feature dict,dom beon and vbon are specifal ones, they exist in both profile and tuning
# so only specified for profile,e.g dap_profile_dict[dom][0] is for profile, dap_profile_dict[dom][1] is for tuning
dap_profile_dict = {
    "ieon": "ieq-enable",
    "iea": "ieq-amount",
    "mdee": "mi-dialog-enhancer-steering-enable",
    "mdle": "mi-dv-leveler-steering-enable",
    "miee": "mi-ieq-steering-enable",
    "msce": "mi-surround-compressor-steering-enable",
    "mave": "mi-adaptive-virtualizer-steering-enable",
    "dvme": "volume-modeler-enable",
    "plb": "calibration-boost",
    "deon": "dialog-enhancer-enable",
    "dea": "dialog-enhancer-amount",
    "ded": "dialog-enhancer-ducking",
    "ngon": "surround-decoder-enable",
    "dsb": "surround-boost",
    "vmb": "volmax-boost",
    "dvle": "volume-leveler-enable",
    "dvla": "volume-leveler-amount",
    "dvli": "volume-leveler-in-target",
    "dvlo": "volume-leveler-out-target",
    "geon": "graphic-equalizer-enable",
    "dom": ["intermediate_profile_partial_virtualizer_enable", "intermediate_tuning_partial_virtualizer_enable"],
    "beon": ["intermediate_profile_bass-enhancer-enable", "intermediate_tuning_bass-enhancer-enable"],
    "vbon": ["intermediate_profile_partial_virtual_bass_enable", "intermediate_tuning_partial_virtual_bass_enable"]
}

# tuning featue dict
dap_tuning_dict = {
    "aobs": "band_optimizer",
    "arbs": "band_regulator",
    "aoon": "audio-optimizer-enable",
    "aron": "regulator-enable",
    "arde": "regulator-speaker-dist-enable",
    "beb": "bass-enhancer-boost",
    "becf": "bass-enhancer-cutoff-frequency",
    "bew": "bass-enhancer-width",
    "bexf": "bass-extraction-cutoff-frequency",
    "ceqt": ["complex-equalizer-tuning-left", "complex-equalizer-tuning-right"],
    "dhfm": "height-filter-mode",
    "arod": "regulator-overdrive",
    "artp": "regulator-timbre-preservation",
    "arra": "regulator-relaxation-amount",
    "vbm": "virtual-bass-mode",
    "vbog": "virtual-bass-overall-gain",
    "vbsg": "virtual-bass-slope-gain",
    "dfsa": "virtualizer-front-speaker-angle",
    "dhsa": "virtualizer-height-speaker-angle",
    "dsa": "virtualizer-surround-speaker-angle",
    "dvmc": "volume-modeler-calibration",
    "bexe": "bass-extraction-enable",
    "ceon": "complex-equalizer-enable",
    "vbmf": "virtual-bass-mix-freqs",
    "vbsf": "virtual-bass-src-freqs",
    "vbhg": "virtual-bass-subgains"
}
# supported dap feature list
# feature_list=[
# "ieon","iea","mdee","mdle","miee","msce","mave","dvme","plb","deon","dea","ded", \
# "ngon","dsb","vmb","dvle","dvla","dvli","dvlo","geon","dom","beon","vbon", \
# "aobs","arbs","aobs","arbs","aoon","aron","arde","beb","becf","bew","bexf","ceqt","dhfm", \
# "arod","artp","arra","vbm","vbog","vbsg","dfsa","dhsa","dsa","dvmc","bexe","ceon", \
# ]

# POST_PROCESSING_PARAS_LIST = [
#     'dea', 'iea', 'dsa', 'beb', 'plb', 'vmb', 'dsb', 'ded', 'vbm', 'dom', 'bew', 'dvla',
#     'arra', 'dfsa', 'dhsa', 'dvmc', 'arod', 'msce', 'arde', 'mdee', 'miee', 'mdle', 'dvle',
#     'dvme', 'mave', 'vcbf', 'becf', 'vbmf', 'vbsf', 'preg', 'vbhg', 'vbog', 'vbsg', 'dvli',
#     'dhfm', 'vbon', 'beon', 'deon', 'geon', 'ieon', 'ngon', 'aoon', 'aron', 'dvlo', 'artp',
#     'pstg', 'gebs', 'iebs', 'aobs', 'arbs', 'vol', 'ceon', 'ceqt'
# ]
POST_PROCESSING_PARAS_LIST = PARA_LIST_IN_GLOBAL_PROCESS

# tuning endpoint list
tuning_endpoint_name = ["Speaker_portrait", "Speaker_landscape", "Headphone", "Ext Spkr", "HDMI", "Miracast", "Unknown"]
profile_name = ["Dynamic", "Movie", "Music", "Custom", "Dynamic1", "Movie1", "Music1", "Custom1",
                "Dynamic2", "Movie2", "Music2", "Custom2", "Dynamic3", "Movie3", "Music3", "Custom3"]

band_optimizer_order = ["frequency", "gain_left", "gain_right", "gain_center", "gain_lfe", "gain_left_surround",
                        "gain_right_surround", "gain_left_rear_surround", "gain_right_rear_surround",
                        "gain_left_top_middle", "gain_right_top_middle"]

band_regulator_order = ["frequency", "threshold_low", "threshold_high", "isolated_band"]

iebs_order = ["frequency", "target"]
gebs_order = ["frequency", "gain"]

dom_endp_dict = {"speaker": 0, "headphone": 1, "passthrough": 2, "miracast": 3, "other": 4}
dom_ori_dict = {"portrait": 0, "landscape": 1, "N/A": 2}
