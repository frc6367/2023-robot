def map_range(x, a, b, c, d):
    y = (x - a) / (b - a) * (d - c) + c
    return y


print(map_range(-1, -1.0, 1.0, 0.5, 0.2))
print(map_range(-0.5, -1.0, 1.0, 0.5, 0.2))
print(map_range(0, -1.0, 1.0, 0.5, 0.2))
print(map_range(0.5, -1.0, 1.0, 0.5, 0.2))
print(map_range(1, -1.0, 1.0, 0.5, 0.2))
