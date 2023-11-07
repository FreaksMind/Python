class Stack:

    def __init__(self):
        self.stack = []
        self.stack_size = 0

    def size(self):
        return self.stack_size

    def empty(self):
        if len(self.stack) == 0:
            return True
        return False

    def push(self, element):
        self.stack += [element]
        self.stack_size += 1

    def pop(self):
        if not self.empty():
            last_elem = self.stack[-1]
            self.stack = self.stack[:-1]
            self.stack_size -= 1
            return last_elem
        return None

    def peek(self):
        if not self.empty():
            return self.stack[-1]
        return None

    def __eq__(self, other_object):
        return self.stack == other_object

    def __str__(self):
        return "\n".join(str(x) for x in self.stack[::-1])
    
class Queue:

    def __init__(self):
        self.queue = []
        self.queue_size = 0

    def size(self):
        return self.queue_size

    def empty(self):
        if len(self.queue) == 0:
            return True
        return False

    def push(self, element):
        self.queue[:0] = [element]
        self.queue_size += 1

    def pop(self):
        if not self.empty():
            last_elem = self.queue[0]
            self.queue = self.queue[1:]
            self.queue_size -= 1
            return last_elem
        return None

    def peek(self):
        if not self.empty():
            return self.queue[0]
        return None

    def __eq__(self, other_object):
        return self.queue == other_object

    def __str__(self):
        return " ".join(str(x) for x in self.queue)
    
class Matrix:
    def __init__(self, N, M) -> None:
        self.N = N
        self.M = M
        self.matrix = []

        for i in range(N):
            row = []
            for j in range(M):
                row.append(0)
            self.matrix.append(row)

    def set(self, row, col, value):
        self.matrix[row][col] = value

    def get(self, row, col):
        return self.matrix[row][col]
    
    def transpose(self):
        transpose = Matrix(self.N, self.M)
        for i in range (self.N):
            for j in range(self.M):
                transpose.set(j, i, self.get(i, j))
        return transpose


    def __str__(self):
        output = ""
        for i in range(self.N):
            for j in range(self.M):
                output += str(self.matrix[i][j]) + " "
            output += "\n"
        return output

    def __eq__(self, other_matrix):
        return self.matrix == other_matrix