import datetime as dt
from dateutil import easter

# Weekend Function


def is_weekend(d: dt.date) -> bool:
    if (d.weekday() - 5) < 0:
        return False
    return True


def is_weekday(d) -> bool:
    if is_weekend(d) == True:
        return False


def is_holiday_brl(d) -> bool:
    yy = d.year
    mm = d.month
    dd = d.day

    if mm >= 8:
        if(
            ((mm == 9) and (dd == 7))
            or
            ((mm == 10) and (dd == 12))
            or
            ((mm == 11) and (dd == 2))
            or
            ((mm == 11) and (dd == 15))
            or
            ((mm == 12) and (dd == 25))
        ):
            return True
    else:
        if(
            ((mm == 1) and (dd == 1))
            or
            ((mm == 4) and (dd == 21))
            or
            ((mm == 5) and (dd == 1))
        ):
            return True

        dt_est = d
        e_est = easter.easter(yy)

        if(
            ((e_est - dt.timedelta(48) <= dt_est <= e_est-dt.timedelta(47)))
            or
            (dt_est == (e_est + dt.timedelta(60)))
            or
            (dt_est == (e_est - dt.timedelta(2)))

        ):
            return True
    return False


def is_holiday_B3(d) -> bool:

    yy = d.year
    mm = d.month
    dd = d.day

    if (
        (mm == 1 and dd == 25 and yy <= 2021)
        or
        (mm == 7 and dd == 9 and yy < 2020)
        or
        (yy >= 2007 and mm == 11 and dd == 20 and yy < 2020)
        or
        (mm == 12 and dd == 24)
        or
        (mm == 12 and (dd == 31 or (dd >= 29 and d.weekday() == 4)))
        or
            is_holiday_brl(d)):
        return True
    return False
