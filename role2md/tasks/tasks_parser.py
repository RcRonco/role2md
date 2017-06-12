import re
import os
from role2md.entry import Entry


def parse_used_variable(used_var):
    """ Parse ansible variable that in use.

        Retrieves used variable string and return only the variable name.
        Example:
            receive - {{ some_var.out }}
            return - some_var

        Args:
            :param used_var:  The used variable string

    Returns:
       Return the variable name.
    """
    # Remove double curly brackets
    clean_var = used_var[2:-2].strip()

    # Check if variable 'function' is used, if yes remove usage
    if clean_var.find(".") != -1:
        clean_var = clean_var[:clean_var.find(".")]
    # Check if variable used as dictionary, if yes remove usage
    if clean_var.find("[") != -1:
        clean_var = clean_var.replace("[", ":").replace("]", "").replace("\'", "")
    # Check if the variable is known ansible/jinja variables
    if (clean_var == "item" or "lookup(" in clean_var or
            bool(re.findall("^ansible_.*", clean_var)) or
            bool(re.findall("^hostvars.*", clean_var))):
        clean_var = None

    return clean_var


def parse_tasks(file_path, table, recursive=False):
    """ Parse ansible task file.

    Retrieves file path and table to fill with the ansible role variables.

    Args:
        :param file_path:  The path to the yaml task file.
        :param table: The table to fill with the variables.
        :param recursive: Run recursively on every include of other ansible task that included.

    Returns:
       A list of the files the function ran on.
       A list of registered variables
    """
    scanned_files = [file_path]
    registered_vars = []
    sub_task = None

    lines = [line.rstrip('\n') for line in open(file_path)]

    # Run on each line in the task
    for line in lines:
        vars_check = True

        # check if there is register declaration
        register = re.search("register: .*", line)

        if register:
            # Get the variable that registered and saved it in the registered list
            clean_value = register.group().replace("register:", "").strip()
            registered_vars.append(clean_value)
            vars_check = False
        elif recursive:
            # Check if there is include declaration
            sub_task = re.search("include: .*", line)

        if sub_task:
            # Get the included file save it and parse it
            sub_task_path = "{}/{}".format(os.path.dirname(file_path),
                                           sub_task.group().replace("include:", "").strip())
            if os.path.exists(sub_task_path):
                sc_files, reg_vars = parse_tasks(sub_task_path, table, registered_vars)
                scanned_files += sc_files
                registered_vars += reg_vars
            else:
                print("The file {} did not found.".format(sub_task_path))
        elif vars_check:
            # Check if there is a variable used in the current line
            match_obj = re.findall("{{[A-Za-z0-9 -_.|]*}}", line)
            if match_obj:
                # Run on each founded variable
                for match in match_obj:
                    # Get the variable name without the using syntax
                    clean_value = parse_used_variable(match)

                    # Add to the table if its not already in it and not in the resisted variables
                    if clean_value and clean_value not in registered_vars and clean_value not in table:
                        table[clean_value] = Entry(clean_value, "Yes", "-")

    return scanned_files, registered_vars
