# define parameters not defined in xml file
PARA_LIST_NOT_EXIST_XML_FILE = ('vcbf', 'preg', 'pstg', 'vol', 'bexe')
# add the number of below three type parameters and get the total number equal to 53
# define classification of device processing parameters (24)
COMPLEX_EQUALIZER = ('ceon', 'ceqt')
AUDIO_OPTIMIZER = ('aoon', 'aobs')
BASS_EXTRACTION = ('bexe', 'bew')
VIRTUAL_BASS = ('vbon', 'vbhg', 'vbog', 'vbsg', 'vbmf', 'vbsf', 'vbm')
BASS_ENHANCER = ('beon', 'becf', 'beb')
GRAPHIC_EQUALIZER = ('geon', 'gebs')
AUDIO_REGULATOR = ('aron', 'arde', 'arra', 'arod', 'artp', 'arbs')
ASSEMBLED_DEVICE_PROCESSING_PARA_LIST = AUDIO_OPTIMIZER + AUDIO_REGULATOR + BASS_ENHANCER + BASS_EXTRACTION + \
                                              VIRTUAL_BASS + GRAPHIC_EQUALIZER + COMPLEX_EQUALIZER
# define classification of content processing parameters (26)
CALIBRATION_BOOST = 'plb'
DIALOG_ENHANCER = ('deon', 'dea', 'ded')
VOL_MAX_BOOST = 'vmb'
VOLUME_LEVELER = ('dvle', 'dvla', 'dvli', 'dvlo', VOL_MAX_BOOST)
VOLUME_MODELER = ('dvme', 'dvmc')
INTELLIGENT_EQUALIZER = ('ieon', 'iea', 'iebs')
MEDIA_INTELLIGENT = ('msce', 'miee', 'mdle', 'mdee', 'mave')
SURROUND_DECODER = 'ngon'
SPEAKER_VIRTUALIZER = ('dsa', 'dfsa', 'dhsa', 'dhfm')
VIRTUALIZER = (SURROUND_DECODER, 'dom', 'dsb', CALIBRATION_BOOST)
ASSEMBLED_CONTENT_PROCESSING_PARA_LIST = DIALOG_ENHANCER + \
                                               VOLUME_LEVELER + VOLUME_MODELER + \
                                               INTELLIGENT_EQUALIZER + \
                                               MEDIA_INTELLIGENT + \
                                               VIRTUALIZER + SPEAKER_VIRTUALIZER
# define classification for parameter not existing in xml but still exist in log (3)
SYSTEM_GAIN = 'vol'
PREGAIN = 'preg'
POSTGAIN = 'pstg'
ASSEMBLE_OTHER_PARA_LIST = (SYSTEM_GAIN, PREGAIN, POSTGAIN)

# define content processing parameters
CONTENT_PROCESSING_PARAM_LIST = ('deon', 'dvle', 'ieon', 'dvme', 'dom', 'msce', 'miee', 'mdle', 'mdee', 'mave', 'ngon')
# define device processing parameters
DEVICE_PROCESSING_PARAM_LIST = ('aoon', 'beon', 'vbon', 'vbm', 'bexe', 'geon', 'aron', 'arde', 'arra', 'arod', 'artp',
                                'arbs', 'ceon', 'ceqt')
# define qmf process expected parameter list
# for dax3 project , vol represents the system volume and exist in qmf and global process
# total 14
DUPLICATED_PARA_LIST_IN_QMF_PROCESS = ('beb', 'becf', 'bew', 'vbm', 'vcbf', 'vbmf', 'vbsf', 'vbhg', 'vbog', 'vbsg',
                                      'gebs', 'aobs', 'vol', 'preg')
