from datetime import datetime
import re


class Helper:
    @staticmethod
    def date_format(value, format_to="%Y-%m-%d %H:%M:%S"):
        if isinstance(value, datetime):
            return value.strftime(format_to)
        else:
            return None
