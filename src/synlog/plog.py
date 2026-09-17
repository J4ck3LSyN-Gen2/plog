import sys, logging, json, time
from typing import Optional, Any
from pathlib import Path
__version__="1.1.0";__author__="J4ck3LSyN"
class C:
    R, G, Y, B, M, C_C, W, K = "\x1b[31m", "\x1b[32m", "\x1b[33m", "\x1b[34m", "\x1b[35m", "\x1b[36m", "\x1b[37m", "\x1b[30m"
    BR, BG, BY, BB, BM, BC, BW, BK = "\x1b[91m", "\x1b[92m", "\x1b[93m", "\x1b[94m", "\x1b[95m", "\x1b[96m", "\x1b[97m", "\x1b[90m"
    BG_R, BG_G, BG_Y, BG_B, BG_M, BG_C, BG_W, BG_K = "\x1b[41m", "\x1b[42m", "\x1b[43m", "\x1b[44m", "\x1b[45m", "\x1b[46m", "\x1b[47m", "\x1b[40m"
    BOLD, DIM, UL, RST = "\x1b[1m", "\x1b[2m", "\x1b[4m", "\x1b[0m"

class FMTTIMES:
    MINIMAL = "%M:%S"
    NORMAL = "%H:%M:%S"
    FULL = "%Y-%m-%d %H:%M:%S"

class PLogFormatter(logging.Formatter):
    CMAP = {logging.DEBUG: C.BK + C.BOLD,logging.INFO: C.BB + C.BOLD,logging.WARNING: C.BY + C.BOLD,logging.ERROR: C.BR + C.BOLD,logging.CRITICAL: C.BG_R + C.BW + C.BOLD,}
    FMT = f"{C.BK}%(asctime)s{C.RST} %(levelcolor)s%(levelname)-8s{C.RST} {C.BC}%(name)s{C.RST} %(message)s"
    RFMT = "%(asctime)s [%(levelname)s] %(name)s: %(message)s"
    def __init__(self, itty: bool = True, datefmt: Optional[str] = "normal"):
        mapped = {
            "normal": FMTTIMES.NORMAL,
            "full": FMTTIMES.FULL,
            "minimal": FMTTIMES.MINIMAL,
        }['normal']
        super().__init__(fmt=self.FMT if itty else self.RFMT, datefmt=mapped)
        self.itty = itty

    def format(self, record):
        if not self.itty:
            return logging.Formatter(self.RFMT, self.datefmt).format(record)
        record.levelcolor = self.CMAP.get(record.levelno, C.RST)
        return logging.Formatter(self.FMT, self.datefmt).format(record)


class RBH(logging.Handler):
    def __init__(self, fmtType: Optional[str] = "full"):
        super().__init__()
        self.fmtType = fmtType if fmtType else "full"
        self.records = []

    def emit(self, record):
        self.records.append({
            "timestamp": time.strftime(self._gtimestamp(), time.localtime(record.created)),
            "level": record.levelname,
            "levelno": record.levelno,
            "logger": record.name,
            "message": record.getMessage(),})

    def _gtimestamp(self, fmtType: Optional[str] = None):
        if not fmtType:
            fmtType = self.fmtType
        if fmtType == "full":
            return FMTTIMES.FULL
        if fmtType == "normal":
            return FMTTIMES.NORMAL
        if fmtType == "minimal":
            return FMTTIMES.MINIMAL
        return FMTTIMES.NORMAL


