"""
A modern, Python3-compatible, well-documented library for communicating
with a MineCraft server.
"""

import re
from collections import OrderedDict, namedtuple

# The version number of the most recent pyCraft release.
__version__ = "0.7.0"

# This bit occurs in the protocol numbers of pre-release versions after 1.16.3.
PRE = 1 << 30

# A record representing a Minecraft version in the following list.
Version = namedtuple('Version', ('id', 'protocol', 'supported'))

# A list of Minecraft versions known to pyCraft, including all supported
# versions as well as some unsupported versions (used by certain forward-
# compatible code: e.g. when comparing the current protocol version with that
# of an unsupported version), in chronological order of publication.
#
# The ID string of a version is the key used to identify it in
# <https://launchermeta.mojang.com/mc/game/version_manifest.json>, or the 'id'
# key in "version.json" in the corresponding ".jar" file distributed by Mojang.
KNOWN_MINECRAFT_VERSION_RECORDS = [
    #       id                       protocol  supported
    Version('13w41a',                0,        False),
    Version('13w41b',                0,        False),
    Version('13w42a',                1,        False),
    Version('13w42b',                1,        False),
    Version('13w43a',                2,        False),
    Version('1.7-pre',               3,        False),
    Version('1.7.1-pre',             3,        False),
    Version('1.7.2',                 4,        True),
    Version('13w47a',                4,        False),
    Version('13w47b',                4,        False),
    Version('13w47c',                4,        False),
    Version('13w47d',                4,        False),
    Version('13w47e',                4,        False),
    Version('13w48a',                4,        False),
    Version('13w48b',                4,        False),
    Version('13w49a',                4,        False),
    Version('1.7.3-pre',             4,        False),
    Version('1.7.4',                 4,        True),
    Version('1.7.5',                 4,        True),
    Version('1.7.6-pre1',            5,        False),
    Version('1.7.6-pre2',            5,        False),
    Version('1.7.6',                 5,        True),
    Version('1.7.7',                 5,        True),
    Version('1.7.8',                 5,        True),
    Version('1.7.9',                 5,        True),
    Version('1.7.10-pre1',           5,        False),
    Version('1.7.10-pre2',           5,        False),
    Version('1.7.10-pre3',           5,        False),
    Version('1.7.10-pre4',           5,        False),
    Version('1.7.10',                5,        True),
    Version('14w02a',                5,        False),
    Version('14w02b',                5,        False),
    Version('14w02c',                5,        False),
    Version('14w03a',                6,        False),
    Version('14w03b',                6,        False),
    Version('14w04a',                7,        False),
    Version('14w04b',                8,        False),
    Version('14w05a',                9,        False),
    Version('14w05b',                9,        False),
    Version('14w06a',                10,       False),
    Version('14w06b',                10,       False),
    Version('14w07a',                11,       False),
    Version('14w08a',                12,       False),
    Version('14w10a',                13,       False),
    Version('14w10b',                13,       False),
    Version('14w10c',                13,       False),
    Version('14w11a',                14,       False),
    Version('14w11b',                14,       False),
    Version('14w17a',                15,       False),
    Version('14w18a',                16,       False),
    Version('14w18b',                16,       False),
    Version('14w19a',                17,       False),
    Version('14w20a',                18,       False),
    Version('14w20b',                18,       False),
    Version('14w21a',                19,       False),
    Version('14w21b',                20,       False),
    Version('14w25a',                21,       False),
    Version('14w25b',                22,       False),
    Version('14w26a',                23,       False),
    Version('14w26b',                24,       False),
    Version('14w26c',                25,       False),
    Version('14w27a',                26,       False),
    Version('14w27b',                26,       False),
    Version('14w28a',                27,       False),
    Version('14w28b',                28,       False),
    Version('14w29a',                29,       False),
    Version('14w29a',                29,       False),
    Version('14w30a',                30,       False),
    Version('14w30b',                30,       False),
    Version('14w30c',                31,       False),
    Version('14w31a',                32,       False),
    Version('14w32a',                33,       False),
    Version('14w32b',                34,       False),
    Version('14w32c',                35,       False),
    Version('14w32d',                36,       False),
    Version('14w33a',                37,       False),
    Version('14w33b',                38,       False),
    Version('14w33c',                39,       False),
    Version('14w34a',                40,       False),
    Version('14w34b',                41,       False),
    Version('14w34c',                42,       False),
    Version('14w34d',                43,       False),
    Version('1.8-pre1',              44,       False),
    Version('1.8-pre2',              45,       False),
    Version('1.8-pre3',              46,       False),
    Version('1.8',                   47,       True),
    Version('1.8.1-pre1',            47,       False),
    Version('1.8.1-pre2',            47,       False),
    Version('1.8.1-pre3',            47,       False),
    Version('1.8.1-pre4',            47,       False),
    Version('1.8.1-pre5',            47,       False),
    Version('1.8.1',                 47,       True),
    Version('1.8.2-pre1',            47,       False),
    Version('1.8.2-pre2',            47,       False),
    Version('1.8.2-pre3',            47,       False),
    Version('1.8.2-pre4',            47,       False),
    Version('1.8.2-pre5',            47,       False),
    Version('1.8.2-pre6',            47,       False),
    Version('1.8.2-pre7',            47,       False),
    Version('1.8.2',                 47,       True),
    Version('1.8.3',                 47,       True),
    Version('1.8.4',                 47,       True),
    Version('1.8.5',                 47,       True),
    Version('1.8.6',                 47,       True),
    Version('1.8.7',                 47,       True),
    Version('1.8.8',                 47,       True),
    Version('1.8.9',                 47,       True),
    Version('15w14a',                48,       False),
    Version('15w31a',                49,       False),
    Version('15w31b',                50,       False),
    Version('15w31c',                51,       False),
    Version('15w32a',                52,       False),
    Version('15w32b',                53,       False),
    Version('15w32c',                54,       False),
    Version('15w33a',                55,       False),
    Version('15w33b',                56,       False),
    Version('15w33c',                57,       False),
    Version('15w34a',                58,       False),
    Version('15w34b',                59,       False),
    Version('15w34c',                60,       False),
    Version('15w34d',                61,       False),
    Version('15w35a',                62,       False),
    Version('15w35b',                63,       False),
    Version('15w35c',                64,       False),
    Version('15w35d',                65,       False),
    Version('15w35e',                66,       False),
    Version('15w36a',                67,       False),
    Version('15w36b',                68,       False),
    Version('15w36c',                69,       False),
    Version('15w36d',                70,       False),
    Version('15w37a',                71,       False),
    Version('15w38a',                72,       False),
    Version('15w38b',                73,       False),
    Version('15w39a',                74,       False),
    Version('15w39b',                74,       False),
    Version('15w39c',                74,       False),
    Version('15w40a',                75,       False),
    Version('15w40b',                76,       False),
    Version('15w41a',                77,       False),
    Version('15w41b',                78,       False),
    Version('15w42a',                79,       False),
    Version('15w43a',                80,       False),
    Version('15w43b',                81,       False),
    Version('15w43c',                82,       False),
    Version('15w44a',                83,       False),
    Version('15w44b',                84,       False),
    Version('15w45a',                85,       False),
    Version('15w46a',                86,       False),
    Version('15w47a',                87,       False),
    Version('15w47b',                88,       False),
    Version('15w47c',                89,       False),
    Version('15w49a',                90,       False),
    Version('15w49b',                91,       False),
    Version('15w50a',                92,       False),
    Version('15w51a',                93,       False),
    Version('15w51b',                94,       False),
    Version('16w02a',                95,       False),
    Version('16w03a',                96,       False),
    Version('16w04a',                97,       False),
    Version('16w05a',                98,       False),
    Version('16w05b',                99,       False),
    Version('16w06a',                100,      False),
    Version('16w07a',                101,      False),
    Version('16w07b',                102,      False),
    Version('1.9-pre1',              103,      False),
    Version('1.9-pre2',              104,      False),
    Version('1.9-pre3',              105,      False),
    Version('1.9-pre4',              106,      False),
    Version('1.9',                   107,      True),
    Version('1.9.1-pre1',            107,      False),
    Version('1.9.1-pre2',            108,      False),
    Version('1.9.1-pre3',            108,      False),
    Version('1.9.1',                 108,      True),
    Version('1.RV-Pre1',             108,      False),
    Version('1.9.2',                 109,      True),
    Version('16w14a',                109,      False),
    Version('16w15a',                109,      False),
    Version('16w15b',                109,      False),
    Version('1.9.3-pre1',            109,      False),
    Version('1.9.3-pre2',            110,      False),
    Version('1.9.3-pre3',            110,      False),
    Version('1.9.3',                 110,      True),
    Version('1.9.4',                 110,      True),
    Version('16w20a',                201,      False),
    Version('16w21a',                202,      False),
    Version('16w21b',                203,      False),
    Version('1.10-pre1',             204,      False),
    Version('1.10-pre2',             205,      False),
    Version('1.10',                  210,      True),
    Version('1.10.1',                210,      True),
    Version('1.10.2',                210,      True),
    Version('16w32a',                301,      True),
    Version('16w32b',                302,      True),
    Version('16w33a',                303,      True),
    Version('16w35a',                304,      True),
    Version('16w36a',                305,      True),
    Version('16w38a',                306,      True),
    Version('16w39a',                307,      True),
    Version('16w39b',                308,      True),
    Version('16w39c',                309,      True),
    Version('16w40a',                310,      True),
    Version('16w41a',                311,      True),
    Version('16w42a',                312,      True),
    Version('16w43a',                313,      True),
    Version('16w44a',                313,      True),
    Version('1.11-pre1',             314,      True),
    Version('1.11',                  315,      True),
    Version('16w50a',                316,      True),
    Version('1.11.1',                316,      True),
    Version('1.11.2',                316,      True),
    Version('17w06a',                317,      True),
    Version('17w13a',                318,      True),
    Version('17w13b',                319,      True),
    Version('17w14a',                320,      True),
    Version('17w15a',                321,      True),
    Version('17w16a',                322,      True),
    Version('17w16b',                323,      True),
    Version('17w17a',                324,      True),
    Version('17w17b',                325,      True),
    Version('17w18a',                326,      True),
    Version('17w18b',                327,      True),
    Version('1.12-pre1',             328,      True),
    Version('1.12-pre2',             329,      True),
    Version('1.12-pre3',             330,      True),
    Version('1.12-pre4',             331,      True),
    Version('1.12-pre5',             332,      True),
    Version('1.12-pre6',             333,      True),
    Version('1.12-pre7',             334,      True),
    Version('1.12',                  335,      True),
    Version('17w31a',                336,      True),
    Version('1.12.1-pre1',           337,      True),
    Version('1.12.1',                338,      True),
    Version('1.12.2-pre1',           339,      True),
    Version('1.12.2-pre2',           339,      True),
    Version('1.12.2',                340,      True),
    Version('17w43a',                341,      True),
    Version('17w43b',                342,      True),
    Version('17w45a',                343,      True),
    Version('17w45b',                344,      True),
    Version('17w46a',                345,      True),
    Version('17w47a',                346,      True),
    Version('17w47b',                347,      True),
    Version('17w48a',                348,      True),
    Version('17w49a',                349,      True),
    Version('17w49b',                350,      True),
    Version('17w50a',                351,      True),
    Version('18w01a',                352,      True),
    Version('18w02a',                353,      True),
    Version('18w03a',                354,      True),
    Version('18w03b',                355,      True),
    Version('18w05a',                356,      True),
    Version('18w06a',                357,      True),
    Version('18w07a',                358,      True),
    Version('18w07b',                359,      True),
    Version('18w07c',                360,      True),
    Version('18w08a',                361,      True),
    Version('18w08b',                362,      True),
    Version('18w09a',                363,      True),
    Version('18w10a',                364,      True),
    Version('18w10b',                365,      True),
    Version('18w10c',                366,      True),
    Version('18w10d',                367,      True),
    Version('18w11a',                368,      True),
    Version('18w14a',                369,      True),
    Version('18w14b',                370,      True),
    Version('18w15a',                371,      True),
    Version('18w16a',                372,      True),
    Version('18w19a',                373,      True),
    Version('18w19b',                374,      True),
    Version('18w20a',                375,      True),
    Version('18w20b',                376,      True),
    Version('18w20c',                377,      True),
    Version('18w21a',                378,      True),
    Version('18w21b',                379,      True),
    Version('18w22a',                380,      True),
    Version('18w22b',                381,      True),
    Version('18w22c',                382,      True),
    Version('1.13-pre1',             383,      True),
    Version('1.13-pre2',             384,      True),
    Version('1.13-pre3',             385,      True),
    Version('1.13-pre4',             386,      True),
    Version('1.13-pre5',             387,      True),
    Version('1.13-pre6',             388,      True),
    Version('1.13-pre7',             389,      True),
    Version('1.13-pre8',             390,      True),
    Version('1.13-pre9',             391,      True),
    Version('1.13-pre10',            392,      True),
    Version('1.13',                  393,      True),
    Version('18w30a',                394,      True),
    Version('18w30b',                395,      True),
    Version('18w31a',                396,      True),
    Version('18w32a',                397,      True),
    Version('18w33a',                398,      True),
    Version('1.13.1-pre1',           399,      True),
    Version('1.13.1-pre2',           400,      True),
    Version('1.13.1',                401,      True),
    Version('1.13.2-pre1',           402,      True),
    Version('1.13.2-pre2',           403,      True),
    Version('1.13.2',                404,      True),
    Version('18w43a',                441,      True),
    Version('18w43b',                441,      True),
    Version('18w43c',                442,      True),
    Version('18w44a',                443,      True),
    Version('18w45a',                444,      True),
    Version('18w46a',                445,      True),
    Version('18w47a',                446,      True),
    Version('18w47b',                447,      True),
    Version('18w48a',                448,      True),
    Version('18w48b',                449,      True),
    Version('18w49a',                450,      True),
    Version('18w50a',                451,      True),
    Version('19w02a',                452,      True),
    Version('19w03a',                453,      True),
    Version('19w03b',                454,      True),
    Version('19w03c',                455,      True),
    Version('19w04a',                456,      True),
    Version('19w04b',                457,      True),
    Version('19w05a',                458,      True),
    Version('19w06a',                459,      True),
    Version('19w07a',                460,      True),
    Version('19w08a',                461,      True),
    Version('19w08b',                462,      True),
    Version('19w09a',                463,      True),
    Version('19w11a',                464,      True),
    Version('19w11b',                465,      True),
    Version('19w12a',                466,      True),
    Version('19w12b',                467,      True),
    Version('19w13a',                468,      True),
    Version('19w13b',                469,      True),
    Version('19w14a',                470,      True),
    Version('19w14b',                471,      True),
    Version('1.14 Pre-Release 1',    472,      True),
    Version('1.14 Pre-Release 2',    473,      True),
    Version('1.14 Pre-Release 3',    474,      True),
    Version('1.14 Pre-Release 4',    475,      True),
    Version('1.14 Pre-Release 5',    476,      True),
    Version('1.14',                  477,      True),
    Version('1.14.1 Pre-Release 1',  478,      True),
    Version('1.14.1 Pre-Release 2',  479,      True),
    Version('1.14.1',                480,      True),
    Version('1.14.2 Pre-Release 1',  481,      True),
    Version('1.14.2 Pre-Release 2',  482,      True),
    Version('1.14.2 Pre-Release 3',  483,      True),
    Version('1.14.2 Pre-Release 4',  484,      True),
    Version('1.14.2',                485,      True),
    Version('1.14.3-pre1',           486,      True),
    Version('1.14.3-pre2',           487,      True),
    Version('1.14.3-pre3',           488,      True),
    Version('1.14.3-pre4',           489,      True),
    Version('1.14.3',                490,      True),
    Version('1.14.4-pre1',           491,      True),
    Version('1.14.4-pre2',           492,      True),
    Version('1.14.4-pre3',           493,      True),
    Version('1.14.4-pre4',           494,      True),
    Version('1.14.4-pre5',           495,      True),
    Version('1.14.4-pre6',           496,      True),
    Version('1.14.4-pre7',           497,      True),
    Version('1.14.4',                498,      True),
    Version('19w34a',                550,      True),
    Version('19w35a',                551,      True),
    Version('19w36a',                552,      True),
    Version('19w37a',                553,      True),
    Version('19w38a',                554,      True),
    Version('19w38b',                555,      True),
    Version('19w39a',                556,      True),
    Version('19w40a',                557,      True),
    Version('19w41a',                558,      True),
    Version('19w42a',                559,      True),
    Version('19w44a',                560,      True),
    Version('19w45a',                561,      True),
    Version('19w45b',                562,      True),
    Version('19w46a',                563,      True),
    Version('19w46b',                564,      True),
    Version('1.15-pre1',             565,      True),
    Version('1.15-pre2',             566,      True),
    Version('1.15-pre3',             567,      True),
    Version('1.15-pre4',             569,      True),
    Version('1.15-pre5',             570,      True),
    Version('1.15-pre6',             571,      True),
    Version('1.15-pre7',             572,      True),
    Version('1.15',                  573,      True),
    Version('1.15.1-pre1',           574,      True),
    Version('1.15.1',                575,      True),
    Version('1.15.2-pre1',           576,      True),
    Version('1.15.2-pre2',           577,      True),
    Version('1.15.2',                578,      True),
    Version('20w06a',                701,      True),
    Version('20w07a',                702,      True),
    Version('20w08a',                703,      True),
    Version('20w09a',                704,      True),
    Version('20w10a',                705,      True),
    Version('20w11a',                706,      True),
    Version('20w12a',                707,      True),
    Version('20w13a',                708,      True),
    Version('20w13b',                709,      True),
    Version('20w14a',                710,      True),
    Version('20w15a',                711,      True),
    Version('20w16a',                712,      True),
    Version('20w17a',                713,      True),
    Version('20w18a',                714,      True),
    Version('20w19a',                715,      True),
    Version('20w20a',                716,      True),
    Version('20w20b',                717,      True),
    Version('20w21a',                718,      True),
    Version('20w22a',                719,      True),
    Version('1.16-pre1',             721,      True),
    Version('1.16-pre2',             722,      True),
    Version('1.16-pre3',             725,      True),
    Version('1.16-pre4',             727,      True),
    Version('1.16-pre5',             729,      True),
    Version('1.16-pre6',             730,      True),
    Version('1.16-pre7',             732,      True),
    Version('1.16-pre8',             733,      True),
    Version('1.16-rc1',              734,      True),
    Version('1.16',                  735,      True),
    Version('1.16.1',                736,      True),
    Version('20w27a',                738,      True),
    Version('20w28a',                740,      True),
    Version('20w29a',                741,      True),
    Version('20w30a',                743,      True),
    Version('1.16.2-pre1',           744,      True),
    Version('1.16.2-pre2',           746,      True),
    Version('1.16.2-pre3',           748,      True),
    Version('1.16.2-rc1',            749,      True),
    Version('1.16.2-rc2',            750,      True),
    Version('1.16.2',                751,      True),
    Version('1.16.3-rc1',            752,      True),
    Version('1.16.3',                753,      True),
    Version('1.16.4-pre1',           PRE | 1,  True),
    Version('1.16.4-pre2',           PRE | 2,  True),
    Version('1.16.4-rc1',            PRE | 3,  True),
    Version('1.16.4',                754,      True),
    Version('20w45a',                PRE | 5,  True),
    Version('20w46a',                PRE | 6,  True),
    Version('20w48a',                PRE | 7,  True),
    Version('20w49a',                PRE | 8,  False),
    Version('20w51a',                PRE | 9,  False),
    Version('1.16.5',                754,      True),
    Version('21w03a',                PRE | 11, False),
    Version('21w05a',                PRE | 12, False),
    Version('21w05b',                PRE | 13, False),
    Version('21w06a',                PRE | 14, False),
    Version('21w07a',                PRE | 15, False),
    Version('1.17-rc2',              PRE | 35, False),
    Version('1.17',                  755,      True),
    Version('1.17.1',                756,      True),
    Version('21w44a',                PRE | 48, False),
    Version('1.18-rc4',              PRE | 60, False),
    Version('1.18',                  757,      True),
    Version('1.18.1',                757,      True),
]

