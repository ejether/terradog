import os
import glob
import logging
import traceback

from .resource import Resource

from .helpers import merge_dict, parse_yaml_file

logger = logging.getLogger(__name__)


class ResourceGroup(object):

    def __init__(self, data: list, resource_type: str, destination: str, global_definitions: dict) -> None:
        self.data = data
        self.destination = destination
        self.type = resource_type
        self.global_definitions = global_definitions
        self.resources = []
        self.local_path = os.path.dirname(__file__)
        self.compile_resources_to_create()

    def parse_exclusions(self, source: str, exclusions: list):
        # Get any monitors that need to be excluded from the family
        # Convert to format for later use
        exclusion_paths = []
        for exclusion in exclusions:
            exclusion_paths.append(f"{source}/{exclusion.replace('.', '/')}.yml")
        logger.debug(f"Exclusions: {exclusion_paths}")
        return exclusion_paths

    def get_resource_files(self, source: str) -> list:
        resource_file_paths = []
        if "." in source:
            resource_file_paths = ["{}/{}/{}.yml".format(self.local_path, self.type, ("/").join(source.split(".")))]
        else:
            resource_file_paths = glob.glob("{}/{}/{}/*.yml".format(self.local_path, self.type, source))
        return resource_file_paths

    def get_resource_data(self, resource_files: list, exclusion_paths: list, item: dict) -> list:
        resources_data = []

        for local_source_path in resource_files:
            if os.path.isfile(local_source_path) and ('/').join(local_source_path.split('/')[-2:]) in exclusion_paths:
                continue

            resource_data = parse_yaml_file(local_source_path)
            # If the items are being pulled from a family,
            # then use all the values in the default item
            if len(resource_files) == 1:
                # Otherwise, overwrite the item values with
                # the values being passed in
                resource_data = merge_dict(resource_data, item)

            resources_data.append(resource_data)

        return resources_data

    def compile_resources_to_create(self) -> None:
        """
        Iterate over the resources in the resource group
        Parse the families, and inline resources
        Parse and remove exclusions
        Compile the Resources to be generated into self.resources
        """

        for item in self.data:
            source = item.get('source')
            # If the source is not None, assume it is a family, or a item from a family
            # Otherwise, treat it as an inline resource
            _pre_compiled_resources_to_create = []
            if source is None:
                _pre_compiled_resources_to_create.append(item)
            else:
                _pre_compiled_resources_to_create += self.get_resource_data(
                    self.get_resource_files(source),
                    self.parse_exclusions(source, item.get('exclude', [])),
                    item
                )

            for resource_data in _pre_compiled_resources_to_create:

                local_definitions = merge_dict(self.global_definitions, item.get('definitions', {}), clobber=True)

                if resource_data.get('vary_by_namespace'):
                    namespaces = local_definitions.get('namespaces', [])

                    if namespaces == []:
                        raise AttributeError(f"Namespaces missing, required for {resource_data['name']}")

                    if not isinstance(namespaces, (list)):
                        raise AttributeError(f'Namespaces definition must be a list {resource_data.id}')
                    for namespace in namespaces:
                        resource_data_with_namespace_definition = resource_data.copy()
                        if not resource_data_with_namespace_definition.get('definitions'):
                            resource_data_with_namespace_definition['definitions'] = {}
                        resource_data_with_namespace_definition['definitions']['namespace'] = namespace
                        self.resources.append(Resource(resource_data_with_namespace_definition, self.type, self.destination, local_definitions))
                    continue
                else:
                    self.resources.append(Resource(resource_data, self.type, self.destination, local_definitions))

    def create(self) -> None:
        for resource in self.resources:
            logger.debug(f"creating {resource}")
            resource.create()
