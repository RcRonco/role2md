import sys
import os
import yaml
import re
import collections


class Entry:
    m_name = ""
    m_description = "Please fill the description."
    m_required = "No"
    m_default = "-"
    m_value = "-"
    m_example = "Please fill the example."

    def __init__(self, name, required, default):
        self.m_name = name
        self.m_required = required
        self.m_default = default


def table_to_md(table):
    if type(table) is None or not table:
        raise Exception("The table is null or empty!")

    ordered_table = collections.OrderedDict(sorted(table.items()))

    mdtable = "| Name    | Description    | Required    | Default    | Values | Examples |\n"
    mdtable += "|:--|:--|:-:|:-:|:-:|:--|\n"

    for value, entry in ordered_table.items():
        if type(entry) is not Entry:
            raise Exception("The table is corrupted.")
        else:
            mdtable += "| " + str(entry.m_name) + " | " + entry.m_description + \
                       " | " + entry.m_required + " | " + str(entry.m_default) + \
                       " | " + entry.m_value + " | " + entry.m_example + " |\n"

    return mdtable


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


def parse_used_variable(used_var):
    clean_var = used_var[2:-2].strip()
    if clean_var.find(".") != -1:
        clean_var = clean_var[:clean_var.find(".")]
    if clean_var.find("[") != -1:
        clean_var = clean_var.replace("[", ":").replace("]", "").replace("\'", "")
    if (clean_var == "item" or "lookup(" in clean_var or
            bool(re.findall("^ansible_.*", clean_var)) or
            bool(re.findall("^hostvars.*", clean_var))):
        clean_var = None
    return clean_var


def parse_tasks(file_path, table, registered_vars=None):
    if registered_vars is None:
        registered_vars = []

    lines = [line.rstrip('\n') for line in open(file_path)]
    for line in lines:
        register = re.search("register: .*", line)
        if register:
            clean_value = register.group().replace("register:", "").strip()
            registered_vars.append(clean_value)
        else:
            match_obj = re.findall("{{[A-Za-z0-9 -_.]*}}", line)
            if match_obj:
                for match in match_obj:
                    clean_value = parse_used_variable(match)
                    if clean_value and clean_value not in registered_vars and clean_value not in table:
                        table[clean_value] = Entry(clean_value, "Yes", "-")


def main(argv):
    root_dir = argv[0]
    table = {}

    for subdir, dirs, files in os.walk(root_dir):
        if subdir == root_dir + "/defaults":
            for file in files:
                parse_defaults((os.path.join(subdir, file)), table)
                print("Defualt: " + os.path.join(subdir, file))
        elif subdir == root_dir + "/tasks":
            for file in files:
                parse_tasks((os.path.join(subdir, file)), table)
                print("Tasks: " + os.path.join(subdir, file))
        else:
            for file in files:
                print("Else: " + os.path.join(subdir, file))

    md_table = table_to_md(table)
    print(md_table)

    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
