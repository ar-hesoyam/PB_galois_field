# in first variant polynomial generator is x^163 + x^7 + x^6 + x^3 + 1; field = GF(2^163)


class PolynomialBaseFieldElement:
    __field_power = 163
    __generator = [0] * 164
    __generator[163 - 0], __generator[163 - 3], __generator[163 - 6], __generator[163 - 7], __generator[163 - 163] = 1, 1, 1, 1, 1

    def __init__(self, vector):
        if type(vector) == str:
            vector = list(map(int, vector))
        if len(vector) == 163:
            self.vector = vector
            self.degree = self.__get_degree()
        elif len(vector) < 163:
            while len(vector) != 163:
                vector.insert(0, 0)
            self.vector = vector
            self.degree = self.__get_degree()
        elif len(vector) > 163:
            self.vector = [0] * 163
            self.degree = 0

    def __get_degree(self):
        for i in range(0, len(self.vector)):
            if self.vector[i] != 0:
                return len(self.vector) - i - 1
        return 0

    def add(self, another_element):
        another_vector = [0] * 163
        for i in range(163):
            another_vector[i] = another_element.vector[i] ^ self.vector[i]
        return PolynomialBaseFieldElement(another_vector)

    @staticmethod
    def mult_vectors(vector, i):  # works as << shift
        vector = vector + [0] * i
        return vector

    @staticmethod
    def add_vectors(vector1, vector2):
        res_vector = [0]*max(len(vector1), len(vector2))
        if len(vector1) < len(vector2):
            vector1 = [0]*abs(len(vector1) - len(vector2)) + vector1
        if len(vector2) < len(vector1):
            vector2 = [0]*abs(len(vector1) - len(vector2)) + vector2
        for i in range(len(res_vector)):
            res_vector[i] = vector1[i] ^ vector2[i]
        return res_vector

    def mult(self, another_element):
        new_vector_degree = self.degree + another_element.degree
        if new_vector_degree >= 163:
            vector = [0] * new_vector_degree
        else:
            vector = [0] * 163
        vector = self.add_vectors(vector, self.vector)
        for i in range(len(another_element.vector)):
            if another_element.vector[i] == 1:
                vector = self.add_vectors(vector, self.mult_vectors(self.vector, len(another_element.vector) - i - 1))
        vector = self.add_vectors(vector, self.vector)
        return PolynomialBaseFieldElement(self.__mod(vector))

    @staticmethod
    def __mod(vector):
        m_degree = 163
        try:
            index_of_1 = vector.index(1)
            f_degree = len(vector) - index_of_1 - 1
        except ValueError:
            f_degree = 0
        while f_degree >= m_degree:
            vector = PolynomialBaseFieldElement.add_vectors(vector, PolynomialBaseFieldElement.mult_vectors(PolynomialBaseFieldElement.__generator, f_degree - m_degree))
            try:
                index_of_1 = vector.index(1)
                f_degree = len(vector) - index_of_1 - 1
            except ValueError:
                f_degree = 0
        return vector[len(vector)-163:]

    def square(self):
        return self.mult(self)

    @staticmethod
    def get_zero():
        return PolynomialBaseFieldElement([0]*163)

    @staticmethod
    def get_one():
        one = [0]*163
        one[162] = 1
        return PolynomialBaseFieldElement(one)

    def trace(self):
        result = self
        current = self
        for i in range(1, self.__field_power):
            current = current.square()
            result = result.add(current)
        return result

    def power(self, c):
        result = self.get_one()
        for i in range(0, len(c.vector) - 1):
            if c.vector[i] == 1:
                result = result.mult(self)
            result = result.square()
        if c.vector[len(c.vector) - 1] == 1:
            result = result.mult(self)
        return result

    def inverse(self):
        result = PolynomialBaseFieldElement.get_one()
        for i in range(1, self.__field_power):
            result = result.mult(self)
            result = result.square()
        return result

    def __str__(self):
        return "".join(map(str, self.vector[self.vector.index(1):]))