PARA_LIST_IN_QMF_PROCESS = ASSEMBLED_CONTENT_PROCESSING_PARA_LIST + DUPLICATED_PARA_LIST_IN_QMF_PROCESS
# PARA_LIST_IN_QMF_PROCESS=('dea', 'iea', 'dsa', 'beb', 'plb', 'vmb', 'dsb', 'ded', 'vbm', 'dom', 'bew', 'dvla', 'dfsa',
#                             'dhsa', 'dvmc', 'msce', 'mdee', 'miee', 'mdle', 'dvle', 'dvme', 'mave', 'vcbf', 'becf',
#                             'vbmf', 'vbsf', 'preg', 'vbhg', 'vbog', 'vbsg', 'dvli', 'dhfm', 'deon', 'ieon', 'ngon',
#                             'dvlo', 'gebs', 'iebs', 'aobs', 'vol')
# define global process expected parameter list
# for dax3 project , added vol, ceon, ceqt to the tuple elements
PARA_LIST_AC4 = ('dea', 'ieid', 'iea', 'dfsa', 'dvlo', 'endp', 'prei', 'mixp', 'drc')
# define global process expected parameter list
# for dax3 project , added vol, ceon, ceqt to the tuple elements
PARA_LIST_IN_GLOBAL_PROCESS = ASSEMBLED_CONTENT_PROCESSING_PARA_LIST + \
                              ASSEMBLED_DEVICE_PROCESSING_PARA_LIST + \
                              ASSEMBLE_OTHER_PARA_LIST
# PARA_LIST_IN_GLOBAL_PROCESS = ('dea', 'iea', 'dsa', 'beb', 'plb', 'vmb', 'dsb', 'ded', 'vbm', 'dom', 'bew', 'dvla',
#                                'arra', 'dfsa', 'dhsa', 'dvmc', 'arod', 'msce', 'arde', 'mdee', 'miee', 'mdle', 'dvle',
#                                'dvme', 'mave', 'vcbf', 'becf', 'vbmf', 'vbsf', 'preg', 'vbhg', 'vbog', 'vbsg', 'dvli',
#                                'dhfm', 'vbon', 'beon', 'deon', 'geon', 'ieon', 'ngon', 'aoon', 'aron', 'dvlo', 'artp',
#                                'pstg', 'gebs', 'iebs', 'aobs', 'arbs', 'vol', 'ceon', 'ceqt')

# define the process name as first filter key word in log file
QMF_PROCESS_NAME = 'DlbDap2QmfProcess'
GLOBAL_PROCESS_NAME = 'DlbDap2Process'
AC4_PROCESS_NAME = 'Ac4DecWrapper'

# define key words in audio chain for dolby content
KEY_WORDS_IN_AUDIO_CHAIN_FOR_DOLBY_CONTENT = [
    'featureTest', 'AudioTrack', 'AudioFlinger', 'OMXMaster',
    'NuPlayer', 'ARenderer:', ' ACodec  :', 'MediaCodec:',
    'DlbDlbEffect', 'DlbDapCrossfadeProcess', 'DlbDapEndpointParamCache', 'DapController',
    'DMSService', 'DlbDap2Process', 'DlbDap2QmfProcess', 'DlbEffectContext',
    'DDP_JOCDecoder', 'evo_parser', 'udc_user', 'ddpdec_client_joc',
    'Ac4', 'AC4', 'ac4'
]
# define key words in audio chain for non dolby content
KEY_WORDS_IN_AUDIO_CHAIN_FOR_NON_DOLBY_CONTENT = [
    'featureTest', 'AudioTrack', 'AudioFlinger', 'OMXMaster',
    'NuPlayer', 'ARenderer:', ' ACodec  :', 'MediaCodec:',
    'DlbDlbEffect', 'DlbDapCrossfadeProcess', 'DlbDapEndpointParamCache', 'DapController',
    'DMSService', 'DlbDap2Process'
]
# define specified feature key word dictionary
DAP_JOC_FORCE_DOWN_MIX_INDEX = 0
DAP_OUT_PUT_MODE_FOR_DOLBY_CONTENT_INDEX = 1
DAP_OUT_PUT_MODE_FOR_NON_DOLBY_CONTENT_INDEX = 2
DAP_MIX_MATRIX_INDEX = 3
SPECIFIED_FEATURE_KEY_WORDS_LIST = [
    'DDP_JOCDecoder: setMultiChannelPCMOutDownmix',
    # DlbDap2QmfProcess: DAP output mode set to 1 with 2 output channels and null mix matrix.
    'DlbDap2QmfProcess: DAP output mode set',  # for DlbDap2QmfProcess and DlbDap2Process
    # DlbDap2Process: DAP output mode set to 11 with 2 output channels and custom mix matrix.
    'DlbDap2Process: DAP output mode set',  # for DlbDap2QmfProcess and DlbDap2Process
    'mix matrix'
]

