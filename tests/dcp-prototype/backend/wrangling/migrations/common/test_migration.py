import json
import unittest

import pkg_resources

from dcp_prototype.backend.wrangling.migrations.common.dataset_metadata import DatasetMetadata
from dcp_prototype.backend.wrangling.migrations.common.gather_dcp_one_data import generate_metadata_structure_from_targz


class TestMigration(unittest.TestCase):
    def test_end_to_end_migration_from_targz(self):
        """A simple end to end test case"""
        infile = pkg_resources.resource_filename(__name__, "../../fixtures/WongAdultRetina.tar.gz")
        expectedfile = pkg_resources.resource_filename(__name__, "../../fixtures/WongAdultRetina.json")

        dataset_metadata = DatasetMetadata()
        generate_metadata_structure_from_targz(infile, dataset_metadata)
        dataset_metadata.process()
        result_project = dataset_metadata.to_dict()
        with open(expectedfile) as jfile:
            expected_project = json.load(jfile)
            title = result_project.get("projects")[0].get("title")
            self.assertEqual(title, "WongAdultRetina")
            self.assertDictEqual(result_project, expected_project)
