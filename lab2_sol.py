
def ex3(list_a, list_b):
    intersection = list(set(list_a) & set(list_b))
    union = list(set(list_a) | set(list_b))
    a_minus_b = list(set(list_a) - set(list_b))
    b_minus_a = list(set(list_b) - set(list_a))

    return (intersection, union, a_minus_b, b_minus_a)

print(ex3([1,2,56,3,6], [3,2,7,3,7,8,2]))

def printMatrix(matrix):
    for i in range(len(matrix)):
        for j in range(len(matrix[0])):
           print(matrix[i][j], end= " ")
        print()


def ex5(matrix):
    for i in range(len(matrix)):
        for j in range(len(matrix[0])):
            if(i == j and i < len(matrix)-1):
                matrix[i+1][j] = 0

    printMatrix(matrix)

matrix = [
    [1, 2, 3],
    [4, 5, 6],
    [7, 8, 9],
]

ex5(matrix)

def ex2(list):
    output_list = []
    for i in range(len(list)):
        prime = True
        for j in range(2, list[i]):
            if list[i] % j == 0:
                prime = False
        if prime:
            output_list.append(list[i])
    return output_list

print(ex2([1,2,3,4,5,6,7,8,9]))

def ex6(*lists, x):
    counter = {}
    for list in lists:
        for item in list:
            if item in counter:
                counter[item] += 1
            else:
                counter[item] = 1

    output = [item for item, count in counter.items() if count == x]

    return output
    
print(ex6([2,6],[2,7],[3,7,7,7,7], x=5))

def ex7(list):
    nrPalindroms = 0
    longestIndex = 0
    longestSize = -1
    for i in range(len(list)):
        if str(list[i]) == str(list[i])[::-1]:
            if len(str(list[i])) > longestSize:
                   longestSize = len(str(list[i]))
                   longestIndex = i
            nrPalindroms += 1


    return (nrPalindroms, list[longestIndex])

print(ex7([12,425, 13331, 1221]))

def ex11(tuples):
    return sorted(tuples, key = lambda x: x[1][2])

print(ex11([('abc', 'bcd'), ('abc', 'zza')]))

def ex10(*lists):
    lists_zip = zip(*lists)
    output = [tuple(tup) for tup in lists_zip]
    return output

print(ex10([1,2,3], [5,6,7], ["a", "b", "c"]))
