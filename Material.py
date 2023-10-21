class Material:
    """
    A class to represent the material properties of a truss element.

    Attributes:
        youngs_modulus (float): Young's Modulus of the material.
    """

    def __init__(self, youngs_modulus: float):
        """
        Initialize a new Material instance.

        Args:
            youngs_modulus (float): Young's Modulus of the material.
        """
        self.youngs_modulus = youngs_modulus