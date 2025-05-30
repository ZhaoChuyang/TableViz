# TableViz

## Overview

TableViz is a Python project that provides tools for organizing and visualizing tabular data in HTML format. The project consists of two main components:

1. **TableData**: Organizes raw Python data structures (dicts and lists of dicts) into a structured table format
2. **Table**: Renders the structured TableData into HTML for display in web pages

## Features

- Convert Python dictionaries and lists of dictionaries into structured table data
- Customizable HTML rendering of tables
- Support for various table attributes (headers, styles, etc.)
- Easy integration with web applications

## Installation

```bash
pip install tableviz
```

## Usage

### Basic Example

```python
from tableviz import TableData, Table

# Create from a list of dictionaries
data = [
    {"name": "Alice", "age": 25, "department": "Engineering"},
    {"name": "Bob", "age": 30, "department": "Marketing"},
    {"name": "Charlie", "age": 28, "department": "Sales"}
]

# Organize the data
table_data = TableData(data)

# Render to HTML
table = Table(table_data)
html_output = table.render()

# Save or display the HTML
with open("output.html", "w") as f:
    f.write(html_output)
```

## Requirements

- Python 3.6+
- jinjia2
- Pillow

## License

MIT License

## Contributing

Contributions are welcome! Please fork the repository and submit a pull request.

## Support

For issues or questions, please open an issue on GitHub.
