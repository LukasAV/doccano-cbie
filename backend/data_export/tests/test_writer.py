import os
import unittest

import pandas as pd
from pandas.testing import assert_frame_equal

from ..pipeline.writers import CsvWriter, FastTextWriter, JsonlWriter, JsonWriter, OpenNLPWriter, CoNLLWriter

class ExportedSpanDummy:
    def __init__(self, label, start_offset, end_offset):
        self.label = label
        self.start_offset = start_offset
        self.end_offset = end_offset


class TestWriter(unittest.TestCase):
    def setUp(self):
        self.dataset = pd.DataFrame(
            [
                {"id": 0, "text": "A"},
                {"id": 1, "text": "B"},
                {"id": 2, "text": "C"},
            ]
        )
        self.file = "tmp.csv"

    def tearDown(self):
        os.remove(self.file)


class TestCSVWriter(TestWriter):
    def test_write(self):
        writer = CsvWriter()
        writer.write(self.file, self.dataset)
        loaded_dataset = pd.read_csv(self.file)
        assert_frame_equal(self.dataset, loaded_dataset)


class TestJsonWriter(TestWriter):
    def test_write(self):
        writer = JsonWriter()
        writer.write(self.file, self.dataset)
        loaded_dataset = pd.read_json(self.file)
        assert_frame_equal(self.dataset, loaded_dataset)


class TestJsonlWriter(TestWriter):
    def test_write(self):
        writer = JsonlWriter()
        writer.write(self.file, self.dataset)
        loaded_dataset = pd.read_json(self.file, lines=True)
        assert_frame_equal(self.dataset, loaded_dataset)


class TestFastText(unittest.TestCase):
    def setUp(self):
        self.expected = "__label__A exampleA\n__label__B exampleB"
        self.dataset = pd.DataFrame([*zip(self.expected.split("\n"))])

    def test_write(self):
        file = "tmp.txt"
        writer = FastTextWriter()
        writer.write(file, self.dataset)
        loaded_dataset = open(file, encoding="utf-8").read().strip()
        self.assertEqual(loaded_dataset, self.expected)


class TestOpenNLPWriter(TestWriter):
    def setUp(self):
        self.dataset = pd.DataFrame(
            [
                {"id": 0, "text": "ABCDEFG", "entities": [ExportedSpanDummy(label='AA', start_offset=1, end_offset=3)]},
                {"id": 1, "text": "HIJKLMN", "entities": [ExportedSpanDummy(label='BB', start_offset=2, end_offset=4)]},
                {"id": 2, "text": "OPQRSTU", "entities": [ExportedSpanDummy(label='CC', start_offset=3, end_offset=4)]},
            ]
        )
        self.file = "tmp.opennlp.txt"

    def test_write(self):
        writer = OpenNLPWriter()
        writer.write(self.file, self.dataset)
        with open(self.file, 'r', encoding='utf-8') as f:
            loaded_dataset = f.read().strip()
            self.assertEqual(loaded_dataset, 'A<START:AA> BC <END>DEFG\nHI<START:BB> JK <END>LMN\nOPQ<START:CC> R <END>STU')


class TestCoNLLWriter(TestWriter):
    def setUp(self):
        self.dataset = pd.DataFrame(
            [
                {"id": 0, "text": "A BC DEFG", "entities": [ExportedSpanDummy(label='AA', start_offset=1, end_offset=3)]},
                {"id": 1, "text": "HI JK LMN", "entities": [ExportedSpanDummy(label='BB', start_offset=2, end_offset=4)]},
                {"id": 2, "text": "OPQ R STU", "entities": [ExportedSpanDummy(label='CC', start_offset=3, end_offset=4)]},
            ]
        )
        self.file = "tmp.opennlp.txt"

    def test_write(self):
        writer = CoNLLWriter()
        writer.write(self.file, self.dataset)
        with open(self.file, 'r', encoding='utf-8') as f:
            loaded_dataset = f.read().strip()
            self.assertEqual(loaded_dataset, 'A\tO\nBC\tB-AA\nDEFG\tO\n\nHI\tO\nJK\tB-BB\nLMN\tO\n\nOPQ\tO\nR\tO\nSTU\tO')
