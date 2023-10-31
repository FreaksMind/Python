def ex1(a, b):
    intersection = set(a) & set(b)
    union = set(a) | set(b)
    difference_a_b = set(a) - set(b)
    difference_b_a = set(b) - set(a)

    result = [intersection, union, difference_a_b, difference_b_a]
    return result

def ex2(string):
    char_count = {}

    for char in string:
        if char in char_count:
            char_count[char] += 1
        else:
            char_count[char] = 1

    return char_count

def ex3(dict1, dict2):

    if type(dict1) is not dict or type(dict2) is not dict:
        return False

    if len(dict1) != len(dict2):
        return False

    for key, value1 in dict1.items():
        if key not in dict2:
            return False
        value2 = dict2[key]
        
        if isinstance(value1, dict) and isinstance(value2, dict):
            if not ex3(value1, value2):
                return False
        else:
            if value1 != value2:
                return False

    return True

def ex4(tag, content, **elements):
    attributes = " ".join(f"{k} = \"{v}\\\"" for k, v in elements.items())
    return f"<{tag} {attributes}> {content}"

def ex6(a_list):

    a = 0
    b = set()
    for l in a_list:
        if a_list.count(l) == 1:
            a += 1
        elif a_list.count(l) > 1:
            b.add(l)
    return (a, len(b))

def ex10(mapping):
    result = []
    visited = set()
    current_key = "start"

    while current_key in mapping and current_key not in visited:
        visited.add(current_key)
        result.append(mapping[current_key])
        current_key = mapping[current_key]

    return result

def ex11(*args, **kwargs):
    values = set(kwargs.values())
    count = sum(1 for arg in args if arg in values)
    return count