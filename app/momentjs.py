from jinja2 import Markup
from datetime import datetime, timedelta

class momentjs(object):
    def __init__(self, timestamp):
        # need to adjust for database being in EST
      #  self.timestamp = timestamp+timedelta(hours=4)
        self.timestamp = timestamp

    def render(self, format):
        return Markup(
            "<script>\ndocument.write(moment(\"%s\").%s);\n</script>" %
            (self.timestamp.strftime("%Y-%m-%dT%H:%M:%S Z"), format))

    def format(self, fmt):
        return self.render("format(\"%s\")" % fmt)

    def calendar(self):
        return self.render("calendar()")

    def fromNow(self):
        return self.render("fromNow()")

    def __call__(self, *args):
        return self.format(*args)
