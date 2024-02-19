from dataclasses import dataclass
from typing import Tuple


@dataclass
class AyahInfo:
    sura: int
    ayah: int


VERSES_BY_RAMADAN_NIGHT = [
    (AyahInfo(sura=1, ayah=1), AyahInfo(sura=2, ayah=203)),
    (AyahInfo(sura=2, ayah=204), AyahInfo(sura=3, ayah=91)),
    (AyahInfo(sura=3, ayah=92), AyahInfo(sura=4, ayah=87)),
    (AyahInfo(sura=4, ayah=88), AyahInfo(sura=5, ayah=82)),
    (AyahInfo(sura=5, ayah=83), AyahInfo(sura=7, ayah=11)),
    (AyahInfo(sura=7, ayah=12), AyahInfo(sura=8, ayah=40)),
    (AyahInfo(sura=8, ayah=41), AyahInfo(sura=9, ayah=93)),
    (AyahInfo(sura=9, ayah=94), AyahInfo(sura=11, ayah=5)),
    (AyahInfo(sura=11, ayah=6), AyahInfo(sura=12, ayah=52)),
    (AyahInfo(sura=12, ayah=53), AyahInfo(sura=14, ayah=52)),
    (AyahInfo(sura=15, ayah=1), AyahInfo(sura=16, ayah=128)),
    (AyahInfo(sura=17, ayah=1), AyahInfo(sura=18, ayah=74)),
    (AyahInfo(sura=18, ayah=75), AyahInfo(sura=20, ayah=135)),
    (AyahInfo(sura=21, ayah=1), AyahInfo(sura=22, ayah=78)),
    (AyahInfo(sura=23, ayah=1), AyahInfo(sura=25, ayah=20)),
    (AyahInfo(sura=25, ayah=21), AyahInfo(sura=27, ayah=59)),
    (AyahInfo(sura=27, ayah=60), AyahInfo(sura=29, ayah=44)),
    (AyahInfo(sura=29, ayah=45), AyahInfo(sura=33, ayah=30)),
    (AyahInfo(sura=33, ayah=31), AyahInfo(sura=36, ayah=21)),
    (AyahInfo(sura=36, ayah=22), AyahInfo(sura=39, ayah=31)),
    (AyahInfo(sura=39, ayah=32), AyahInfo(sura=41, ayah=46)),
    (AyahInfo(sura=41, ayah=47), AyahInfo(sura=45, ayah=37)),
    (AyahInfo(sura=46, ayah=1), AyahInfo(sura=51, ayah=30)),
    (AyahInfo(sura=51, ayah=31), AyahInfo(sura=57, ayah=29)),
    (AyahInfo(sura=58, ayah=1), AyahInfo(sura=66, ayah=12)),
    (AyahInfo(sura=67, ayah=1), AyahInfo(sura=77, ayah=50)),
    (AyahInfo(sura=78, ayah=1), AyahInfo(sura=114, ayah=6)),
]


def get_start_end_ayah_by_night(night: int) -> Tuple[AyahInfo]:
    return VERSES_BY_RAMADAN_NIGHT[(night - 1) % 27]
