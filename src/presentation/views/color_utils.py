from enum import Enum


class Format(Enum):
    """Enum for formats in terminal."""

    NORMAL = 0
    BOLD = 1
    FAINT = 2
    ITALICS = 3
    UNDERLINED = 4


class Color(Enum):
    """Enum for colors in terminal."""

    BLACK_FOREGROUND = 30
    RED_FOREGROUND = 31
    GREEN_FOREGROUND = 32
    YELLOW_FOREGROUND = 33
    BLUE_FOREGROUND = 34
    MAGENTA_FOREGROUND = 35
    CYAN_FOREGROUND = 36
    LIGHT_GRAY_FOREGROUND = 37
    GRAY_FOREGROUND = 90
    LIGHT_RED_FOREGROUND = 91
    LIGHT_GREEN_FOREGROUND = 92
    LIGHT_YELLOW_FOREGROUND = 93
    LIGHT_BLUE_FOREGROUND = 94
    LIGHT_MAGENTA_FOREGROUND = 95
    LIGHT_CYAN_FOREGROUND = 96
    WHITE_FOREGROUND = 97

    BLACK_BACKGROUND = 40
    RED_BACKGROUND = 41
    GREEN_BACKGROUND = 42
    YELLOW_BACKGROUND = 43
    BLUE_BACKGROUND = 44
    MAGENTA_BACKGROUND = 45
    CYAN_BACKGROUND = 46
    LIGHT_GRAY_BACKGROUND = 47
    GRAY_BACKGROUND = 100
    LIGHT_RED_BACKGROUND = 101
    LIGHT_GREEN_BACKGROUND = 102
    LIGHT_YELLOW_BACKGROUND = 103
    LIGHT_BLUE_BACKGROUND = 104
    LIGHT_MAGENTA_BACKGROUND = 105
    LIGHT_CYAN_BACKGROUND = 106
    WHITE_BACKGROUND = 107


def to_color(
    text: str,
    foreground_color: Color = Color.WHITE_FOREGROUND,
    background_color: Color = Color.BLACK_BACKGROUND,
    text_format: Format = Format.NORMAL,
) -> str:
    """Returns the text in the specified color."""

    return f"\033[{text_format.value};{foreground_color.value};{background_color.value}m{text}\033[0m"
