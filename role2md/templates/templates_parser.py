import os
from jinja2 import Environment, meta, FileSystemLoader
from role2md.entry import Entry


def parse_templates(file_path, table, registered_vars=None):
    if registered_vars is None:
        registered_vars = []

    env = Environment(autoescape=False, loader = FileSystemLoader(os.path.dirname(file_path)))
    template_source = env.loader.get_source(env, os.path.basename(file_path))[0]
    parsed_content = env.parse(template_source)
    undec_vars = meta.find_undeclared_variables(parsed_content)
    for value in undec_vars:
        if value not in registered_vars and value not in table:
            table[value] = Entry(value, "Yes", "-")

    print(undec_vars)

