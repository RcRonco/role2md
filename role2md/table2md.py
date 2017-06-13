import collections
from role2md.types import Entry, R2MException


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
    if type(table) is None or not table:
        raise R2MException("The table is null or empty!")

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
