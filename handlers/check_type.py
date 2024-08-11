from distutils.util import strtobool


def check_type(value):
    if isinstance(value, bool):
        value_check = value
    elif value in 'YN':
        value_check = strtobool(value)
    else:
        value_check = True
    return value_check


if __name__ == '__main__':
    print(check_type('Y'))
    print(check_type('N'))
