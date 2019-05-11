def next_power_of_two(x):
    i = 0
    while (1 << i) <= x:
        i += 1
    return 1 << i


def format_css_percent(x):
    return "width: {}%; height: 6px;".format(x)


def get_percent(x):
    return format_css_percent(
        int(x / next_power_of_two(x) * 100 + 0.5)
    )


def get_relative_percent(value, relative_value):
    if relative_value == 0:
        percent = 100
    else:
        percent = abs(int(value * 100 / relative_value + 0.5) - 100)

    return format_css_percent(percent), "{}% {} than last month".format(
        percent, "higher" if value >= relative_value else "lower"
    )


def get_date(date):
    d, m, y = date.day, date.month, date.year
    return int(y), int(m)


def move_date_back(date, cnt_month):
    year, month = date
    month -= cnt_month
    while month <= 0:
        year -= 1
        month += 12
    return year, month