# define index of output mode, orientation and mix matrix in filtered string
INDEX_OUTPUT_MODE_IN_GLOBAL_PROCESS_LIST = -9
INDEX_ORIENTATION_IN_GLOBAL_PROCESS_LIST = -6
INDEX_MIX_MATRIX_IN_GLOBAL_PROCESS_LIST = -3
INDEX_OUTPUT_MODE_IN_QMF_PROCESS_LIST = -9
INDEX_ORIENTATION_IN_QMF_PROCESS_LIST = -6
INDEX_MIX_MATRIX_IN_QMF_PROCESS_LIST = -3

# for ac4 parameter comparison, all defined in ac4dec_wrapper.h file
# define ieid according to iebs
INDEX_IEQ_OFF = '0'
IEQ_DETAILED_SPECIFIED_STRING_IN_IEBS = "-411"
INDEX_IEQ_DETAILED = '3'
IEQ_BALANCED_SPECIFIED_STRING_IN_IEBS = "-283"
INDEX_IEQ_BALANCED = '1'
IEQ_WARM_SPECIFIED_STRING_IN_IEBS = "-235"
INDEX_IEQ_WARM = '2'
# define endp value
# 0x0200
AC4DEC_OUT_CH_LO_RO = '512'
# 0x0210
AC4DEC_OUT_CH_HEADPHONE = '528'
# 0x0211
AC4DEC_OUT_CH_SPEAKER_VIRT = '529'
# define Default mixing preference of main and associated
AC4DEC_WRAPPER_MAIN_ASSO_PREF_DEFAULT = '0'
# Default presentation index
AC4DEC_WRAPPER_PRESENTATION_INDEX_DEFAULT = '65535'
# Default drc mode when dap on and off
AC4DEC_WRAPPER_DRC_MODE_DEFAULT_DAP_ON = '-14'
AC4DEC_WRAPPER_DRC_MODE_DEFAULT_DAP_OFF = '-17'
# endpoint type defined in dom list
# index 0 means virtualizer enable or disable
# index 1 is ,
# index 2 means endpoint type : 0-spk 1-hp 2-pass though 3-other 4-default
# index 3 is ,
# index 4 means orientation : 0-portrait 1-landscape 2-N/A
index_orientation_type_in_dom = 4
value_of_speaker_portrait_type_in_dom = '0'
value_of_speaker_landscape_type_in_dom = '1'
value_of_unknown_orientation_type_in_dom = '2'
index_vir_status_in_dom = 0
index_endpoint_type_in_dom = 2
value_of_speaker_endpoint_type_in_dom = '0'
value_of_headphone_endpoint_type_in_dom = '1'
value_of_pass_through_endpoint_type_in_dom = '2'
value_of_other_endpoint_type_in_dom = '3'
value_of_default_endpoint_type_in_dom = '4'
invalid_value_endpoint_type_in_dom = '10'

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
# define dap four cc expected value when dap off for ac4 content
# dolby content will apply the off profile value in ac4 decoder
# non-dolby content will bypass all dap features
dap_off_four_cc_expected_dictionary_for_ac4_content_in_dax3 = {
    'dea': '0',
    'ieid': '0',
    'iea': '0',
    'dfsa': '0',
    'dvlo': '-17',
    'endp': AC4DEC_OUT_CH_LO_RO,
    'prei': AC4DEC_WRAPPER_PRESENTATION_INDEX_DEFAULT,
    'mixp': AC4DEC_WRAPPER_MAIN_ASSO_PREF_DEFAULT,
    'drc': AC4DEC_WRAPPER_DRC_MODE_DEFAULT_DAP_OFF
}
