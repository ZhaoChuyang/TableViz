from typing import Dict, List, Optional, Union, Tuple
import collections
from PIL import Image
import numbers


class TableData:
    def __init__(self, data: Union[Dict[str, List], List[Dict]], max_display_rows: int = 10, max_col_width: int = 20):
        """
        Initialize TableData from either a dictionary of columns or a list of rows.

        Args:
            data: Input data which can be either:
                - Dict[str, List]: Dictionary where keys are column names and values are column data
                - List[Dict]: List of dictionaries where each dictionary represents a row
            max_display_rows: Maximum number of rows to display when printing the table.
            max_col_width: Maximum width (in characters) for each column when displaying.
        """
        if isinstance(data, dict):
            self._from_dict(data)
        elif isinstance(data, list):
            self._from_list(data)
        else:
            raise ValueError("Unsupported data type")
        
        self.max_display_rows = max_display_rows  # Limit for display
        self.max_col_width = max_col_width  # Max column width for display

    def _from_dict(self, data: Dict[str, List], column_order: Optional[List[str]] = None):
        """
        Initialize table data from a dictionary of columns.

        Args:
            data: Dictionary where keys are column names and values are column data
            column_order: Optional list specifying the order of columns. If provided,
                          must contain all columns from the data dictionary.
        """
        keys = list(data.keys())
        # Use specified column order if provided, otherwise keep original order
        if column_order is not None:
            # Validate that column_order contains all original keys
            assert set(column_order) == set(keys), \
                   "column_order must contain all original columns"
            keys = column_order
        
        # Reorder keys
        data = {key: data[key] for key in keys}

        self.data = data
        self.keys = keys
        self.validate_data_types()
    
    def _from_list(self, data: List[Dict], column_order: Optional[List[str]] = None):
        """
        Initialize table data from a list of rows.

        Args:
            data: List of dictionaries where each dictionary represents a row
            column_order: Optional list specifying the order of columns. If provided,
                          must contain all columns from the data.
        """
        assert len(data) > 0, "Data should not be empty."
        
        # Get keys from first row
        keys = list(data[0].keys())
        
        # Use specified column order if provided, otherwise keep original order
        if column_order is not None:
            # Validate that column_order contains all original keys
            assert set(column_order) == set(keys), \
                   "column_order must contain all original columns"
            keys = column_order
        
        # Convert list of rows to dictionary of columns
        result = collections.defaultdict(list)
        for row in data:
            for key in keys:
                result[key].append(row[key])
        
        self.data = dict(result)
        self.keys = keys
        self.validate_data_types()
    
    def validate_data_types(self):
        """
        Validate that all values in the table are of supported types.

        Supported types are: numbers.Number, str, and PIL.Image.Image.
        """
        for col in self.keys:
            for value in self.data[col]:
                if isinstance(value, (numbers.Number, str, Image.Image, Dict, List, Tuple)):
                    continue
                else:
                    raise ValueError(f"Unsupported data type in column '{col}': {type(value)}")
    
    def reorder_columns(self, new_order: List[str]):
        """
        Reorder the columns in the table.

        Args:
            new_order: List of column names in the desired order. Must contain
                       all existing columns.
        """
        assert set(new_order) == set(self.keys), \
               "new_order must contain all existing columns"
        self.keys = new_order
        self.data = {col: self.data[col] for col in new_order}
    
    @property
    def columns(self):
        """Get the list of column names."""
        return self.keys

    def __len__(self):
        """Get the number of rows in the data"""
        return len(next(iter(self.data.values()))) if self.data else 0
    
    def __getitem__(self, key: Union[str, List[str]]) -> Union[List, 'TableData']:
        """
        Get column(s) by name.

        Args:
            key: Either:
                - str: Single column name
                - List[str]: List of column names

        Returns:
            - If key is str: List of values for that column
            - If key is List[str]: New TableData containing only the specified columns
        """
        if isinstance(key, str):
            # Single column access
            if key not in self.keys:
                raise KeyError(f"Column '{key}' not found. Available columns: {self.keys}")
            return self.data[key]
        elif isinstance(key, list):
            # Multiple column access
            for k in key:
                if k not in self.keys:
                    raise KeyError(f"Column '{k}' not found. Available columns: {self.keys}")
            new_data = {k: self.data[k] for k in key}
            return TableData.from_dict(new_data)
        else:
            raise TypeError("Column access must be string or list of strings")
    
    def iterrows(self):
        """
        Iterate over the table rows.

        Yields:
            Tuple[int, Dict]: For each row, a tuple containing:
                - int: Row index
                - Dict: Dictionary of column values for that row
        """
        for i in range(len(self)):
            yield i, {col: self.data[col][i] for col in self.keys}
    
    def __repr__(self):
        """Return the representation of the table in DataFrame format"""
        if not self.data or not self.keys:
            return "Empty TableData"
        
        # Determine how many rows to display
        num_rows = len(next(iter(self.data.values())))
        display_rows = min(num_rows, self.max_display_rows)
        
        # Prepare header
        headers = [str(col)[:self.max_col_width].ljust(self.max_col_width) for col in self.keys]
        header_line = " | ".join(headers)
        separator = "-" * len(header_line)
        
        # Prepare rows
        rows = []
        for i in range(display_rows):
            row_values = []
            for col in self.keys:
                value = str(self.data[col][i])
                if len(value) > self.max_col_width:
                    value = value[:self.max_col_width-3] + "..."
                row_values.append(value.ljust(self.max_col_width))
            rows.append(" | ".join(row_values))
        
        # Add ellipsis if we're not showing all rows
        if num_rows > display_rows:
            rows.append(f"... ({num_rows - display_rows} more rows)")
        
        return f"TableData ({num_rows} rows × {len(self.keys)} columns)\n" + \
               f"{header_line}\n{separator}\n" + \
               "\n".join(rows)
