def convert_px_to_minute(px_x: int, px_y: int) -> int:
    """Convert background-position arguments from the "sb-sprite-uhr-klein"
    CSS class to the game minute.

    This CSS class uses some smartness that moves the this image around so as
    to choose the game minutes
    https://tmssl.akamaized.net/images/spielbericht/sb-sprite-uhr-k.png

    This function has been taken from the `transfermarkt-scraper` repository.
    You can find the repo here -> https://github.com/dcaribou/transfermarkt-scraper/tree/main

    Args:
        px_x (int): X position in pixels
        px_y (int): Y position in pixels

    Returns:
        int: game minute
    """

    n = 10  # number of columns in the matrix
    m = 13  # number of rows in the matrix
    h = 36  # size of the chronometer square in pixels

    x_offset = 0
    y_offset = 0

    matrix = [list(range((a - 1) * n + 1, a * n + 1)) for a in range(1, m)]

    if abs(px_y) > h * (m - 1 - y_offset):  # no data available
        return -1

    x = abs(px_x) / h
    assert x.is_integer()
    x = int(x) + x_offset

    y = abs(px_y) / h
    assert y.is_integer()
    y = int(y) + y_offset

    return matrix[y][x]
