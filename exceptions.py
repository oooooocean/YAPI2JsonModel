
class SimpleError(Exception):
    def __init__(self, description):
        self.description = description

    def __str__(self):
        return self.description


class ParseError(SimpleError):
    """
    解析异常
    """
    pass


class ReptileError(ParseError):
    """
    爬虫异常
    """
    pass
