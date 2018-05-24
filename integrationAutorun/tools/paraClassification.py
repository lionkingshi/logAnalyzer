# add the number of below three type parameters and get the total number equal to 53
# define classification of device processing parameters (24)
COMPLEX_EQUALIZER = ('ceon', 'ceqt')
AUDIO_OPTIMIZER = ('aoon', 'aobs')
BASS_EXTRACTION = ('bexe', 'bew')
VIRTUAL_BASS = ('vbon', 'vbhg', 'vbog', 'vbsg', 'vbmf', 'vbsf', 'vbm')
BASS_ENHANCER = ('beon', 'becf', 'beb')
GRAPHIC_EQUALIZER = ('geon', 'gebs')
AUDIO_REGULATOR = ('aron', 'arde', 'arra', 'arod', 'artp', 'arbs')
# define classification of content processing parameters (26)
DIALOG_ENHANCER = ('deon', 'dea', 'ded')
VOLUME_LEVELER = ('dvle', 'dvla', 'dvli', 'dvlo')
INTELLIGENT_EQUALIZER = ('ieon', 'iea', 'iebs')
VOLUME_MODELER = ('dvme', 'dvmc')
MI_ = ('msce', 'miee', 'mdle', 'mdee', 'mave')
SURROUND_DECODER = ('ngon')
SPEAKER_VIRTUALIZER = ('dsa', 'dfsa', 'dhsa', 'dhfm')
VIRTUALIZER = ('dom', 'dsb')
VOL_MAX_BOOST = ('vmb')
CALIBRATION_BOOST = ('plb')
# define classification for parameter not existing in xml but still exist in log (3)
SYSTEM_GAIN = 'vol'
PREGAIN = 'preg'
POSTGAIN = 'pstg'

# define content processing parameters
CONTENT_PROCESSING_PARAM_LIST = ('deon', 'dvle', 'ieon', 'dvme', 'dom', 'msce', 'miee', 'mdle', 'mdee', 'mave', 'ngon')
# define device processing parameters
DEVICE_PROCESSING_PARAM_LIST = ('aoon', 'beon', 'vbon', 'vbm', 'bexe', 'geon', 'aron', 'arde', 'arra', 'arod', 'artp',
                                'arbs', 'ceon', 'ceqt')
# define qmf process expected parameter list
# for dax3 project , vol represents the system volume and exist in qmf and global process
PARA_LIST_IN_QMF_PROCESS = ('dea', 'iea', 'dsa', 'beb', 'plb', 'vmb', 'dsb', 'ded', 'vbm', 'dom', 'bew', 'dvla', 'dfsa',
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