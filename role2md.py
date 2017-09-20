import sys
import os
import argparse

from role2md.tasks.tasks_parser import parse_tasks
from role2md.defaults.defaults_parser import parse_defaults
from role2md.build_md import table_to_md,build_rdme
from role2md.templates.templates_parser import parse_templates


def init_args():
    parser = argparse.ArgumentParser(description="Convert ansible role to Readme")
    parser.add_argument('-src', metavar='I', type=str, help="The path to the ansbile role")
    parser.add_argument('-dst', metavar='O', type=str, help="The path to save the README.md")
    parser.add_argument('-desc', metavar='D', type=str, help="Description of the role")
    args = parser.parse_args()

    return args.src, args.dst, args.desc

def main(argv):
    table = {}
    src, dst, desc = init_args()

    if os.path.exists(dst):
        print("The output destination already exists.")
        exit(-1)

    if not os.path.exists(src):
        raise Exception("{} does not exists.".format(src))

    # Parse all the default files in the role
    if os.path.exists(src + "/defaults"):
        for subdir, dirs, files in os.walk(src + "/defaults"):
            for file in files:
                parse_defaults((os.path.join(subdir, file)), table)
                print("Defualt: {}".format(os.path.join(subdir, file)))

    # Parse main.yml task recursively, if main.yml exists
    if os.path.exists(src + "/tasks"):
        scanned_files, registered_vars = parse_tasks((os.path.join(src, "tasks/main.yml")), table, True)
        print("Files scanned:\n\t\t" + '\n\t\t'.join(scanned_files))
    else:
        raise Exception("{}/task/main.yml does not exists.".format(src))

    # Parse all the template files in the role
    if os.path.exists(src + "/templates"):
        for subdir, dirs, files in os.walk(src + "/templates"):
            for file in files:
                parse_templates((os.path.join(subdir, file)), table, registered_vars)
                print("Template: {}".format(os.path.join(subdir, file)))
    else:
        print("Skipping templates - Templates not found.")

    with open(dst, "w") as fd:
        # Generate the markdown table from the collected variables
        fd.write(build_rdme(os.path.basename(src), description=desc, table=table_to_md(table)))


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
