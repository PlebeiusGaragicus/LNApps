def lerp(a, b, t):
    """
    Linear interpolation between values a and b by an amount t.

    Parameters:
    - a (float): Start value
    - b (float): End value
    - t (float): Interpolation factor, typically between 0 and 1

    Returns:
    - float: Interpolated value
    """
    return a + (b - a) * t


# lerp but for colors:
def lerp_color(a, b, t):
    """
    Linear interpolation between colors a and b by an amount t.

    Parameters:
    - a (tuple): Start color
    - b (tuple): End color
    - t (float): Interpolation factor, typically between 0 and 1

    Returns:
    - tuple: Interpolated color
    """
    # NOTE: this is a bit of a hack, but it works
    t = max(0, min(1, t))  # Clamp t to the [0, 1] range
    return tuple([lerp(a[i], b[i], t) for i in range(len(a))])
