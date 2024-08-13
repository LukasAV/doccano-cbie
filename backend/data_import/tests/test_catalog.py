import unittest

from data_import.pipeline.catalog import Options
from projects.models import ProjectType


class TestOptions(unittest.TestCase):
    def test_return_at_least_one_option(self):
        for task in ProjectType:
            with self.subTest(task=task):
                options = Options.filter_by_task(task)
                self.assertGreaterEqual(len(options), 1)

    def test_option_names(self):
        expected_option_names = {
            ProjectType.DOCUMENT_CLASSIFICATION: ['CSV', 'Excel', 'JSON', 'JSONL', 'TextFile', 'TextLine', 'Word', 'fastText'],
            ProjectType.SEQUENCE_LABELING: ['BioC', 'CoNLL', 'JSONL', 'TextFile', 'TextLine', 'Word'],
            ProjectType.SEQ2SEQ: ['CSV', 'Excel', 'JSON', 'JSONL', 'TextFile', 'TextLine', 'Word'],
            ProjectType.INTENT_DETECTION_AND_SLOT_FILLING: ['JSONL', 'TextFile', 'TextLine', 'Word'],
            ProjectType.IMAGE_CLASSIFICATION: ['ImageFile'],
            ProjectType.IMAGE_CAPTIONING: ['ImageFile'],
            ProjectType.BOUNDING_BOX: ['ImageFile'],
            ProjectType.SEGMENTATION: ['ImageFile'],
            ProjectType.SPEECH2TEXT: ['AudioFile'],
        }
        for task in ProjectType:
            with self.subTest(task=task):
                options = Options.filter_by_task(task)
                option_names = [option['name'] for option in options]
                self.assertListEqual(sorted(option_names), sorted(expected_option_names[task]))