# An OrderedDict mapping the id string of each known Minecraft version to its
# protocol version number, in chronological order of release.
KNOWN_MINECRAFT_VERSIONS = OrderedDict()

# As KNOWN_MINECRAFT_VERSIONS, but only contains versions supported by pyCraft.
SUPPORTED_MINECRAFT_VERSIONS = OrderedDict()

# As SUPPORTED_MINECRAFT_VERSIONS, but only contains release versions.
RELEASE_MINECRAFT_VERSIONS = OrderedDict()

# A list of the protocol version numbers in KNOWN_MINECRAFT_VERSIONS
# in the same order (chronological) but without duplicates.
KNOWN_PROTOCOL_VERSIONS = []

# A list of the protocol version numbers in SUPPORTED_MINECRAFT_VERSIONS
# in the same order (chronological) but without duplicates.
SUPPORTED_PROTOCOL_VERSIONS = []

# A list of the protocol version numbers in RELEASE_MINECRAFT_VERSIONS
# in the same order (chronological) but without duplicates.
RELEASE_PROTOCOL_VERSIONS = []

# A dict mapping each protocol version number in KNOWN_PROTOCOL_VERSIONS to
# its index within this list (used for efficient comparison of protocol
# versions according to chronological release order).
PROTOCOL_VERSION_INDICES = {}


