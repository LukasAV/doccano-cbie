import abc

import pandas as pd


class Writer(abc.ABC):
    extension = ""

    @staticmethod
    @abc.abstractmethod
    def write(file, dataset: pd.DataFrame):
        raise NotImplementedError("Please implement this method in the subclass.")


class CsvWriter(Writer):
    extension = "csv"

    @staticmethod
    def write(file, dataset: pd.DataFrame):
        dataset.to_csv(file, index=False, encoding="utf-8")


class JsonWriter(Writer):
    extension = "json"

    @staticmethod
    def write(file, dataset: pd.DataFrame):
        dataset.to_json(file, orient="records", force_ascii=False)


class JsonlWriter(Writer):
    extension = "jsonl"

    @staticmethod
    def write(file, dataset: pd.DataFrame):
        dataset.to_json(file, orient="records", force_ascii=False, lines=True)


class OpenNLPWriter(Writer):
    extension = "opennlp.txt"

    @staticmethod
    def write(file, dataset: pd.DataFrame):
        def inline_annotations(row):
            text = row['text']
            entities = sorted(row['entities'], key=lambda x: x.start_offset, reverse=True)
            for entity in entities:
                text = text[:entity.start_offset] + f"<START:{entity.label}> " + text[entity.start_offset:entity.end_offset] + f" <END>" + text[entity.end_offset:]
            return text

        dataset['result'] = dataset.apply(inline_annotations, axis=1)
        with open(file, 'w') as f:
            for line in dataset['result']:
                f.write(line + '\n')


class CoNLLWriter(Writer):
    extension = "txt"

    @staticmethod
    def write(file, dataset: pd.DataFrame):
        result = []

        for index, row in dataset.iterrows():
            text = row['text']
            entities = row['entities']
            tokens = text.split()
            bio_tags = ['O'] * len(tokens)
            for entity in entities:
                start_word_index = len(text[:entity.start_offset].split())
                end_word_index = len(text[:entity.end_offset].split()) - 1

                if start_word_index <= end_word_index:
                    bio_tags[start_word_index] = 'B-' + str(entity.label)
                    for i in range(start_word_index + 1, end_word_index + 1):
                        bio_tags[i] = 'I-' + str(entity.label)

            for token, tag in zip(tokens, bio_tags):
                result.append(f"{token}\t{tag}")

            result.append("")

        with open(file, 'w') as f:
            for line in result:
                f.write(line + '\n')


class FastTextWriter(Writer):
    extension = "txt"

    @staticmethod
    def write(file, dataset: pd.DataFrame):
        dataset.to_csv(file, index=False, encoding="utf-8", header=False)
