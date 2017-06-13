import re
import os
from role2md.types import Entry


def parse_fact(lines, index, table, registered_vars):
    """ Handle set_fact declaration

        Retrieves line and check if there is fact declaration.
        If there is declaration add it to registered variables.
        Handle one-lined and multi-lined declarations.

        Args:
            :param lines:  The lines to check.
            :param index: The current line index in lines.
            :param table: The table to fill with the variables.
            :param registered_vars: A list to add the facts to

        Returns:
           Return the new index in lines.
        """
    tabs_count = 0
    fact_processing = False

    # Search if there is any one line set fact declaration
    set_fact = re.search("set_fact: .*=.*", lines[index])
    if set_fact:
        # Get all values and add them to the registered variables
        values = lines[index].split(" ")
        for value in values:
            if "=" in value:
                variable = value.split("=")[0]
                registered_vars.append(variable)
    else:
        # Check if there is any set fact declaration
        set_fact = re.search("set_fact:", lines[index])
        if set_fact:
            # Set values to start multi-line fact declaration
            fact_processing = True
            tabs_count = lines[index].find("set_fact:")
            index += 1

    # Parse multi-line declaration
    while fact_processing and index < len(lines):
        # Scan for used variable inside of the set_fact declaration
        scan_variables(lines[index], table, registered_vars)

        # Get the current indentation to check if set_fact finished
        curr_tabs = re.search("[ ]*", lines[index]).end()
        if tabs_count < curr_tabs:
            # Search for fact name
            fact = re.search(".*:", lines[index])
            if fact:
                # Add fact to registered variables
                registered_vars.append(fact.group()[:-1].strip())
            else:
                # Finish the fact processing
                break
        else:
            # Finish the fact processing
            break
        index += 1

    return index


def parse_used_variable(used_var):
    """ Parse Ansible variable that in use.

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


def scan_variables(line, table, registered_vars):
    """ Scan for used variables ansible task file.

       Retrieves a line and add to table all used variables.

       Args:
            :param line:  The line to Scan.
            :param table: The table to fill with the variables.
            :param registered_vars: A list to add the facts to

       Returns:
          None.
       """
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


def parse_tasks(file_path, table, recursive=False):
    """ Parse Ansible task file.

    Retrieves file path and table to fill with the Ansible role variables.

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
    index = 0

    lines = [line.rstrip('\n') for line in open(file_path)]

    # Run on each line in the task
    while index < len(lines):
        line = lines[index]
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
                vars_check = False
        elif vars_check:
            # Scan for variables in current line
            scan_variables(line, table, registered_vars)

            # Process set_fact variable
            index = parse_fact(lines, index, table, registered_vars)

        # Move to the next line
        index += 1

    return scanned_files, registered_vars
