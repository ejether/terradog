

import os
import re
import git

from .helpers import parse_yaml_file


class Docs(object):
    """
        Provides and automated way to keep the /monitors.md document up to date without toil
    """
    @classmethod
    def monitors(cls):
        # Get all the monitors from the disk
        monitors_path = os.path.join(os.path.dirname(__file__), 'monitors')

        monitors_doc_line_list = [
            '# List of Monitor Families and Monitors'
            ''
        ]

        _, monitor_families, _ = next(os.walk(monitors_path))

        for monitor_family in monitor_families:
            monitors_doc_line_list.append(
                '- {}'.format(
                    " ".join(monitor_family.split('-')).title()
                )
            )

            for _, _, monitors in os.walk(os.path.join(monitors_path, monitor_family)):
                for monitor in monitors:
                    monitors_doc_line_list.append(
                        '    - [{}]({})'.format(
                            " ".join(monitor[:-4].split('_')).title(),
                            f"/terradog/monitors/{monitor}"
                        )
                    )
                    monitors_doc_line_list.append("         - Required Definitions:")

                    monitor_data = parse_yaml_file(os.path.join(monitors_path, monitor_family, monitor))
                    all_definitions = []

                    # Pull all definitions out of the monitor. Strip ${}
                    for key, value in monitor_data.items():
                        all_definitions += [match[2:-1] for match in re.findall(r'\${\w*}', str(value))]

                    # Uniq + Sort
                    all_definitions = list(set(all_definitions))
                    all_definitions.sort()

                    # Get Default Definitions

                    default_definitions = monitor_data.get('definition_defaults', {})

                    # Determing required definitions
                    for _def in [d for d in all_definitions if d not in default_definitions.keys()]:
                        monitors_doc_line_list.append("            - `{}`".format(_def))

                    monitors_doc_line_list.append("         - Optional Definitions: (default)")

                    for _def, _default in default_definitions.items():
                        monitors_doc_line_list.append("            - `{}`: {}".format(_def, _default))

            return '\n'.join(monitors_doc_line_list)
