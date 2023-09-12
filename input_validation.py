import datetime

def input_number(prompt="Please enter a decimal number: ", error="Input must be a decimal number: ",
                 conversion_function=float, le=None, lt=None, ge=None, gt=None):
    while True:
        try:
            value = conversion_function(input(prompt))
            if le is not None and value > le:
                print(F"{value} must be less than or equal to {le}")
                continue
            if lt is not None and value >= lt:
                print(F"{value} must be less than {lt}")
                continue
            if ge is not None and value < ge:
                print(F"{value} must be greater than or equal to {ge}")
                continue
            if gt is not None and value <= gt:
                print(F"{value} must be greater than {gt}")
                continue
            return value
        except ValueError:
            print(error)


def input_float(prompt="Please enter a decimal number: ", error="Input must be a decimal number: ", **kwargs):
    return input_number(prompt=prompt, error=error,
                        conversion_function=float, **kwargs)


def input_int(prompt="Please enter a whole number: ", error="Input must be a whole number: ", **kwargs):
    return input_number(prompt=prompt, error=error,
                        conversion_function=int, **kwargs)

def valid_date(date_text):
    try:
        datetime.datetime.strptime(date_text, '%m/%d/%Y')
        return True
    except ValueError:
        return False

def valid_string(value):
    if not value.isalpha():
        return False
    return True


def input_string(prompt="Please enter a string: ", error="Invalid input. Please enter a valid string.",
                 valid=lambda x: len(x) > 0):

    while True:
        value = input(prompt)
        if valid(value):
            return value
        print(error)


def y_or_n(prompt="Please answer yes or no: ", error="Invalid input. Please enter yes or no."):
    while True:
        value = input(prompt).lower()
        if value in ["yes", "y"]:
            return True
        elif value in ["no", "n"]:
            return False
        else:
            print(error)


def select_item(choices, prompt="Please select an item: ", error="Invalid input. Please select a valid item."):
    choice_map = dict(map(lambda x: (x.lower(), x), choices))

    while True:
        choice = input(prompt).lower()

        if choice in choice_map:
            return choice_map[choice]

        print(error)


def valid_password(password):
    return len(password) >= 1


def input_value(argtype, **kwargs):
    if argtype == "int":
        return input_int(**kwargs)
    elif argtype == "float":
        return input_float(**kwargs)
    elif argtype == "string":
        return input_string(**kwargs)
    elif argtype == "y_or_n":
        return y_or_n(**kwargs)
    elif argtype == "select_item":
        return select_item(**kwargs)
    else:
        raise ValueError(f"Invalid type argument: {argtype}. The valid values are 'int', 'float', 'string', 'y_or_n', "
                         f"and 'select_item'.")
