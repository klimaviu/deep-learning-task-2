from pathlib import Path
from typing import Any, Dict, List, Optional
from llama_index.legacy.readers.base import BaseReader
from llama_index.legacy.schema import Document

class CSVReader(BaseReader):
    """CSV parser.

    Args:
        concat_rows (bool): whether to concatenate all rows into one document.
            If set to False, a Document will be created for each row.
            True by default.

    """

    def __init__(self, *args: Any, concat_rows: bool = True, encoding: str = "utf-8", **kwargs: Any) -> None:
        """Init params."""
        super().__init__(*args, **kwargs)
        self._concat_rows = concat_rows
        self.encoding = encoding

    def load_data(
        self, file: Path, extra_info: Optional[Dict] = None
    ) -> List[Document]:
        """Parse file.

        Returns:
            Union[str, List[str]]: a string or a List of strings.

        """
        try:
            import csv
        except ImportError:
            raise ImportError("csv module is required to read CSV files.")
        text_list = []
        with open(file, encoding=self.encoding) as fp:
            csv_reader = csv.reader(fp)
            for row in csv_reader:
                text_list.append(", ".join(row))
        if self._concat_rows:
            return [Document(text="\n".join(text_list), metadata=extra_info)]
        else:
            return [Document(text=text, metadata=extra_info) for text in text_list]
