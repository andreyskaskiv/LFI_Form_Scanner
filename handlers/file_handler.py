from colorama import Fore, Style

from handlers.decorators import with_progress_bar

PREFIX = "report/"


@with_progress_bar
def write_links_to_file(data: list[str], write_file: str):
    """Write data to a file"""
    with open(PREFIX + write_file + '.txt', 'w') as file_to_write:
        for count_line, line in enumerate(data, 1):
            row = f"{line}\n"
            file_to_write.write(row)

    return (f"{Fore.YELLOW}{Style.BRIGHT}\n "
            f"👾 File name: '{write_file}.txt' 👾 "
            f"{Style.RESET_ALL}\n")


def write_target_links(filename: str, link: str):
    with open(PREFIX + filename, 'a') as file:
        file.write(link + '\n')


@with_progress_bar
def write_data_to_file(data: list[str], write_file: str):
    """Write data to a file"""
    with open(PREFIX + write_file + '.txt', 'w', encoding='utf-8') as file_to_write:
        for count_line, line in enumerate(data, 1):
            row = (f"{count_line}. {line[0]}\n"
                   f"{'- ' * 25}\n"
                   f"[***] 💉 Payload: \n{line[1]}\n"
                   f" {'= ' * 25}\n\n\n")
            file_to_write.write(row)

    return (f"{Fore.YELLOW}{Style.BRIGHT}\n "
            f"👾 File name: '{write_file}.txt' 👾 "
            f"{Style.RESET_ALL}\n")


@with_progress_bar
def write_forms_to_file(data: list[str], write_file: str):
    """Write data to a file"""
    with open(PREFIX + write_file + '.txt', 'w', encoding='utf-8') as file_to_write:
        for count_line, line in enumerate(data, 1):
            row = (f"{count_line}. {line[0]}\n"
                   f"{line[1]}\n"
                   f"{'- ' * 25}\n"
                   f"[***] 💉 Payload: {line[2]}\n"
                   f" {'= ' * 25}\n\n\n")
            file_to_write.write(row)

    return (f"{Fore.YELLOW}{Style.BRIGHT}\n "
            f"👾 File name: '{write_file}.txt' 👾 "
            f"{Style.RESET_ALL}\n")


def read_data_from_file(read_file: str) -> list[str]:
    """Read data from file"""
    lines = []
    with open(read_file) as file:
        for line in file:
            line = line.strip()
            if line:
                lines.append(line)

    return lines


def parse_data_from_authorization_file(read_file: str) -> dict[str, str]:
    """Parse data from abbreviations SVF_Sebastian Vettel_FERRARI"""
    lines_map = {}
    with open(read_file) as file:
        for line in file:
            line = line.strip()
            if line:
                line_split = line.split(":")
                lines_map[line_split[0]] = line_split[1]

    return lines_map
