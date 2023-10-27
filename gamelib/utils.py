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
