class Hex:
    """
    Holds the HEX colors

    References:
    - https://stackoverflow.com/questions/29643352/converting-hex-to-rgb-value-in-python
    - https://www.delftstack.com/howto/python/python-hex-to-rgb/
    """

    def __init__(self, hex_string):
        self.hex_string = self.standard_hex_string(hex_string)

    @staticmethod
    def standard_hex_string(hex_string):
        if not isinstance(hex_string, str):
            raise TypeError(f"hex_string has to be a string; {hex_string}")
        if hex_string.startswith("#"):
            hex_string = hex_string[1:]
        if len(hex_string) != 6:
            raise ValueError(f"hex_string has to be 6 characters long; {hex_string}")

        return f"{hex_string}"

    @property
    def hex(self):
        return self.hex_string

    @property
    def rgb(self):
        r_g_b = tuple([int(self.hex[i : i + 2], 16) for i in (0, 2, 4)])

        return r_g_b

    def __str__(self) -> str:
        return f"hex: #{self.hex}; rgb: {self.rgb}"
