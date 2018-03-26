#!/usr/bin/python
"""
Created on Mar 21st, 2017
@author: twang
"""
import sys

# Input File
INPUT = 'effect_params.txt'

# Output File
OUTPUT = 'dap_cpdp.txt'

UTF_8 = 'utf-8'

STEREO = '1'
HEADPHONE = '9'

# define unique added four cc name in dax3 project
DAX3_UNIQUE_PARA = ('vol', 'ceon', 'ceqt')

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
    'vol'      :   'system-gain',
    'ceon'     :   'complex-equalizer-enable',
    'ceqt'     :   'complex-equalizer-tuning'
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

    elif id == 'vbmf' or id == 'vbsf' or id == 'ceqt':
        return value.replace(',', ':')
    else:
        return value


def dom(value):
    return STEREO
    # if value == '0':
    #     return STEREO
    # elif value == '2':
    #     return HEADPHONE
    # else:
    #     parameter = '11:2:'
    #     for eachNum in range(8):
    #         parameter += (value.split(',')[2*eachNum+1]) + ',' + (value.split(',')[2*eachNum+2]) + ':'
    #     result = parameter[:-1]
    #     return result


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


def translate(name, value):
    namev2 = DAP1_2_DAP2[name]
    valuev2 = mapping(name, value)
    parameter = ' --' + namev2 + '=' + valuev2
    return parameter


def transfer_para(input_file_name=INPUT, output_file_name=OUTPUT):
    print('Welcome to DAP Parameters Converter!')

    # Read data from dump file
    # fp_r = codecs.open(INPUT, 'r', UTF_8)
    # lines = fp_r.readlines()
    # fp_r.close()
    with open(input_file_name, 'r') as fp_r:
        lines = fp_r.readlines()
        fp_r.close()

    # default values
    content = 'dap_cpdp.exe --init=mi_process_disable=0,virtual_bass_process_enable=0,mode=0,max_num_objects=16\
    DapPcmInput.wav --out=processed.wav'

    # translate strings and values
    for line in lines:
        line = line.strip('\n')
        keys = (line.split('=')[0])
        values = (line.split('=')[1])
        if keys == 'vcbf':
            continue
        if keys == 'vbon':
            if values == '1':
                content = content.replace('virtual_bass_process_enable=0', 'virtual_bass_process_enable=1')
                continue
            else:
                continue
        # add code for dax3 project
        if keys in DAX3_UNIQUE_PARA:
            if values == 'non-exist':
                continue
            else:
                content += translate(keys, values)
        else:
            if values == 'non-exist':
                continue
            else:
                content += translate(keys, values)

    # generate output
    # fp_w = codecs.open(OUTPUT, 'w', UTF_8)
    # fp_w.write(content)
    # fp_w.close()
    with open(output_file_name, 'w') as fp_w:
        fp_w.write(content)
        fp_w.close()

    print('Done! Refer to %s ' % output_file_name)


def main():
    transfer_para()


if __name__ == "__main__":
    try:
        sys.exit(main())
    except SystemExit:
        print ('!!!!! error info' + sys.exc_info()[0])
        print ('!!!!! fail DAP Parameters Converter ')
        pass

