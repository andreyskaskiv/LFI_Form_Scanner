from colorama import Fore, Style
from prettytable.colortable import ColorTable, Theme


class MyTheme(Theme):
    def __init__(self):
        super().__init__(
            default_color=f"{Fore.LIGHTYELLOW_EX}{Style.BRIGHT}",
            vertical_color=Fore.CYAN,
            horizontal_color=Fore.CYAN,
            junction_color=Fore.YELLOW,
        )


my_theme = MyTheme()


def show_param(directory_input, def_output_directory,
               path_to_links_to_crawler,
               requests_per_minute,
               submit_form_post, verbose,
               checks,level):

    submit_form_post = f"{Fore.LIGHTGREEN_EX}Yes{Style.RESET_ALL}" if submit_form_post == 'Y' else f"{Fore.LIGHTRED_EX}No{Style.RESET_ALL}"
    verbose = f"{Fore.LIGHTGREEN_EX}Yes{Style.RESET_ALL}" if verbose == 'Y' else f"{Fore.LIGHTRED_EX}No{Style.RESET_ALL}"
    level = f"{Fore.LIGHTGREEN_EX}{level}{Style.RESET_ALL}" if level == 'easy' else f"{Fore.LIGHTRED_EX}{level}{Style.RESET_ALL}"

    table = ColorTable(theme=my_theme, padding_width=2)
    table.field_names = [f"{Fore.LIGHTYELLOW_EX}{Style.BRIGHT}Parameter{Style.RESET_ALL}",
                         f"{Fore.LIGHTYELLOW_EX}{Style.BRIGHT}Value{Style.RESET_ALL}"]
    table.add_row(["DIRECTORY_INPUT:", directory_input])
    table.add_row(["DEF_OUTPUT_DIRECTORY:", def_output_directory])
    table.add_row(["PATH_TO_LINKS_TO_CRAWLER:", path_to_links_to_crawler])
    table.add_row(["REQUESTS_PER_MINUTE:", requests_per_minute])
    table.add_row(["SUBMIT_FORM_POST:", submit_form_post])
    table.add_row(["VERBOSE:", verbose])
    table.add_row(["VULNERABILITY_CHECK:", checks])
    table.add_row(["LEVEL:", level])

    table.align = "l"

    print(f"\n{table}\n\n")
