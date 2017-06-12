import collections
from role2md.entry import Entry


def table_tomd(table):
    if type(table) is None or not table:
        raise Exception("The table is null or empty!")

    ordered_table = collections.OrderedDict(sorted(table.items()))

    md_table = "| Name    | Description    | Required    | Default    | Values | Examples |\n"
    md_table += "|:--|:--|:-:|:-:|:-:|:--|\n"

    for value, entry in ordered_table.items():
        if type(entry) is not Entry:
            raise Exception("The table is corrupted.")
        else:
            md_table += "| " + str(entry.m_name) + " | " + entry.m_description + \
                       " | " + entry.m_required + " | " + str(entry.m_default) + \
                       " | " + entry.m_value + " | " + entry.m_example + " |\n"

    return md_table