class plog:
    LMAP = {
        0: logging.DEBUG,
        "d": logging.DEBUG,
        1: logging.INFO,
        "i": logging.INFO,
        2: logging.WARNING,
        "w": logging.WARNING,
        3: logging.ERROR,
        "r": logging.ERROR,
        4: logging.CRITICAL,
        "c": logging.CRITICAL,
    }
    PMAP = {
        1: f"{C.BG}[*]{C.RST} ",
        2: f"{C.BY}[!]{C.RST} ",
        3: f"{C.BR}[-]{C.RST} ",
        4: f"{C.BG_R}{C.BW}[CRIT]{C.RST} ",
        "output": f"{C.BM}[^]{C.RST} ",
    }
    def __init__(self, lname: str, verbosity: bool = True, llvl: int = logging.DEBUG):
        self._verb = verbosity
        self._name = str(lname)
        self.logger = logging.getLogger(str(self._name))
        self.logger.setLevel(llvl)
        self.logger.propagate = False
        self.logger.handlers.clear()
        self.chandle = logging.StreamHandler(sys.stdout)
        self.chandle.setFormatter(PLogFormatter(itty=sys.stdout.isatty()))
        self.chandle.setLevel(logging.INFO if self._verb else logging.CRITICAL + 1)
        self.logger.addHandler(self.chandle)
        self.bhandle = RBH()
        self.logger.addHandler(self.bhandle)

    @property
    def verbosity(self):
        return self._verb

    @verbosity.setter
    def verbosity(self, state: bool):
        self._verb = state
        self.chandle.setLevel(logging.INFO if state else logging.CRITICAL + 1)

    def count(self):
        return len(self.bhandle.records)

    def isingle(self,idx:int):
        records=list(self.bhandle.records)
        if idx < 0 or idx >= len(records):
            raise ValueError(f"(plog.index(idx={idx})) - idx:`{idx}` > length of records ({len(records)}) || idx:`{idx}` < 0")
        return records[idx]

    def irange(self,max:int|str,min:int=0):
        records = list(self.bhandle.records)
        min = int(min)
        if min < 0 or min > len(records):
            raise ValueError(f"(plog.irange(max={max},min={min})) - min:`{min}` < 0 || min:`{min}` > length of records ({len(records)})")
        if isinstance(max, str):
            if max == "...":
                end = len(records)
            elif max == "..":
                end = len(records) // 2
            elif max == ".":
                end = 3 if len(records) > 3 else 1
            else:
                raise ValueError(f"(plog.irange(max={max},min={min})) - max:`{max}(str)` was invalid, expected [ '.,..,...' got `{max}` ]")
        else:
            max = int(max)
            if max < 0 or max > len(records):
                raise ValueError(f"plog.irange(max={max},min={min}) - max:`{max}` < 0 || max:`{max}` > length of records ({len(records)})")
            end = max
        return records[min:end]

    def log(self, msg: str, lvl: int | str = 1, excInfo: bool = False, silent: bool = False, nolog: bool = False):
        if silent or nolog:
            return
        lvl = self.LMAP.get(lvl, logging.INFO)
        pfx = self.PMAP.get(lvl, "")
        self.logger.log(lvl, f"{pfx}{msg}", exc_info=excInfo)

    def dump(self, fp:Optional[str]=None,clear:bool=False, indent:int=2):
        records = list(self.bhandle.records)
        if fp:
            try:
                with open(fp, "w", encoding="utf-8") as fh:
                    json.dump(records, fh, indent=indent)
            except Exception as E:
                raise Exception(f"(plog.dump(fp={str(fp)},clear={clear},indent={indent})) - Unknown Exception during `dump` operation!\n\t- `{str(E.__class__.__name__)}`\n\t- `{str(E)}`")
        if clear:
            self.bhandle.records.clear()
        return records

    def dumps(self,data:dict[str,Any],indent:int=2,lvl:int|str=1):
        jtxt:list[str] = []
        try:
            pdata = {}
            for k,v in data.items():
                if isinstance(v,Path):
                    v = str(v)
                elif isinstance(v,bytes):
                    v = f"(hex:{str(v.hex())}) (Raw: {str(v.decode())})"
                pdata[k]=v
            jtxt = [f"[json]\t- {l}" for l in json.dumps(pdata,indent=indent).split("\n")]
        except json.JSONDecodeError as JI:
            raise Exception(f"(plog.dumps) - Json Decode Issue during `dumps` operation, is the input `JSON`?:\n\t- `{JI.__class__.__name__}`\n\t- `{JI}`")
        except Exception as E:
            raise Exception(f"(plog.dumps) - Unknown Exception during operation!\n\t- `{E.__class__.__name__}`\n\t- `{E}`")
        for l in jtxt:
            self.log(str(l),lvl=lvl)
        return (data,jtxt)
