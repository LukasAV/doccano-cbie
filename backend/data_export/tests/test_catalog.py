import unittest

from ..pipeline.catalog import Options
from projects.models import ProjectType


class TestOptions(unittest.TestCase):
    def test_return_at_least_one_option(self):
        for task in ProjectType:
            with self.subTest(task=task):
                options = Options.filter_by_task(task)
                self.assertGreaterEqual(len(options), 1)

    def test_option_names(self):
        expected_option_names = {
            ProjectType.DOCUMENT_CLASSIFICATION: ['CSV', 'JSON', 'JSONL', 'fastText'],
            ProjectType.SEQUENCE_LABELING: ['CoNLL', 'JSONL', 'OpenNLP name finder training format'],
            ProjectType.SEQ2SEQ: ['CSV', 'JSON', 'JSONL'],
            ProjectType.INTENT_DETECTION_AND_SLOT_FILLING: ['JSONL'],
            ProjectType.IMAGE_CLASSIFICATION:['JSONL'],
            ProjectType.IMAGE_CAPTIONING: ['JSONL'],
            ProjectType.BOUNDING_BOX: ['JSONL'],
            ProjectType.SEGMENTATION: ['JSONL'],
            ProjectType.SPEECH2TEXT: ['JSONL'],
        }
        for task in ProjectType:
            with self.subTest(task=task):
                options = Options.filter_by_task(task)
                option_names = [option['name'] for option in options]
                self.assertListEqual(sorted(option_names), sorted(expected_option_names[task]))
