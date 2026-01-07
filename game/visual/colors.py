colors: dict[str, str] = {
    "black": "0",
    "red": "1",
    "green": "2",
    "yellow": "3",
    "blue": "4",
    "magenta": "5",
    "cyan": "6",
    "white": "7",
    "gray-0100": "232",
    "gray-0200": "233",
    "gray-0300": "234",
    "gray-0400": "235",
    "gray-0500": "236",
    "gray-0600": "237",
    "gray-0700": "238",
    "gray-0800": "239",
    "gray-0900": "240",
    "gray-1000": "241",
    "gray-1100": "242",
    "gray-1200": "243",
    "gray-1300": "244",
    "gray-1400": "245",
    "gray-1500": "246",
    "gray-1600": "247",
    "gray-1700": "248",
    "gray-1800": "249",
    "gray-1900": "250",
    "gray-2000": "251",
    "gray-2100": "252",
    "gray-2200": "253",
    "gray-2300": "254",
    "gray-2400": "255"
}

def color_text(text: str, foreground_color: str | None = None, background_color: str | None = None, bold: bool = False) -> str:
    to_return: str = ""

    if bold:
        to_return += f"\033[1m"
    
    if foreground_color:
        to_return += f"\033[38;5;{colors.get(foreground_color)}m"

    if background_color:
        to_return += f"\033[48;5;{colors.get(background_color)}m"
    
    to_return += text + "\033[0m"
    return to_return