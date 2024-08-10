# Adding new formats

The following changes are necessary to add a new format for import or export


## Import

Changes in the following files are necessary to add a new import format, in the examples called `NewFormat`:


### `backend/data_import/pipeline/catalog.py`

Add a new format for the format, inheriting from the `Format` base class

```python
class NewFormat(Format):
    name = "NewFormat"
    accept_types = "text/*"
```

Register the new format, providing a sample file in `backend/data_import/pipeline/examples/sequence_labeling/example.xyz`

```python
Options.register(
    Option(
        display_name=NewFormat.name,
        task_id=ProjectType.SEQUENCE_LABELING,
        file_format=NewFormat,
        arg=ArgNewFormat,
        file=SEQUENCE_LABELING_DIR / "example.xyz",
    )
)
```
For `arg` either choose an existing format or define a new one

```python
class ArgNewFormat(BaseModel):
    custom_arg: str = "default arg value"
```


### `backend/data_import/pipeline/parsers.py`

Add a new parser for the format, inheriting from the `Parser` base class

```python
class NewFormatParser(Parser):
    def __init__(self, **kwargs):
        self._errors = []
        # parser specific initialization

    def parse(self, filename: str) -> Iterator[Dict[Any, Any]]:
        # Implement the parsing logic here
        # for every line in the file yield a dictionary with:
        #   DEFAULT_TEXT_COLUMN: the text as string
        #   DEFAULT_LABEL_COLUMN: the labels as a list of tupels (<start index, inclusive>, <end index, exclusive>, <label as string>). Can be omitted for unlabeled data
        yield {DEFAULT_TEXT_COLUMN: text, DEFAULT_LABEL_COLUMN: labels}
        
    @property
    def errors(self) -> List[FileParseException]:
        return self._errors
```


### `backend/data_import/pipeline/factories.py`

Import the new format from the catalog

```python
from .catalog import (
    ...
    NewFormat,
)
```

Import the new parser from the parsers

```python
from .parsers import (
    ...
    NewFormatParser,
)
```

Add the new parser to the parser factory

```python
def create_parser(file_format: Format, **kwargs):
    mapping = {
        ...
        NewFormat.name: NewFormatParser,
    }
    return mapping[file_format.name](**kwargs)
```


## Export

Changes in the following files are necessary to add a new import format, in the examples called `NewFormat`:


### `backend/data_export/pipeline/catalog.py`

Add a new format for the format, inheriting from the `Format` base class

```python
class NewFormat(Format):
    name = "NewFormat"
```
Register the new format, providing a sample file in `backend/data_export/pipeline/examples/sequence_labeling/example.xyz`

```python
Options.register(ProjectType.SEQUENCE_LABELING, NewFormat, SEQUENCE_LABELING_DIR / "example.xyz")
```


### `backend/data_export/pipeline/formatters.py`

Add new formatters to transform the dataset before writing it if necessary, inheriting from the `Formatter` base class

```python
class NewFormatFormatter(Formatter):
    def apply(self, dataset: pd.DataFrame) -> pd.DataFrame:
        # Implement the transformation logic here
        return dataset
```


### `backend/data_export/pipeline/writers.py`

Add a new writer for the format, inheriting from the `Writer` base class

```python
class NewFormatWriter(Writer):
    extension = "xyz"

    @staticmethod
    def write(file, dataset: pd.DataFrame):
        # Implement the writing logic here to write the formatted dataset to the file as needed
```


### `backend/data_export/pipeline/factories.py`

Import the new format from the catalog

```python
from .catalog import ..., NewFormat
```
Add the new writer to the writer factory

```python
def create_writer(file_format: str) -> writers.Writer:
    mapping = {
        ...
        NewFormat.name: writers.NewFormatWriter(),
    }
```

Configure the formatters for the new format

```python
def create_formatter(project: Project, file_format: str) -> List[Formatter]:
    ...
    mapping: Dict[str, Dict[str, List[Formatter]]] = {
        ...
        ProjectType.SEQUENCE_LABELING: {
            ...
            NewFormat.name: [
                NewFormatFormatter(**mapper_relation_extraction),
            ]
```
