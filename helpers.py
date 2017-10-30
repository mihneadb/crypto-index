def truncate(x, num_decimals):
    factor = 10 ** num_decimals
    return int(x * factor) / float(factor)