def initglobals(use_known_records=False):
    '''Initialise the above global variables, using
       'SUPPORTED_MINECRAFT_VERSIONS' as the source if 'use_known_records' is
       False (for backward compatibility, this is the default behaviour), or
       otherwise using 'KNOWN_MINECRAFT_VERSION_RECORDS' as the source.

       This allows 'SUPPORTED_MINECRAFT_VERSIONS' or, respectively,
       'KNOWN_MINECRAFT_VERSION_RECORDS' to be updated by the library user
       during runtime and then the derived data to be updated as well, to allow
       for dynamic version support. All updates are done by reference to allow
       this to work elsewhere in the code.
    '''
    if use_known_records:
        # Update the variables that depend on KNOWN_MINECRAFT_VERSION_RECORDS.
        KNOWN_MINECRAFT_VERSIONS.clear()
        KNOWN_PROTOCOL_VERSIONS.clear()
        SUPPORTED_MINECRAFT_VERSIONS.clear()
        PROTOCOL_VERSION_INDICES.clear()
        for version in KNOWN_MINECRAFT_VERSION_RECORDS:
            KNOWN_MINECRAFT_VERSIONS[version.id] = version.protocol
            if version.protocol not in KNOWN_PROTOCOL_VERSIONS:
                PROTOCOL_VERSION_INDICES[version.protocol] \
                    = len(KNOWN_PROTOCOL_VERSIONS)
                KNOWN_PROTOCOL_VERSIONS.append(version.protocol)
            if version.supported:
                SUPPORTED_MINECRAFT_VERSIONS[version.id] = version.protocol

    # Update the variables that depend on SUPPORTED_MINECRAFT_VERSIONS.
    SUPPORTED_PROTOCOL_VERSIONS.clear()
    RELEASE_MINECRAFT_VERSIONS.clear()
    RELEASE_PROTOCOL_VERSIONS.clear()
    for (version_id, protocol) in SUPPORTED_MINECRAFT_VERSIONS.items():
        if re.match(r'\d+(\.\d+)+$', version_id):
            RELEASE_MINECRAFT_VERSIONS[version_id] = protocol
            if protocol not in RELEASE_PROTOCOL_VERSIONS:
                RELEASE_PROTOCOL_VERSIONS.append(protocol)
        if protocol not in SUPPORTED_PROTOCOL_VERSIONS:
            SUPPORTED_PROTOCOL_VERSIONS.append(protocol)


initglobals(use_known_records=True)
