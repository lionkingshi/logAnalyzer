# define content processing parameters
CONTENT_PROCESSING_PARAM_LIST = ('deon', 'dvle', 'ieon', 'dvme', 'dom', 'msce', 'miee', 'mdle', 'mdee', 'mave', 'ngon')
# define device processing parameters
DEVICE_PROCESSING_PARAM_LIST = ('aoon', 'beon', 'vbon', 'vbm', 'bexe', 'geon', 'aron', 'arde', 'arra', 'arod', 'artp',
                                'arbs')
# define qmf process expected parameter list
# for dax3 project , vol represents the system volume and exist in qmf and global process
PARA_LIST_IN_QMF_PROCESS = ('dea', 'iea', 'dsa', 'beb', 'plb', 'vmb', 'dsb', 'ded', 'vol', 'dom', 'bew', 'dvla', 'dfsa',
                            'dhsa', 'dvmc', 'msce', 'mdee', 'miee', 'mdle', 'dvle', 'dvme', 'mave', 'vcbf', 'becf',
                            'vbmf', 'vbsf', 'preg', 'vbhg', 'vbog', 'vbsg', 'dvli', 'dhfm', 'deon', 'ieon', 'ngon',
                            'dvlo', 'gebs', 'iebs', 'aobs', 'vol')
# define global process expected parameter list
# for dax3 project , added vol, ceon, ceqt to the tuple elements
PARA_LIST_IN_GLOBAL_PROCESS = ('dea', 'iea', 'dsa', 'beb', 'plb', 'vmb', 'dsb', 'ded', 'vbm', 'dom', 'bew', 'dvla',
                               'arra', 'dfsa', 'dhsa', 'dvmc', 'arod', 'msce', 'arde', 'mdee', 'miee', 'mdle', 'dvle',
                               'dvme', 'mave', 'vcbf', 'becf', 'vbmf', 'vbsf', 'preg', 'vbhg', 'vbog', 'vbsg', 'dvli',
                               'dhfm', 'vbon', 'beon', 'deon', 'geon', 'ieon', 'ngon', 'aoon', 'aron', 'dvlo', 'artp',
                               'pstg', 'gebs', 'iebs', 'aobs', 'arbs', 'vol', 'ceon', 'ceqt')
# define the process name as first filter key word in log file
QMF_PROCESS_NAME = 'DlbDap2QmfProcess'
GLOBAL_PROCESS_NAME = 'DlbDap2Process'

# define key words in audio chain for dolby content
KEY_WORDS_IN_AUDIO_CHAIN_FOR_DOLBY_CONTENT = [
    'featureTest', 'AudioTrack', 'AudioFlinger', 'OMXMaster',
    'NuPlayer', 'ARenderer:', ' ACodec  :', 'MediaCodec:',
    'DlbDlbEffect', 'DlbDapCrossfadeProcess', 'DlbDapEndpointParamCache', 'DapController',
    'DMSService', 'DlbDap2Process', 'DlbDap2QmfProcess', 'DlbEffectContext',
    'DDP_JOCDecoder', 'evo_parser', 'udc_user', 'ddpdec_client_joc'
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
    'DlbDap2QmfProcess: DAP output mode set',  # for DlbDap2QmfProcess and DlbDap2Process
    'DlbDap2Process: DAP output mode set',  # for DlbDap2QmfProcess and DlbDap2Process
    'mix matrix'
]