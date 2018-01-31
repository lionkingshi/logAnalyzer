#!/usr/bin/python
'''
Created on Mar 21st, 2017
@author: twang
'''

import sys
from collections import OrderedDict



DAP1_2_DAP2 = OrderedDict()

def initilizeOrderedDict():
    DAP1_2_DAP2['dea'] = '0xffff'
    DAP1_2_DAP2['iea'] = '0xffff'
    DAP1_2_DAP2['dsa'] = '0xffff'
    DAP1_2_DAP2['beb'] = '0xffff'
    DAP1_2_DAP2['plb'] = '0xffff'
    DAP1_2_DAP2['vmb'] = '0xffff'
    DAP1_2_DAP2['dsb'] = '0xffff'
    DAP1_2_DAP2['ded'] = '0xffff'
    DAP1_2_DAP2['vbm'] = '0xffff'
    DAP1_2_DAP2['dom'] = '0xffff'
    DAP1_2_DAP2['bew'] = '0xffff'
    DAP1_2_DAP2['dvla'] = '0xffff'
    DAP1_2_DAP2['arra'] = '0xffff'
    DAP1_2_DAP2['dfsa'] = '0xffff'
    DAP1_2_DAP2['dhsa'] = '0xffff'
    DAP1_2_DAP2['dvmc'] = '0xffff'
    DAP1_2_DAP2['arod'] = '0xffff'
    DAP1_2_DAP2['msce'] = '0xffff'
    DAP1_2_DAP2['arde'] = '0xffff'
    DAP1_2_DAP2['mdee'] = '0xffff'
    DAP1_2_DAP2['miee'] = '0xffff'
    DAP1_2_DAP2['mdle'] = '0xffff'
    DAP1_2_DAP2['dvle'] = '0xffff'
    DAP1_2_DAP2['dvme'] = '0xffff'
    DAP1_2_DAP2['mave'] = '0xffff'
    DAP1_2_DAP2['vcbf'] = '0xffff'
    DAP1_2_DAP2['becf'] = '0xffff'
    DAP1_2_DAP2['vbmf'] = '0xffff'
    DAP1_2_DAP2['vbsf'] = '0xffff'
    DAP1_2_DAP2['preg'] = '0xffff'
    DAP1_2_DAP2['vbhg'] = '0xffff'
    DAP1_2_DAP2['vbog'] = '0xffff'
    DAP1_2_DAP2['vbsg'] = '0xffff'
    DAP1_2_DAP2['dvli'] = '0xffff'
    DAP1_2_DAP2['dhfm'] = '0xffff'
    DAP1_2_DAP2['vbon'] = '0xffff'
    DAP1_2_DAP2['beon'] = '0xffff'
    DAP1_2_DAP2['deon'] = '0xffff'
    DAP1_2_DAP2['geon'] = '0xffff'
    DAP1_2_DAP2['ieon'] = '0xffff'
    DAP1_2_DAP2['ngon'] = '0xffff'
    DAP1_2_DAP2['aoon'] = '0xffff'
    DAP1_2_DAP2['aron'] = '0xffff'
    DAP1_2_DAP2['dvlo'] = '0xffff'
    DAP1_2_DAP2['artp'] = '0xffff'
    DAP1_2_DAP2['pstg'] = '0xffff' # audio dump parameter does not include this
    DAP1_2_DAP2['gebs'] = '0xffff'
    DAP1_2_DAP2['iebs'] = '0xffff'
    DAP1_2_DAP2['aobs'] = '0xffff'
    DAP1_2_DAP2['arbs'] = '0xffff'


#  "DAPv1 parameters name" to "DAPv2 parameters name"


def main():
    print('Welcome to DAP Parameters Converter!')

    # initial the order dictory to align with audio dump parameter list
    initilizeOrderedDict()

    # Read data from log file
    with open('log.txt', 'r') as fp_r:
        lines = fp_r.readlines()
        fp_r.close()

    for line in lines:
        line = line.strip('\n')
        line = line.replace(' ','') # remove empty char
        FourccStartIndex = line.find('(') # dap parameter begin with '(' and end with '=''
        FourccEndIndex = line.find('=')
        FourccValueStartIndex = line.find('[') # dap parameter value begin with '[' and end with ']'
        FourccValueEndIndex = line.find(']')
        Fourcc = line[(FourccStartIndex+1):FourccEndIndex]
        FourccValue= line[(FourccValueStartIndex+1):FourccValueEndIndex]
        DAP1_2_DAP2[Fourcc] = FourccValue
        # print('fourcc : {name}={value}'.format(name=Fourcc,value=FourccValue))
        print('fourcc 2: {name}={value}'.format(name=Fourcc,value=DAP1_2_DAP2[Fourcc]))

    for key,value in DAP1_2_DAP2.items():
        print key + " => " + value

        # print('length : {length}'.format(length=len(line)))
        # print('line content is {content}'.format(content=line))
        # keys = (line.split('=')[0])
        # values = (line.split('=')[1])
        # print('dap paramater name {dap_para} and its value :{dap_para_value}'.format(dap_para=keys,dap_para_value=values))


    with open('effect_param1.txt', 'w') as fp_w:
        for key,value in DAP1_2_DAP2.items():
            content = key+"="+value+'\n'
            # print("write content to file :"+content)
            fp_w.write(content)
        fp_w.close()
    
    print('Done! Refer to dap_cpdp.txt')

if __name__ == "__main__":
    sys.exit(main())





