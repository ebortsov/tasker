class NoUpdateError(Exception):
    def __init__(self):
        super().__init__("The database query didn't change anything")

