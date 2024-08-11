from tqdm import tqdm


def with_progress_bar(func):
    def wrapper(data, write_file):
        if len(data) > 10:
            progress_bar = tqdm(data, bar_format="{l_bar}%s{bar}%s{r_bar}" % ('\033[93m Write to file: ', ''))
            result = func(progress_bar, write_file)
            progress_bar.set_postfix(file=write_file, refresh=True)
            progress_bar.close()
        else:
            result = func(data, write_file)

        return result

    return wrapper
