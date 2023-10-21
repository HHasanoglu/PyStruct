class Section:
    """
    A class to represent the cross-sectional Properties of a frame and truss element.

    Attributes:
        area (float): Cross-sectional area of the truss element.
    """

    def __init__(self, area: float):
        """
        Initialize a new Area instance.

        Args:
            area (float): Cross-sectional area of the truss element.
        """
        self.area = area