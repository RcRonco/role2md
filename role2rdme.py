import sys
import os

from role2md.tasks.tasks_parser import parse_tasks
from role2md.defaults.defaults_parser import parse_defaults
from role2md.table2md import table_to_md
from role2md.templates.templates_parser import parse_templates


def main(argv):
    root_dir = argv[0]
    table = {}
    registered_vars = []

    if os.path.exists(root_dir + "/defaults"):
        for subdir, dirs, files in os.walk(root_dir + "/defaults"):
            for file in files:
                parse_defaults((os.path.join(subdir, file)), table)
                print("Defualt: {}".format(os.path.join(subdir, file)))

    if os.path.exists(root_dir + "/tasks"):
        scanned_files, registered_vars = parse_tasks((os.path.join(root_dir, "tasks/main.yml")), table, True)
        print("Files scanned:\n\t\t" + '\n\t\t'.join(scanned_files))

    if os.path.exists(root_dir + "/templates"):
        for subdir, dirs, files in os.walk(root_dir + "/templates"):
            for file in files:
                parse_templates((os.path.join(subdir, file)), table, registered_vars)
                print("Template: {}".format(os.path.join(subdir, file)))

    md_table = table_to_md(table)
    print(md_table)


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
