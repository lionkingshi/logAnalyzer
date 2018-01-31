#!/usr/bin/python
'''
Created on Mar 21st, 2017
@author: twang
'''

# Input File
INPUT = 'effect_params.txt'

# Output File
OUTPUT = 'dap_cpdp.txt'

UTF_8 = 'utf-8'

STEREO = '1'
HEADPHONE = '9'

#  "DAPv1 parameters name" to "DAPv2 parameters name"
DAP1_2_DAP2 = {
    'dea'      :   'dialog-enhancer-amount',
    'iea'      :   'ieq-amount',
    'dsa'      :   'virtualizer-surround-speaker-angle',
    'beb'      :   'bass-enhancer-boost',
    'plb'      :   'calibration-boost',
    'vmb'      :   'volmax-boost',
    'dsb'      :   'surround-boost',
    'ded'      :   'dialog-enhancer-ducking',
    'vbm'      :   'virtual-bass-mode',
    'dom'      :   'output-mode',
    'bew'      :   'bass-enhancer-width',
    'dvla'     :   'volume-leveler-amount',
    'arra'     :   'regulator-relaxation-amount',
    'dfsa'     :   'virtualizer-front-speaker-angle',
    'dhsa'     :   'virtualizer-height-speaker-angle',
    'dvmc'     :   'volume-modeler-calibration',
    'arod'     :   'regulator-overdrive',
    'msce'     :   'mi-surround-compressor-steering-enable',
    'arde'     :   'regulator-speaker-dist-enable',
    'mdee'     :   'mi-dialog-enhancer-steering-enable',
    'miee'     :   'mi-ieq-steering-enable',
    'mdle'     :   'mi-dv-leveler-steering-enable',
    'dvle'     :   'volume-leveler-enable',
    'dvme'     :   'volume-modeler-enable',
    'mave'     :   'mi-adaptive-virtualizer-steering-enable',
    'vcbf'     :   'NOT USED',
    'becf'     :   'bass-enhancer-cutoff-frequency',
    'vbmf'     :   'virtual-bass-mix-freqs',
    'vbsf'     :   'virtual-bass-src-freqs',
    'vbhg'     :   'virtual-bass-subgains',
    'vbog'     :   'virtual-bass-overall-gain',
    'vbsg'     :   'virtual-bass-slope-gain',
    'dvli'     :   'volume-leveler-in-target',
    'dhfm'     :   'height-filter-mode',
    'vbon'     :   'virtual-bass-process-enable',
    'beon'     :   'bass-enhancer-enable',
    'deon'     :   'dialog-enhancer-enable',
    'geon'     :   'graphic-equalizer-enable',
    'ieon'     :   'ieq-enable',
    'ngon'     :   'surround-decoder-enable',
    'aoon'     :   'audio-optimizer-enable',
    'aron'     :   'regulator-enable',
    'dvlo'     :   'volume-leveler-out-target',
    'artp'     :   'regulator-timbre-preservation',
    'preg'     :   'pregain',
    'pstg'     :   'postgain',
    'gebs'     :   'graphic-equalizer-bands',
    'iebs'     :   'ieq-bands',
    'aobs'     :   'audio-optimizer-bands',
    'arbs'     :   'regulator-tuning',
}


def mapping(id, value):
    if id == 'gebs':
        return gebs(value)

    elif id == 'iebs':
        return iebs(value)

    elif id == 'aobs':
        return aobs(value)

    elif id == 'arbs':
        return arbs(value)

    elif id == 'dom':
        return dom(value)

    elif id == 'vbmf' or id == 'vbsf':
        return value.replace(',', ':')

    else:
        return value


def dom(value):
    if value == '0':
        return STEREO
    elif value == '2':
        return HEADPHONE
    else:
        parameter = '11:2:'
        for eachNum in range(8):
            parameter += (value.split(',')[2*eachNum+1]) + ',' + (value.split(',')[2*eachNum+2]) + ':'
        result = parameter[:-1]
        return result


def gebs(value):
    parameter = ''
    for eachNum in range(20):
        parameter += (value.split(',')[eachNum+1]) + ':' + (value.split(',')[eachNum+21]) + ','
    result = parameter[:-1]
    return result


def iebs(value):
    parameter = ''
    for eachNum in range(20):
        parameter += (value.split(',')[eachNum+1]) + ':' + (value.split(',')[eachNum+21]) + ','
    result = parameter[:-1]
    return result


def aobs(value):
    parameter = ''
    for eachNum in range(20):
        parameter += (value.split(',')[eachNum + 2]) + ':' + (value.split(',')[eachNum + 22]) + ':' + \
                        (value.split(',')[eachNum + 42]) + ':' + (value.split(',')[eachNum + 62]) + ':' + \
                        (value.split(',')[eachNum + 82]) + ':' + (value.split(',')[eachNum + 102]) + ':' + \
                        (value.split(',')[eachNum + 122]) + ':' + (value.split(',')[eachNum + 142]) + ':' + \
                        (value.split(',')[eachNum + 162]) + ':' + (value.split(',')[eachNum + 182]) + ':' + \
                        (value.split(',')[eachNum + 202]) + ','
    result = parameter[:-1]
    return result


def arbs(value):
    parameter = ''
    for eachNum in range(20):
        parameter += (value.split(',')[eachNum+1]) + ':' + (value.split(',')[eachNum+21]) + ':' + \
                        (value.split(',')[eachNum + 41]) + ':' + (value.split(',')[eachNum + 61]) + ','
    result = parameter[:-1]
    return result

