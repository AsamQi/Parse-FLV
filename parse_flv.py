# -*- coding: utf-8 -*-
"""
Parse flv files
Usage:

As a module:
from parse_flv import Parse_flv
Parse_flv('xxx.flv')

or:
python parse_flv.py xxx.flv

"""
from struct import unpack
from os.path import getsize
import sys

log = open("parseflv.log", "w")


def _parse_array(flv, size):
    #Parse the information in script data.(About the meta data)
    for i in range(size):
        str_len = unpack('>H', flv.read(2))[0]
        str_name = flv.read(str_len)
        log.write('Title: %s.\n' % str_name)
        title_type = unpack('>B', flv.read(1))[0]
        log.write('The Type of this Title is: %d\n' % title_type)

        if title_type == 2:
            str_len = unpack('>H', flv.read(2))[0]
            log.write('%s\n\n' % flv.read(str_len))
        elif title_type == 12:
            str_len = unpack('>I', flv.read(4))[0]
            log.write('%s\n\n' % flv.read(str_len))
        elif title_type == 0:
            log.write('%f\n\n' % unpack('>d', flv.read(8))[0])

        elif title_type == 1:
            log.write('Bool: %s\n\n' % unpack('>B', flv.read(1))[0])

        elif title_type == 3:
            str_len = unpack('>H', flv.read(2))[0]
            log.write('%s\n' % flv.read(str_len))
            subType = unpack('>B', flv.read(1))[0]
            log.write('subType: %d\n' % subType)
            keyframe_num = unpack('>I', flv.read(4))[0]
            log.write('Size : %d\n' % keyframe_num)
            for i in range(keyframe_num):
                flv.seek(1, 1)
                temple_run = unpack('>d', flv.read(8))[0]
                log.write('\tid = %d: %d\n' % (i, temple_run))

            str_len2 = unpack('>H', flv.read(2))[0]
            log.write('%s\n' % flv.read(str_len2))
            subType2 = unpack('>B', flv.read(1))[0]
            log.write('subType2: %d\n' % subType2)
            keyframe_num2 = unpack('>I', flv.read(4))[0]
            log.write('Size : %d\n' % keyframe_num2)
            for i in range(keyframe_num2):
                flv.seek(1, 1)
                temple_run = unpack('>d', flv.read(8))[0]
                log.write('\tid = %d: %f\n' % (i, temple_run))


#Parse single flv file and take the meta info.
def Parse_flv(f):
    flv = open(f, 'rb')
    flv_head = unpack('>3s', flv.read(3))[0]
    if flv_head != "FLV":
        raise NameError('This is not FLV file!')
    flv.seek(13)
    first_tag = unpack('>B', flv.read(1))[0]
    if first_tag != 18:
        raise NameError('This is not standard script tag!')

    flv.seek(10, 1)
    amf1 = unpack('>B', flv.read(1))[0]
    if amf1 == 2:
        log.write('Reach the first Amf.\n')
    else:
        raise NameError('Error!')
    amf1_str_len = unpack('>H', flv.read(2))[0]
    amf1_str = flv.read(amf1_str_len)
    log.write('AMF1: %s\n' % amf1_str)

    amf2 = unpack('>B', flv.read(1))[0]
    if amf2 == 8:
        log.write('Reach the second Amf.\n')
    else:
        raise NameError('Error2!')
    array_size = unpack('>I', flv.read(4))[0]
    log.write('The array size is %d.\n\n' % array_size)

    _parse_array(flv, array_size)

    flv.close()


if __name__ == "__main__":
    Parse_flv(sys.argv[1])
