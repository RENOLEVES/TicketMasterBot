import bracex


def square_to_brace(s):
    stack = []
    s = list(s)
    for i, char in enumerate(s):
        if char == '[':
            stack.append(i)
        elif char == ']':
            start = stack.pop()
            s[start] = '{'
            s[i] = '}'
    return ''.join(s)


def expand_custom(s):
    converted = square_to_brace(s)
    return list(bracex.expand(converted))
