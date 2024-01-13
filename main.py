from PB_galois_field import *


def main():
    str1 = "1101010110010010101100100110100111011001101001011000101110101011001001010110101100100110110101111"
    str2 = "1010101100110010110011101001100101101111101010110100101110010100100011100011011010111100101"
    str3 = "1111001010110111011001111000101011101101100111110101001001000100010110101100110010100100101010101"
    f_el1 = PolynomialBaseFieldElement(str1)
    f_el2 = PolynomialBaseFieldElement(str2)
    f_el3 = PolynomialBaseFieldElement(str3)
    print(f_el1.__str__())
    print(f_el2.__str__())
    print(f_el1.add(f_el2))
    print(f_el2.mult(f_el1))
    print(f_el1.square())
    print(f_el1.inverse())
    print(f_el1.trace())
    print(f_el1.power(f_el3))


if __name__ == '__main__':
    main()

