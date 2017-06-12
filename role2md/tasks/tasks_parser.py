import re
from role2md.entry import Entry


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