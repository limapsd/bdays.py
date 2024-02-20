from libs.bdays.rules import *
import operator
from functools import reduce
from itertools import compress
from math import copysign


def isbd(is_holiday_):
    def _inside(dt):
        if is_weekend(dt):
            return False
        return not is_holiday_(dt)
    return _inside


def listholiday(holiday, dt0, dt1):
    list_ = np.array([dt0, dt1])
    regeln = holiday_rules(holiday)

    d0 = list_.min()
    d1 = list_.max()

    date_range = [d0 + dt.timedelta(days=j) for j in range((d1-d0).days + 1)]
    v_isholiday = [regeln(i) for i in date_range]
    return list(compress(date_range,v_isholiday))

def accumlate(iterable, func = operator.add,*, initial = None):
    'Return running totals'
    it = iter(iterable)
    total = initial
    if initial is None:
        try:
            total = next(it)
        except StopIteration:
            return
    yield total
    for element in it:
        total = func(total,element)
        yield total

def calc_bd(is_bd, d0,dn):
    
    def acc_bd(s,di):
        isbdprev,dprev,bdprev = s
        x = is_bd(di)
        inc = 1 if x else 0
        return (x,di,bdprev + inc)
    
    delta_t = map(
        lambda dt:d0 +dt,
        map(dt.timedelta,range(1,(dn-d0).days))
    )
    _acc = accumlate(
        delta_t,
        func = acc_bd,
        initial=(True,d0,0))
    return map(lambda s:s[2],_acc)



is_holiday_fs = {
    'BRL': is_holiday_brl,
    'B3':is_holiday_B3
}

d0 = dt.date(1900,1,1)
dn = dt.date(2200,12,30)

def init_bd_cache(is_hldy_list, d0, dn):
    return map(lambda c: list(calc_bd(c, d0, dn)), is_hldy_list)

is_bd_fs = dict(zip(is_holiday_fs.keys(), map(isbd, is_holiday_fs.values())))
bd_cache_map = dict(zip(is_holiday_fs.keys(), init_bd_cache(is_bd_fs.values(),d0,dn) ))

def bdays(ds,de,bd):
    s = (ds-d0).days
    e = (de-d0).days
    return bd[e] - bd[s]

def adjust_bday(d, sign, bd):
    if sign > 0:
        return adjust_bday_fwd(d,bd)
    return adjust_bday_bk(d, bd)

def adjust_bday_bk(d, bd):
    prev = d + dt.timedelta(-1)
    while bdays(prev,d, bd) == 0:
        d =prev
        prev = prev + dt.timedelta(-1)
    return max(d,d0)

def adjust_bday_fwd(d, bd):
    prev = d + dt.timedelta(-1)
    while bdays(prev,d, bd) == 0:
        prev = d
        d = d + dt.timedelta(1)
    return min(d,dn)

def ndays(ds,n,bd):
    dg = ds +dt.timedelta(days = int(n*365/252 ))
    sign = copysign(1,n)
    dg   = adjust_bday(dg,sign, bd)
    m = bdays(ds, dg, bd)
    if m ==n:
        return dg
    if abs(n-m) < abs(n):
        return ndays(dg, n-m, bd)
    else:
        raise RecursionError(f'ds:{ds}ds/dg:{dg}/n:{n}/m:{m}')

def bd_day_counters(holiday):
    bd =bd_cache_map[holiday]
    return (
        lambda d0, dn: bdays(d0,dn, bd),
        lambda ds,n: ndays(ds, n , bd)   
        )

def bd_day_adjusts(holiday):
    bd = bd_cache_map[holiday]
    return lambda d, sign : adjust_bday(d,sign,bd)