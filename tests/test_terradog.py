
import os
import glob
import unittest
import logging

from terradog import TerraDog

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


# class DDGoldenTestCase(unittest.TestCase):

#     def setUp(self):
#         Config(
#             inventory='default',
#             interactive=False,
#             confirm=False,
#             overwrite=False,
#             home='tests/files/'
#         )

#         self.repo_dir=os.path.join(GOLDEN_HOME, "datadog/", self.name)
#         Config().infrastructure_repo=self.repo_dir

#         if not os.path.exists(self.repo_dir):
#             os.makedirs(self.repo_dir)
#         self.start_hash=HashDirectory(self.repo_dir)

#         shutil.rmtree(self.repo_dir)
#         shutil.copytree(os.path.join(GOLDEN_HOME, "initial/", self.start_inventory), self.repo_dir)

#         self.dd=Datadog(data={})

#     def tearDown(self):
#         self.end_hash=HashDirectory(self.repo_dir)
#         self.assertEqual(self.start_hash, self.end_hash)


# class TestDatadog(DDTestCase):

#     def test_datadog_defaults(self):

#         dd=Datadog()

#         self.assertEqual(dd._defaults, {'backend': 'datadog/tf.state'})
#         self.assertTrue(dd.inventory_required)
#         self.assertIsInstance(dd.inventory, (Inventory))
#         self.assertEqual(dd.display_name, "Datadog")
#         self.assertTrue(dd.update_implemented)


# class TestDatadogAdd(DDGoldenTestCase):
#     name="add"

#     def test_datadog_add(self):
#         self.dd._data['datadog_cluster_agent_token']='fake_token'
#         self.dd.add()


# class TestDatadogAddAzure(DDGoldenTestCase):
#     name="add-azure"

#     def test_datadog_add(self):
#         self.dd._data['cloud']='azure'
#         self.dd._data['datadog_sp_password']='fake_password'
#         self.dd._data['datadog_cluster_agent_token']='fake_token'
#         self.dd.add()


# class TestDashboards(DDGoldenTestCase):
#     name="dashboards"

#     def test_dashboard_add(self):
#         self.dd._data['datadog_cluster_agent_token']='fake_token'
#         self.dd.add()
#         data={
#             'definitions': {'cluster_tag': 'cluster_tag'},
#             'dashboards': [{'source': 'kubernetes.resources'}],
#         }
#         ds=Dashboards(data)
#         ds.add()


# class TestMonitorDefinitionsGlobal(DDGoldenTestCase):
#     name="monitors-global"

#     def test_pods_monitor_output(self):
#         self.dd._data['datadog_cluster_agent_token']='fake_token'
#         self.dd.add()
#         data={
#             'definitions': {
#                 'cluster': 'cluster_name',
#                 'pods_pending_critical_threshold': 1234,
#                 'namespace': 'namespace_name',
#                 'environment': 'test',
#                 'cluster_tag': 'cluster_tag',
#                 'notifications': '@slack',
#                 'low_urgency_notifications': '@slack',
#             },
#             'dashboards': [{'source': 'kubernetes.resources'}],
#             'monitors': [{'source': 'kubernetes.pods_pending'}],
#         }
#         ms=Monitors(data)
#         ms.add()


# class TestMonitors(DDGoldenTestCase):
#     name="pod-monitors"

#     def test_pods_monitor_output(self):
#         self.dd._data['datadog_cluster_agent_token']='fake_token'
#         self.dd.add()
#         with open(TEST_FILE_PATH + "rodd_test_input.yaml") as f:
#             data=yaml.load(f.read(), Loader=yaml.loader.FullLoader)
#         ms=Monitors(data)
#         ms.add()


# class TestDowntimes(DDGoldenTestCase):
#     name="downtimes"

#     def test_downtime_output(self):
#         self.dd._data['datadog_cluster_agent_token']='fake_token'
#         self.dd.add()
#         data={
#             'definitions': {
#                 'cluster': 'cluster_name',
#                 'namespace': 'namespace_name',
#                 'environment': 'test',
#                 'cluster_tag': 'cluster_tag',
#                 'notifications': '@slack',
#                 'low_urgency_notifications': '@slack',
#             },
#             'downtimes': [{
#                 'name': 'Test Maintenance Window',
#                 'scope': '*',
#                 'start': 1614285704,
#                 'end': 1645821704,
#                 'recurrence_type': 'days',
#                 'recurrence_period': 1,
#             }],
#         }
#         ms=Downtimes(data)
#         ms.add()
