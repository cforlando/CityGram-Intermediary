##--Thomas Adriaan Hellinger
##--This is where we keep the constants, that's why the file is named 
##--"constants.py" (very confusing, I know).
##-2016-05-16
from enum import Enum


class TimeUnit(Enum):
    SECOND = 1
    MINUTE = 60 * SECOND
    HOUR = 60 * MINUTE
    MILLISECOND = SECOND / 10**3
    MICROSECOND = SECOND / 10**6
    NANOSECOND = SECOND / 10**9
