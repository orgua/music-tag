#!/usr/bin/env python
# coding: utf-8

# FIXME: there's probably a more standard way of setting desc or repeated tags
# FIXME: there's probably a better way of dealing with pic_type

import mutagen
import mutagen.id3
import mutagen.easyid3
import mutagen.mp3
import mutagen.trueaudio

from music_tag import util
from music_tag.file import Artwork, AudioFile, MetadataItem, TAG_MAP_ENTRY


def get_tracknumA(afile, norm_key):
    return util.get_easy_tracknum(afile, norm_key, _tag_name='TRK')
def set_tracknumA(afile, norm_key, val):
    return util.set_easy_tracknum(afile, norm_key, val, _tag_name='TRK')
def get_totaltracksA(afile, norm_key):
    return util.get_easy_totaltracks(afile, norm_key, _tag_name='TRK')
def set_totaltracksA(afile, norm_key, val):
    return util.set_easy_totaltracks(afile, norm_key, val, _tag_name='TRK')

def get_discnumA(afile, norm_key):
    return util.get_easy_discnum(afile, norm_key, _tag_name='TPA')
def set_discnumA(afile, norm_key, val):
    return util.set_easy_discnum(afile, norm_key, val, _tag_name='TPA')
def get_totaldiscsA(afile, norm_key):
    return util.get_easy_totaldiscs(afile, norm_key, _tag_name='TPA')
def set_totaldiscsA(afile, norm_key, val):
    return util.set_easy_totaldiscs(afile, norm_key, val, _tag_name='TPA')

def get_tracknumB(afile, norm_key):
    return util.get_easy_tracknum(afile, norm_key, _tag_name='TRCK')
def set_tracknumB(afile, norm_key, val):
    return util.set_easy_tracknum(afile, norm_key, val, _tag_name='TRCK')
def get_totaltracksB(afile, norm_key):
    return util.get_easy_totaltracks(afile, norm_key, _tag_name='TRCK')
def set_totaltracksB(afile, norm_key, val):
    return util.set_easy_totaltracks(afile, norm_key, val, _tag_name='TRCK')

def get_discnumB(afile, norm_key):
    return util.get_easy_discnum(afile, norm_key, _tag_name='TPOS')
def set_discnumB(afile, norm_key, val):
    return util.set_easy_discnum(afile, norm_key, val, _tag_name='TPOS')
def get_totaldiscsB(afile, norm_key):
    return util.get_easy_totaldiscs(afile, norm_key, _tag_name='TPOS')
def set_totaldiscsB(afile, norm_key, val):
    return util.set_easy_totaldiscs(afile, norm_key, val, _tag_name='TPOS')

def get_pictures(afile, norm_key):
    pics = afile.mfile.tags.getall('APIC') + afile.mfile.tags.getall('PIC')
    artworks = []
    for p in pics:
        artworks.append(Artwork(p.data, pic_type=p.type))
    return MetadataItem(Artwork, None, artworks)

def set_pictures(afile, norm_key, artworks):
    if afile.mfile.tags.getall('APIC'):
        kls = mutagen.id3.APIC
    elif afile.mfile.tags.getall('PIC'):
        kls = mutagen.id3.PIC
    else:
        if afile.mfile.tags.version[:2] == (2, 2):
            kls = mutagen.id3.PIC
        else:
            kls = mutagen.id3.APIC

    tag = str(kls.__name__).strip(':')
    afile.mfile.tags.delall(tag)
    for i, art in enumerate(artworks.values):
        afile.mfile.tags.add(kls(data=art.raw, type=art.pic_type, desc=str(i)))

# https://github.com/tilo/ID3/tree/master/docs

