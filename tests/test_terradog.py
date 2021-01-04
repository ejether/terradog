
import os
import re
import glob
import unittest
import logging


from terradog import TerraDog
from terradog.resource import Resource

from terradog.helpers import parse_yaml_file, hash_directory


logger = logging.getLogger(__name__)


def crush_file_contents(contents):
    return re.sub(contents, u'^\n', '')


def read_file(path):
    with open(path, 'rb') as f:
        return crush_file_contents(f.read().decode('utf-8')).encode('utf-8')


class TerraDogGoldenFilesTest(unittest.TestCase):
    source_file_path = './tests/fixtures/test_all.yaml'
    output_dir = './tests/goldenfiles/test_all'

    def setUp(self):
        # Get Test Data
        self.test_all_data = parse_yaml_file(self.source_file_path)

        # Get Hash of Existing Files
        self.start_hash = hash_directory(self.output_dir)

        # Delete Existing Files
        for f in glob.glob(os.path.join(self.output_dir, '*')):
            os.remove(f)

    def test_generated_files_match_golden_files(self):
        TerraDog(self.test_all_data, self.output_dir).create()
        self.end_hash = hash_directory(self.output_dir)

        self.assertEqual(self.start_hash, self.end_hash)


class TerraDogResourceGroupTest(unittest.TestCase):
    pass


class TerraDogResourceTest(unittest.TestCase):

    def setUp(self):
        self.test_data = parse_yaml_file('./tests/fixtures/test_resource.yaml')
        self.input_definitions = {
            'environment': 'test_environment',
            'cluster': 'test_cluster',
            'namespace': 'test_namespace',
            'notifications': '@test_notifications'
        }

    def test_inline_missing_definition_raises(self):
        definitions = {}
        with self.assertRaises(KeyError):
            Resource(self.test_data, 'monitor', '/tmp/', definitions)

    def test_inline_definitions(self):
        inline_definitions = {
            'cluster': 'inline_cluster',
            'namespace': 'inline_namespace'
        }

        combined_definitions = {
            'environment': 'test_environment',
            'cluster': 'inline_cluster',
            'namespace': 'inline_namespace',
            'notifications': '@test_notifications'
        }

        test_resource = Resource(self.test_data, 'monitor', '/tmp/', self.input_definitions)
        self.assertEqual(test_resource.data['definitions'], inline_definitions)
        self.assertEqual(test_resource.global_definitions, self.input_definitions)
        self.assertEqual(test_resource.definitions, combined_definitions)

        self.assertEqual(test_resource.data['query'], "inline_cluster inline_namespace test_environment")

    def test_attributes_and_properties(self):
        test_resource = Resource(self.test_data, 'monitor', '/tmp/', self.input_definitions)
        self.assertEqual(test_resource.global_definitions, self.input_definitions)
        self.assertEqual(test_resource.template_file_name, 'monitor.tf.jinja')
        self.assertEqual(test_resource.target_file_name, '/tmp/test_var_replacement_for_inline_monitors.tf')
        self.assertEqual(test_resource.data, self.test_data)

    def test_title_for_file_name(self):
        self.test_data['title'] = "New Test Title"
        test_resource = Resource(self.test_data, 'monitors', '/tmp/', self.input_definitions)
        self.assertEqual(test_resource.target_file_name, '/tmp/test_var_replacement_for_inline_monitors.tf')

    def test_pural_to_singular_for_resource_type(self):
        test_resource = Resource(self.test_data, 'monitors', '/tmp/', self.input_definitions)
        self.assertEqual(test_resource.template_file_name, 'monitor.tf.jinja')
