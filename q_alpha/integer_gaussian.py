class IntegerGaussian:
    """
    Represents a Gaussian integer (a + bj) where a and b are Python integers.
    'j' is used as the symbol for the imaginary unit sqrt(-1) in string representation.
    """
    def __init__(self, real: int, imag: int):
        if not isinstance(real, int) or not isinstance(imag, int):
            raise TypeError("Real and imaginary parts of an IntegerGaussian must be integers.")
        self.real = real
        self.imag = imag

    def __add__(self, other):
        if not isinstance(other, IntegerGaussian):
            return NotImplemented
        return IntegerGaussian(self.real + other.real, self.imag + other.imag)

    def __sub__(self, other):
        if not isinstance(other, IntegerGaussian):
            return NotImplemented
        return IntegerGaussian(self.real - other.real, self.imag - other.imag)

    def __mul__(self, other):
        if isinstance(other, int): # Scalar multiplication
            return IntegerGaussian(self.real * other, self.imag * other)
        if not isinstance(other, IntegerGaussian):
            return NotImplemented
        # (a+bj)(c+dj) = (ac-bd) + (ad+bc)j
        real_part = self.real * other.real - self.imag * other.imag
        imag_part = self.real * other.imag + self.imag * other.real
        return IntegerGaussian(real_part, imag_part)

    def __rmul__(self, other):
        if isinstance(other, int):
            return self.__mul__(other)
        return NotImplemented

    def __neg__(self):
        return IntegerGaussian(-self.real, -self.imag)

    def __eq__(self, other):
        if not isinstance(other, IntegerGaussian):
            return False
        return self.real == other.real and self.imag == other.imag

    def __str__(self):
        if self.imag == 0:
            return str(self.real)
        elif self.real == 0:
            if self.imag == 1:
                return "j"
            elif self.imag == -1:
                return "-j"
            else:
                return f"{self.imag}j"
        else:
            sign = "+" if self.imag > 0 else "-"
            abs_imag = abs(self.imag)
            imag_str = f"{abs_imag}j" if abs_imag != 1 else "j"
            return f"{self.real}{sign}{imag_str}"

    def __repr__(self):
        return f"IntegerGaussian({self.real}, {self.imag})"
