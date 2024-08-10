from .catalog import (
    CSV,
    JSON,
    JSONL,
    AudioFile,
    CoNLL,
    BioC,
    Excel,
    Word,
    FastText,
    Format,
    ImageFile,
    TextFile,
    TextLine,
)
from .parsers import (
    CoNLLParser,
    BioCParser,
    CSVParser,
    ExcelParser,
    WordParser,
    FastTextParser,
    JSONLParser,
    JSONParser,
    LineParser,
    PlainParser,
    TextFileParser,
)


def create_parser(file_format: Format, **kwargs):
    mapping = {
        TextFile.name: TextFileParser,
        TextLine.name: LineParser,
        CSV.name: CSVParser,
        JSONL.name: JSONLParser,
        JSON.name: JSONParser,
        FastText.name: FastTextParser,
        Excel.name: ExcelParser,
        Word.name: WordParser,
        CoNLL.name: CoNLLParser,
        BioC.name: BioCParser,
        ImageFile.name: PlainParser,
        AudioFile.name: PlainParser,
    }
    return mapping[file_format.name](**kwargs)
