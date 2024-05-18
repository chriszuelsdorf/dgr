import datetime
import re


def is_valid_num(i: str, defrng):
    """Check if i is numeric, integer, and in range"""
    if not i.isnumeric():
        return False
    return int(i) in defrng


def parseelem(expr, defrng, failmsg) -> list[range]:
    """Parse the element into a list of ranges"""
    if ',' in expr:
        o = []
        for e in expr.split(','):
            o += parseelem(e, defrng, failmsg)
        return o

    ffmsg = f"{failmsg} {expr}"
    rangereg = "[0-9]+-[0-9]+"
    if expr == '*': # handles *
        return [defrng]
    elif re.match(f"^{rangereg}$", expr): # handles bare range
        p = [int(x) for x in expr.split('-')]
        if not all([is_valid_num(x, defrng) for x in p]):
            raise ValueError(ffmsg)
        return [range(p[0], p[1])]
    elif re.match(f"^*/[0-9]+$", expr): # handles */5
        p = int(expr.split('/')[1])
        if not is_valid_num(p, defrng):
            raise ValueError(ffmsg)
        return [range(defrng.start, defrng.stop, p)]
    elif re.match(f"^{rangereg}/[0-9]+$", expr): # handles 0-15/5
        p = [int(x) for x in expr.split('/')[0].split('-')]
        den = int(expr.split('/')[1])
        if not (all([is_valid_num(x, defrng) for x in p]) and is_valid_num(den, defrng)):
            raise ValueError(ffmsg)
        return [range(p[0], p[1], den)]
    raise ValueError(ffmsg)


in_any = lambda elem, l_ranges: any([elem in x for x in l_ranges])


class Cron:
    def __init__(self, expr) -> None:
        if not isinstance(expr, str):
            raise TypeError()
        el = expr.split(' ')
        if not len(el) == 5:
            raise ValueError("Need exactly 5 elements")
        self.min = parseelem(el[0], range(0, 60), "Bad minute portion")
        self.hr = parseelem(el[1], range(0, 24), "Bad hour portion")
        self.dom = parseelem(el[2], range(1, 32), "Bad day-of-month portion")
        self.domstar = el[2] == '*'
        self.mon = parseelem(el[3], range(1, 13), "Bad month portion")
        self.dow = parseelem(el[4], range(0, 7), "Bad day-of-week portion")
        self.dowstar = el[4] == '*'

    def prev(self):
        now = datetime.datetime.now(datetime.timezone.utc)
        while True:
            while not in_any(now.month, self.mon):
                now = now.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
                now = now - datetime.timedelta(minutes=1)
            
            # Update day - note that if it changed we have to make sure it didn't
            #   tick back into an ineligible month
            didit = False
            while True:
                # If neither dom nor dow is specified, it's always acceptable
                if self.domstar and self.dowstar:
                    break
                # If dom is specified and valid, it's acceptable
                if (not self.domstar) and in_any(now.day, self.dom):
                    break
                # If dow is specified and valid, it's acceptable
                if (not self.dowstar) and in_any(now.isoweekday()%7, self.dow):
                    break
                now = now.replace(hour=0, minute=0, second=0, microsecond=0)
                now = now - datetime.timedelta(minutes=1)
                didit = True
            if didit:
                continue

            # Update hour - note that if it changed we have to make sure it didn't
            #   tick back into an ineligible month or day
            didit = False
            while not in_any(now.hour, self.hr):
                now = now.replace(minute=0, second=0, microsecond=0)
                now = now - datetime.timedelta(minutes=1)
                didit = True
            if didit:
                continue

            # Update minute - note that if it changed we have to make sure it didn't
            #   tick back into an ineligible month, day, or hour
            didit = False
            while not in_any(now.minute, self.min):
                now = now.replace(second=0, microsecond=0)
                now = now - datetime.timedelta(minutes=1)
                didit = True
            if didit:
                continue

            return now
            
    def next(self):
        now = datetime.datetime.now(datetime.timezone.utc)
        while True:
            while not in_any(now.month, self.mon):
                now = now.replace(
                    month=(now.month % 12) + 1, 
                    day=1, 
                    hour=0, 
                    minute=0, 
                    second=0, 
                    microsecond=0
                )
            
            # Update day - note that if we changed it we have to make sure we 
            #   haven't ticked over into an ineligible month
            didit = False
            while True:
                # If neither dom nor dow is specified, it's always acceptable
                if self.domstar and self.dowstar:
                    break
                # If dom is specified and valid, it's acceptable
                if (not self.domstar) and in_any(now.day, self.dom):
                    break
                # If dow is specified and valid, it's acceptable
                if (not self.dowstar) and in_any(now.isoweekday() % 7, self.dow):
                    break
                now = now + datetime.timedelta(days=1)
                now = now.replace(hour=0, minute=0, second=0, microsecond=0)
                didit = True
            if didit:
                continue

            # Update hour - note that if we changed it we have to make sure we 
            #   haven't ticked over into an ineligible month or day
            didit = False
            while not in_any(now.hour, self.hr):
                now = now + datetime.timedelta(hours=1)
                now = now.replace(minute=0, second=0, microsecond=0)
                didit = True
            if didit:
                continue

            # Update minute - note that if we changed it we have to make sure we 
            #   haven't ticked over into an ineligible hour, month, or day
            didit = False
            while not in_any(now.minute, self.min):
                now = now + datetime.timedelta(minutes=1)
                now = now.replace(second=0, microsecond=0)
                didit = True
            if didit:
                continue

            return now
        
