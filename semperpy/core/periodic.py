from semperpy.core.date import Date

# should this be a function?
class Periodic(object):

    def __init__(self, hourly=0, daily=0, monthly=0, yearly=0):
        self.yearly = yearly
        self.monthly = monthly
        self.daily = daily
        self.hourly = hourly
        # extend for specific hours?
