class ImprobableError(Exception):
    """
    Error to call when something highly improbable happens
    """
    def __init__(self, message):
        self.message = message
