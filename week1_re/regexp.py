def calculate(data, findall):
    matches = findall(r"([abc]{1})([\-\+]?)=([abc]?)([\-\+]?)(\d{0,})")
    for match in matches:
        v1, s, v2 = match[0], match[1], match[2]
        n = -1 * int(match[4] or 0) if match[3] == '-' else int(match[4] or 0)
        if s == '':
            data[v1] = data.get(v2, 0) + n
        else:
            sign = 1 if s == '+' else -1
            data[v1] = data.get(v1, 0) + sign * (data.get(v2, 0) + n)
    return data