_TAG_MAP_ID3_2_2 = {
    'tracktitle': TAG_MAP_ENTRY(getter='TT2', setter='TT2', type=str),
    'artist': TAG_MAP_ENTRY(getter='TP1', setter='TP1', type=str),
    'album': TAG_MAP_ENTRY(getter='TAL', setter='TAL', type=str),
    'albumartist': TAG_MAP_ENTRY(getter='TP2', setter='TP2', type=str),
    'composer': TAG_MAP_ENTRY(getter='TCM', setter='TCM', type=str),
    'tracknumber': TAG_MAP_ENTRY(getter=get_tracknumA,
                                 setter=set_tracknumA,
                                 type=str),
    'totaltracks': TAG_MAP_ENTRY(getter=get_totaltracksA,
                                 setter=set_totaltracksA,
                                 type=str),
    'discnumber': TAG_MAP_ENTRY(getter=get_discnumA,
                                setter=set_discnumA,
                                type=str),
    'totaldiscs': TAG_MAP_ENTRY(getter=get_totaldiscsA,
                                setter=set_totaldiscsA,
                                type=str),
    'genre': TAG_MAP_ENTRY(getter='TCO', setter='TCO', type=str),
    'year': TAG_MAP_ENTRY(getter=('TYE', 'TDA', 'TRD', 'TOR'),
                          setter=('TYE', 'TDA', 'TRD', 'TOR'),
                          type=str),
    # 'comment': TAG_MAP_ENTRY(getter='COMM', setter='COMM', type=str,
    #                          sanitizer=util.sanitize_bool),
    # 'lyrics': TAG_MAP_ENTRY(getter='USLT', setter='USLT', type=str),
    # 'compilation': TAG_MAP_ENTRY(getter='TCMP', setter='TCMP', type=int),

    'artwork': TAG_MAP_ENTRY(getter=get_pictures, setter=set_pictures,
                             type=Artwork),
}

_TAG_MAP_ID3_2_3 = {
    'tracktitle': TAG_MAP_ENTRY(getter='TIT2', setter='TIT2', type=str),
    'artist': TAG_MAP_ENTRY(getter='TPE1', setter='TPE1', type=str),
    'album': TAG_MAP_ENTRY(getter='TALB', setter='TALB', type=str),
    'albumartist': TAG_MAP_ENTRY(getter='TPE2', setter='TPE2', type=str),
    'composer': TAG_MAP_ENTRY(getter='TCOM', setter='TCOM', type=str),
    'tracknumber': TAG_MAP_ENTRY(getter=get_tracknumB,
                                 setter=set_tracknumB,
                                 type=str),
    'totaltracks': TAG_MAP_ENTRY(getter=get_totaltracksB,
                                 setter=set_totaltracksB,
                                 type=str),
    'discnumber': TAG_MAP_ENTRY(getter=get_discnumB,
                                setter=set_discnumB,
                                type=str),
    'totaldiscs': TAG_MAP_ENTRY(getter=get_totaldiscsB,
                                setter=set_totaldiscsB,
                                type=str),
    'genre': TAG_MAP_ENTRY(getter='TCON', setter='TCON', type=str),
    'year': TAG_MAP_ENTRY(getter=('ASDF', 'TORY', 'TYER', 'TDAT', 'TDRC'),
                          setter=('ASDF', 'TORY', 'TYER', 'TDAT', 'TDRC'),
                          type=str),
    'comment': TAG_MAP_ENTRY(getter='COMM', setter='COMM', type=str),
    'lyrics': TAG_MAP_ENTRY(getter='USLT', setter='USLT', type=str),
    'compilation': TAG_MAP_ENTRY(getter='TCMP', setter='TCMP', type=str),

    'artwork': TAG_MAP_ENTRY(getter=get_pictures, setter=set_pictures,
                             type=Artwork),
}

