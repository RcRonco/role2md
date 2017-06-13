import os
from jinja2 import Environment, meta, FileSystemLoader
from role2md.types import Entry


# TODO: Add support for functions usage {{ variable | to_nice_json }}
# TODO: Add support for cleaning Ansible variables (Hostvars...).


def parse_templates(file_path, table, registered_vars=None):
    """ Parse Ansible template file.

        Retrieves file path and table to fill with the Ansible used variables.

        Args:
            :param file_path:  The path to the yaml task file.
            :param table: The table to fill with the variables.
            :param registered_vars: A list of variable registered in runtime.

        Raise:
            R2MException: An Error while parsing the default files.
    """
    # Initialize the registered variable list if not initialized already
    if registered_vars is None:
        registered_vars = []

    # Build a Jinja2 environment
    env = Environment(autoescape=False, loader=FileSystemLoader(os.path.dirname(file_path)))
    template_source = env.loader.get_source(env, os.path.basename(file_path))[0]

    # Parse the content of the template
    parsed_content = env.parse(template_source)

    # Get undeclared variable that in use
    undec_vars = meta.find_undeclared_variables(parsed_content)
    for value in undec_vars:
        if value not in registered_vars and value not in table:
            table[value] = Entry(value, "Yes", "-")

