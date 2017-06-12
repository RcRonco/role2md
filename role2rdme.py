import sys
import os

from role2md.tasks.tasks_parser import parse_tasks
from role2md.defaults.defaults_parser import parse_defaults
from role2md.table_to_md import table_tomd


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

    md_table = table_tomd(table)
    print(md_table)


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