_TAG_MAP_ID3_2_4 = {
    'tracktitle': TAG_MAP_ENTRY(getter='TIT2', setter='TIT2', type=str),
    'artist': TAG_MAP_ENTRY(getter='TPE1', setter='TPE1', type=str),
    'album': TAG_MAP_ENTRY(getter='TALB', setter='TALB', type=str),
    'albumartist': TAG_MAP_ENTRY(getter='TPE2', setter='TPE2', type=str),
    'composer': TAG_MAP_ENTRY(getter='TCOM', setter='TCOM', type=str),
    'tracknumber': TAG_MAP_ENTRY(getter=get_tracknumB,
                                 setter=set_tracknumB,
                                 remover=('TRK', 'TRCK'),
                                 type=str),
    'totaltracks': TAG_MAP_ENTRY(getter=get_totaltracksB,
                                 setter=set_totaltracksB,
                                 remover=('TRK', 'TRCK'),
                                 type=str),
    'discnumber': TAG_MAP_ENTRY(getter=get_discnumB,
                                setter=set_discnumB,
                                remover=('TPA', 'TPOS'),
                                type=str),
    'totaldiscs': TAG_MAP_ENTRY(getter=get_totaldiscsB,
                                setter=set_totaldiscsB,
                                remover=('TPA', 'TPOS'),
                                type=str),
    'genre': TAG_MAP_ENTRY(getter='TCON', setter='TCON',
                           type=str),
    'year': TAG_MAP_ENTRY(getter=('TDOR', 'TORY', 'TYER', 'TDAT', 'TDRC'),
                          setter=('TDOR', 'TYER', 'TDAT', 'TDRC'),
                          type=str),
    'comment': TAG_MAP_ENTRY(getter='COMM', setter='COMM', type=str),
    'lyrics': TAG_MAP_ENTRY(getter='USLT', setter='USLT', type=str),
    'compilation': TAG_MAP_ENTRY(getter='TCMP', setter='TCMP', type=str),

    'artwork': TAG_MAP_ENTRY(getter=get_pictures, setter=set_pictures,
                             remover=('APIC', 'PIC'),
                             type=Artwork),
}


class Id3File(AudioFile):
    tag_format = "Id3"
    mutagen_kls = mutagen.id3.ID3FileType

    def __init__(self, filename, **kwargs):
        mfile = kwargs.get('_mfile', None)
        if mfile is None:
            mfile = mutagen.File(filename)
            kwargs['_mfile'] = mfile

        id3_ver = mfile.tags.version[:2]
        if id3_ver == (2, 2):
            self._TAG_MAP = _TAG_MAP_ID3_2_2
        elif id3_ver == (2, 3):
            self._TAG_MAP = _TAG_MAP_ID3_2_3
        elif id3_ver == (2, 4):
            self._TAG_MAP = _TAG_MAP_ID3_2_4
        else:
            raise NotImplementedError("Unexpected id3 tag version: {0}"
                                      "".format(mfile.tags.version))

        super(Id3File, self).__init__(filename, **kwargs)

    def _ft_getter(self, key):
        vals = self.mfile.tags.getall(key)
        ret = []
        for val in vals:
            if isinstance(val.text, (list, tuple)):
                ret += [str(t) for t in val.text]
            else:
                ret += [str(val.text)]
        return ret

    def _ft_setter(self, key, md_val, appendable=True):
        self.mfile.tags.delall(key)
        kls = getattr(mutagen.id3, key.split(':')[0])
        self.mfile.tags.add(kls(text=str(md_val)))

    def _ft_rmtag(self, key):
        self.mfile.tags.delall(key)


class Mp3File(Id3File):
    tag_format = "Mp3"
    mutagen_kls = mutagen.mp3.MP3

    def __init__(self, filename, **kwargs):
        super(Mp3File, self).__init__(filename, **kwargs)

        self.tag_map = self.tag_map.copy()
        self.tag_map.update({
            '#codec': TAG_MAP_ENTRY(getter=lambda afile, norm_key: 'mp3',
                                    type=str),
            '#bitspersample': TAG_MAP_ENTRY(getter=lambda afile, norm_key: None,
                                    type=int),
        })


class EasyMp3File(AudioFile):
    tag_format = "EasyMP3"
    mutagen_kls = mutagen.mp3.EasyMP3


class EasyId3File(AudioFile):
    tag_format = "EasyID3"
    mutagen_kls = mutagen.easyid3.EasyID3FileType


class TrueAudioFile(Id3File):
    tag_format = "TrueAudio"
    mutagen_kls = mutagen.trueaudio.TrueAudio


class EasyTrueAudioFile(AudioFile):
    tag_format = "EasyTrueAudio"
    mutagen_kls = mutagen.trueaudio.EasyTrueAudio
