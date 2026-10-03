import re
def bbox(d):
    """피그마/fontTools SVG path(d) 의 대략 bbox (절대좌표 M L C Q H V Z)"""
    xs, ys = [], []; cx = cy = 0
    for cmd, args in re.findall(r'([MLCQHVZmlcqhvz])([^MLCQHVZmlcqhvz]*)', d):
        n = list(map(float, re.findall(r'-?\d*\.?\d+(?:e-?\d+)?', args)))
        if cmd in 'MLCQ':
            for i in range(0, len(n) - 1, 2): xs.append(n[i]); ys.append(n[i+1])
            if n: cx, cy = n[-2], n[-1]
        elif cmd == 'H':
            for v in n: xs.append(v); cx = v
            ys.append(cy)
        elif cmd == 'V':
            for v in n: ys.append(v); cy = v
            xs.append(cx)
    return min(xs), min(ys), max(xs), max(ys)
