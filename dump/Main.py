#!/usr/bin/python
'''
Created on Mar 21st, 2017
@author: twang
'''


import sys
import codecs
import DAP


def translate(name, value):
    namev2 = DAP.DAP1_2_DAP2[name]
    valuev2 = DAP.mapping(name, value)
    parameter = ' --' + namev2 + '=' + valuev2
    return parameter


def main():
    print('Welcome to DAP Parameters Converter!')

    # Read data from dump file
    #fp_r = codecs.open(DAP.INPUT, 'r', DAP.UTF_8)
    #lines = fp_r.readlines()
    #fp_r.close()
    with open(DAP.INPUT, 'r') as fp_r:
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
        content += translate(keys, values)

    # generate output
    #fp_w = codecs.open(DAP.OUTPUT, 'w', DAP.UTF_8)
    #fp_w.write(content)
    #fp_w.close()
    with open(DAP.OUTPUT, 'w') as fp_w:
        fp_w.write(content)
        fp_w.close()

    print('Done! Refer to dap_cpdp.txt')


if __name__ == "__main__":
    sys.exit(main())





