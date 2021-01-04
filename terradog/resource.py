import os
import re
import logging
import traceback

from string import Template
from terradog.helpers import render_template, merge_dict

logger = logging.getLogger(__name__)


class Resource(object):

    def __init__(self, data: dict, resource_type: str, destination: str, global_definitions: dict = {}) -> None:
        self.data = data
        self.destination = destination
        self.type = resource_type
        self.global_definitions = global_definitions
        self.local_path = os.path.dirname(__file__)
        self.replace_definitions()

    @property
    def files_directory(self) -> str:
        """Returns the path on disk where class is installed.
        Used to find the jinja templates (string)
        """
        return os.path.join(self.local_path, 'files')

    @property
    def template_file_name(self) -> str:
        return f"{self.type.rstrip('s')}.tf.jinja"

    @property
    def name(self) -> str:
        raw_resource_name = self.data.get('name', self.data.get('title', 'Unknown Title'))
        self.data['resource_name'] = re.sub('^_', '', re.sub('[^0-9a-zA-Z]+', '_', raw_resource_name.lower())).strip('_')
        return self.data['resource_name']

    @property
    def target_file_name(self) -> str:
        return os.path.normpath(os.path.join(self.destination, f"{self.name}.tf"))

    def render_directory_templates(self) -> None:
        """
        Loop and use render_template helper method on all templates
        in destination directory, but use the _data['name'] as the base
        for the target file instead of the template name itself
        """
        logger.debug(f"Creating: {self.target_file_name}")
        render_template(
            self.template_file_name,
            self.files_directory,
            self.target_file_name,
            self.data,
            delete_template=False,
            overwrite=True
        )

    def create(self) -> None:
        """ Create TF file for a single resource. """
        try:
            logger.debug("New Name: {}".format(self.name))

            for key in self.data:
                if type(self.data[key]) in [str]:
                    self.data[key] = self.data[key].replace('"', '\\"')

            self.render_directory_templates()

        except Exception as e:
            logger.error("Error occurred configuring component")
            logger.error(e)
            logger.debug(traceback.format_exc())

    def replace_definitions(self) -> None:
        """ Replace ${definitions} with their value """

        def _replace_definition(string, definitions):
            if type(string) in [str]:
                logger.debug("Replacing {} in {}".format(definitions, string))
                try:
                    return Template(string).substitute(**definitions)
                except KeyError as e:
                    raise KeyError("Missing required definition {}".format(e)) from None
            return string

        # Locally scoped copy of definitions to add monitor defaults to
        _definitions = self.definitions

        logger.debug("Definitions: {}".format(_definitions))
        for key in self.data.keys():

            # Just handle the tags and thresholds separately since they are a list.  Probably a
            # better way to do this in the future
            if key == 'tags':
                logger.debug("Found tags: {}".format(self.data[key]))
                for index, item in enumerate(self.data[key]):
                    self.data[key][index] = _replace_definition(self.data[key][index], _definitions)
            elif key == 'thresholds':
                logger.debug("Found thresholds: {}".format(self.data[key]))
                for threshold_type in self.data[key]:
                    self.data[key][threshold_type] = _replace_definition(self.data[key][threshold_type], _definitions)
            elif key == 'template_variables':
                logger.debug("Found template_variables: {}".format(self.data[key]))
                for index, item in enumerate(self.data[key]):
                    for k, v in item.items():
                        self.data[key][index][k] = _replace_definition(v, _definitions)
            else:
                self.data[key] = _replace_definition(self.data[key], _definitions)

    @property
    def definitions(self) -> dict:
        """ Return dictionary of merged definitions: global, definition_defaults, definitions """
        definitions = merge_dict(self.data.get('definition_defaults', {}), self.global_definitions, clobber=True)
        definitions = merge_dict(definitions, self.data.get('definitions', {}), clobber=True)
        return definitions
