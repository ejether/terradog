import os
import logging
import traceback

from .helpers import validate_tf
from .resource_group import ResourceGroup

logger = logging.getLogger(__name__)


class TerraDog(object):

    """
    TerraDog class accepts a dictionary of datadog resources and definitions from which it
    will create a set of terraform configurations as described by the input dictionary
    """

    def __init__(self, raw_data, output_directory, *args, **kwargs) -> None:
        """
        Accepts
        - raw_data: Dictionary of parameters being used by the component (dict)
        - output_directory: directory in which to create resources

        Returns:
        None
        """

        self.raw_data = raw_data

        # Modify path and check to see if it is a dir.
        real_path = os.path.realpath(os.path.expanduser(output_directory))
        if os.path.isdir(os.path.realpath(os.path.expanduser(output_directory))):
            self.destination = real_path
        else:
            raise FileNotFoundError(f"{real_path} is not a directory!")

        # Get Top Level items
        self.global_definitions = self.raw_data.get('definitions', {})

    def create(self) -> None:
        """
        Executes ResourceGroup.create() on each ResourceGroup in the in-file
        Validate Terraform output

        Accepts:
            No Arguments
        Returns:
            None
        """
        for rg in self.resource_groups:
            rg.create()
            logger.warning(f"New {rg.type} added.")
        validate_tf(self.destination)

    @property
    def resource_groups(self) -> list[ResourceGroup]:
        """
        From the the in-file, parse the sections into ResourceGroups

        Accepts:
            No arguments
        Returns:
            list[ResourceGroup]
        """
        _resource_groups = []
        for resource_type in [key for key in self.raw_data.keys() if key not in ["definitions"]]:
            _resource_groups.append(
                ResourceGroup(
                    self.raw_data[resource_type],
                    resource_type,
                    self.destination,
                    self.global_definitions
                )
            )
        return _resource_groups
