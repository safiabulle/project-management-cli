class Person:
    """
    Base class for people in the system.
    """

    def __init__(self, name):
        self.name = name

    def __str__(self):
        return self.name