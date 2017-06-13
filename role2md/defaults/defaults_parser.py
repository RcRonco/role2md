import yaml
from role2md.types import Entry, R2MException


def parse_sub_variable(var_name, var_values, table):
    """ Parse Ansible hashmap values.

        Retrieves the hashmap variable and add
         him and all sub-variable to the table.

        Args:
            :param var_name:  the name of the variable.
            :param var_values: The sub-variables needed parsing.
            :param table: The table to fill with the variables.

        Raise:
            R2MException: An Error while parsing the default files.
    """
    # Run on each sub-variable
    for sub_key, sub_value in var_values.items():
        # Append to variable name the sub-variable name
        full_key = "{}:{}".format(var_name, sub_key)

        # Check that there is no duplications in declaration
        if full_key in table:
            raise R2MException("There are duplications in the variables names.")
        # Check if the sub-variable is hashmap also
        if type(sub_value) is dict:
            parse_sub_variable(full_key, sub_value, table)
        else:
            table[full_key] = Entry(full_key, "No", sub_value)


def parse_defaults(file_path, table):
    """ Parse Ansible default file.

        Retrieves file path and table to fill with the Ansible role variables.

        Args:
            :param file_path:  The path to the yaml task file.
            :param table: The table to fill with the variables.

        Raise:
            R2MException: An Error while parsing the default files.
    """
    # Open default file
    with open(file_path, "r") as stream:
        try:
            # Parse defaults with yaml parser
            defaults = yaml.load(stream)

            # Run on each default key
            for key, value in defaults.items():
                # Check if there is duplication of variable default declaration
                if key in table:
                    raise R2MException("There are duplications in the variables names.")
                # Check if the value is  dictionary to parse sub variables
                elif type(value) is dict:
                    parse_sub_variable(key, value, table)
                # Check if there is default or lookup function in use
                elif "default" in str(value) and "lookup" in str(value):
                    clean_value = value[value.find("default"):-2].strip()
                    clean_value = clean_value[len("default") + 1:value[value.find("default"):-2].find(",")]
                    table[key] = Entry(key, "No", clean_value)
                else:
                    table[key] = Entry(key, "No", value)
        except yaml.YAMLError as err:
            print(err)
