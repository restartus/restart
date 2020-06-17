from typelib import List


class Frame:
    """Base class for everything that is storing all the details of a dataframe

    We have this class so you don't have recalculate everything
    And eventually it will allow you to overwrite assignments and cause recalc

    Attr:
    name(str): The facts about a pandas framce
    row_labels: the row names
    column_labels: the column names
    values: The raw data
    df: The Pandas Dataframe
    """
    def __init__(self, name: str,
                 row_labels: List[str] = [],
                 column_labels: List[str] = [],
                 values=[]):
        """Initialize Population
        Args:
            name(str): friendly name of population
        """
        self.name: str = name
        self.row_labels: List[str] = row_labels
        self.column_labels: List[str] = column_labels
        self.rows: int = len(row_labels)
        self.columns: int = len(column_labels)
        self.values = values
