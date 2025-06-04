# TableViz

## Overview

TableViz is a Python project that provides tools for organizing and visualizing tabular data in HTML format. The project consists of two main components:

1. **TableData**: Organizes raw Python data structures (dicts and lists of dicts) into a structured table format
2. **Table**: Renders the structured TableData into HTML for display in web pages

Supported data types:
- number (integer, float)
- string
- PIL image
- python dict
- python list/tuple

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
from PIL import Image

# Raw data in python list
data = [
    {"name": "Alice", "age": 25, "department": "Engineering", "avatar": Image.open('alice.jpg')},
    {"name": "Bob", "age": 30, "department": "Marketing", "avatar": Image.open('bob.jpg')},
    {"name": "Charlie", "age": 28, "department": "Sales", "avatar": Image.open('charlie.jpg')}
]

# Create TableData and Table
table_data = TableData(data)
table = Table(table_data, save_dir='./test')

# Get HTML page in string format
html = table.get_html()

# Save HTML to './test/index.html'
table.save()

# Serve the HTML page on http://0.0.0.0:8000
table.serve(host='0.0.0.0', port=8000)
```

## Requirements

- Python 3.6+
- jinjia2
- Pillow
- rich

## License

MIT License

## Contributing

Contributions are welcome! Please fork the repository and submit a pull request.

## Support

For issues or questions, please open an issue on GitHub.
