def next_power_of_two(x):
    i = 0
    while (1 << i) <= x:
        i += 1
    return 1 << i


def get_percent(x):
    return "width: {}%; height: 6px;".format(
        int(x / next_power_of_two(x) * 100)
    )
