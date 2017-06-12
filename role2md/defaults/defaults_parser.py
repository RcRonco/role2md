import yaml
from role2md.entry import Entry


def parse_subvariable(key, value, table):
    for subkey, subvalue in value.items():
        full_key = key + ":" + subkey
        if full_key in table:
            raise Exception("There are duplications in the variables names.")
        if type(subvalue) is dict:
            parse_subvariable(full_key, subvalue, table)
        else:
            table[full_key] = Entry(full_key, "No", subvalue)


def parse_defaults(file_path, table):
    with open(file_path, "r") as stream:
        try:
            defaults = yaml.load(stream)
            for key, value in defaults.items():
                if key in table:
                    raise Exception("There are duplications in the variables names.")
                elif type(value) is dict:
                    parse_subvariable(key, value, table)
                elif "default" in str(value) and "lookup" in str(value):
                    clean_value = value[value.find("default"):-2].strip()
                    clean_value = clean_value[len("default") + 1:value[value.find("default"):-2].find(",")]
                    table[key] = Entry(key, "No", clean_value)
                else:
                    table[key] = Entry(key, "No", value)
            print(defaults)
        except yaml.YAMLError as err:
            print(err)
