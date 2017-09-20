import re
import collections
from jinja2 import Environment, PackageLoader
from role2md.types import Entry, R2MException


def clear_ansible_vars(table):
    """ Remove from the table the unneccesery ansible variables like:
        - ansible_*
        - item/item.*
        - hostvars
        - lookup
    Args:
        :param table:  Dictionary which the key is string and the key is Entry structure.
    Returns: None
    Raises:
        R2MException: An error occurred accessing the big table.Table object.
    """
    invalid_keys = []
    # Check that the table is ok
    if type(table) is None:
        raise R2MException("The table is null or empty!")

    for key in table.keys():
        # Check if the variable is known ansible/jinja variables
        if (key == "item" or "lookup(" in key or
                bool(re.findall("^ansible_.*", key)) or
                bool(re.findall("^hostvars.*", key)) or
                bool(re.findall("^item:.*", key))):
            invalid_keys.append(key)

    # Remove invalid entries
    for key in invalid_keys:
        del table[key]


def table_to_md(table):
    """ Generate An Markdown Table from Dictionary of Entries.
        Receive a dictionary of Entry structure and build and Markdown table from it.
    Args:
        :param table:  Dictionary which the key is string and the key is Entry structure.
    Returns:
       A string which contains the Markdown table.
    Raises:
        R2MException: An error occurred accessing the bigtable.Table object.
    """
    # Check that the table is ok
    if type(table) is None:
        raise R2MException("The table is null or empty!")

    clear_ansible_vars(table)

    # Reorder the entries in the dictionary to Alphabetic order
    ordered_table = collections.OrderedDict(sorted(table.items()))

    # Declare the table in MD
    md_table = "| Name    | Description    | Required    | Default    | Values | Examples |\n" \
               "|:--|:--|:-:|:-:|:-:|:--|\n"

    # Run on each entry and add it to the Markdown table
    for value, entry in ordered_table.items():
        # Check if all the values are Entry class type
        if type(entry) is not Entry:
            raise R2MException("The table is corrupted.")
        else:
            md_table += "| {} | {} | {} | {} | {} | {} |\n".format(str(entry.m_name), entry.m_description,
                                                                   entry.m_required, str(entry.m_default),
                                                                   entry.m_value, entry.m_example)

    return md_table


def build_rdme(name, description=None, table=None):
    env = Environment(loader=PackageLoader('role2md', '.'))
    template = env.get_template('README.md.jinja2')
    return template.render(role_name=name, role_description=description, variable_table=table)
