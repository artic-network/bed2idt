from enum import Enum

"""
These are the correct values on the IDT website as of time of writing
Please check https://eu.idtdna.com/site/order/oligoentry to confirm
"""


class PlateSize(Enum):
    WELL96 = "96"
    WELL384 = "384"


class PlateSplitBy(Enum):
    POOL = "pool"
    REF = "ref"
    REF_POOL = "ref_pool"
    NONE = "none"


class PlateFillBy(Enum):
    ROWS = "rows"
    COLS = "cols"


class TubeScale(Enum):
    NM25 = "25nm"
    NM100 = "100nm"
    NM250 = "250nm"
    UM1 = "1um"
    UM5 = "5um"
    UM10 = "10um"


class TubePurification(Enum):
    STD = "STD"
    PAGE = "PAGE"
    HPLC = "HPLC"
    IEHPLC = "IEHPLC"
    RNASE = "RNASE"
    DUALHPLC = "DUALHPLC"
    PAGEHPLC = "PAGEHPLC"
