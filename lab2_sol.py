def ex0(n):
    return n*(n+1)//2

#print(ex0(10))

def ex1(arg, nr):
    for char in range(ord(arg), ord(arg) + nr):
        print('{:x}'.format(char))

#ex1('0', 10)
#ex1('a', 26)
#ex1('A', 26)

def ex2(list):
    output = " ".join(str(bin(n))[2:].rjust(8, '0') for n in list) 
    return output, output.count('0'), output.count('1') 

#print(ex2([0,1,2,3,4])) 


def ex3(dividend = 12, divisor = 5):
    output = []
    remainder = dividend % divisor

    for i in range(100):
        quotient = (remainder * 10) // divisor
        output.append(str(quotient))
        remainder = (remainder * 10) % divisor

    print(f"{dividend//divisor}.{''.join(output)}")


#ex3(12, 5)

def ex6(alp, p, n):

        permutation = [alp[i % len(alp)] for i in range((n-1), (n-1) + p)]
        return ''.join(permutation)

#print(ex6("abc", 3, 2))

def printMatrix(matrix):
    for i in range(len(matrix)):
            print(matrix[i])

def ex7(matrix):
    for i in range(len(matrix)):
        output_matrix = []
        for j in range(len(matrix[0])):
            line = [int(k) for k in "".join(bin(matrix[i][j])[2:].rjust(8, '0'))]
            output_matrix.append(line)
        
        printMatrix(output_matrix)
        print()

'''
ex7([[0x00, 0x00, 0xFC, 0x66, 0x66, 0x66, 0x7C, 0x60, 0x60, 0x60, 0x60, 0xF0, 0x00, 0x00, 0x00, 0x00],
   [0x00, 0x00, 0x00, 0x00, 0x00, 0xC6, 0xC6, 0xC6, 0xC6, 0xC6, 0xC6, 0x7E, 0x06, 0x0C, 0xF8, 0x00],
   [0x00, 0x00, 0x10, 0x30, 0x30, 0xFC, 0x30, 0x30, 0x30, 0x30, 0x36, 0x1C, 0x00, 0x00, 0x00, 0x00],
   [0x00, 0x00, 0xE0, 0x60, 0x60, 0x6C, 0x76, 0x66, 0x66, 0x66, 0x66, 0xE6, 0x00, 0x00, 0x00, 0x00],
   [0x00, 0x00, 0x00, 0x00, 0x00, 0x7C, 0xC6, 0xC6, 0xC6, 0xC6, 0xC6, 0x7C, 0x00, 0x00, 0x00, 0x00],
   [0x00, 0x00, 0x00, 0x00, 0x00, 0xDC, 0x66, 0x66, 0x66, 0x66, 0x66, 0x66, 0x00, 0x00, 0x00, 0x00]])
'''

def ex8(Y):
    points = []
    y_size = len(Y)
    for i in range(y_size):
        points.append([i, Y[i]])
    points.append([y_size-1, 0])
    area = 0
    for i in range(len(points) - 1):
        area += points[i][0]*points[i+1][1] - points[i][1]*points[i+1][0]
    return abs(area)/2

#print(ex8([6,6,6,6,7,8,9,9,9,8,12,14,13,9,8,8,8,4,3,3,3]))




