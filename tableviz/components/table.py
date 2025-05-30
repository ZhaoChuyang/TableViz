import os
import datetime
from typing import Optional, Literal
from pathlib import Path
from jinja2 import Environment, FileSystemLoader
from PIL import Image
import numbers
from ..table_data import TableData
from ..utils import encode_base64_image, resize_longest_edge


TEMPLATE_DIR = Path(__file__).parent.parent / "templates"


class Table:
    def __init__(self, data: Optional[TableData], save_dir: Optional[str] = None, store_image: Optional[Literal['local', 'base64']] = 'local', resize_image: Optional[int] = None, max_rows: Optional[int] = None, display_index: Optional[bool] = None):
        """
        Args:
            data (TableData): The table data to be rendered.
            save_dir (Optional[str]): The directory where the HTML file and embed images will be saved. If set it to None, files will be saved in the current directory.
            store_image (Optional[Literal['local', 'base64']]): Whether to store the image as a local file or base64 encoded string. Defaults to 'local'.
            resize_image (Optional[int]): Resize the image to this size before saving. Set to None to disable resizing.
            max_rows (Optional[int]): Maximum number of rows to display. Defaults to None.
            display_index (Optional[bool]): Whether to display the index column. Defaults to None.
        """
        if save_dir is None:
            save_dir = f'./{datetime.datetime.now().strftime("tableview_%Y%m%d%H%M")}'
            os.makedirs(save_dir, exist_ok=True)
        
        if store_image == 'local':
            os.makedirs(os.path.join(save_dir, "images"), exist_ok=True)

        self.data = data
        self.store_image = store_image
        self.resize_image = resize_image
        self.max_rows = max_rows
        self.display_index = display_index
        self.save_dir = save_dir
        self.env = Environment(loader=FileSystemLoader(TEMPLATE_DIR))
        self.template = self.env.get_template('index.html')
    
    def setup_data(self, data: TableData):
        """Setup the table with the given data."""
        self.data = data

    def render(self) -> str:
        """Render the table as a HTML string"""
        #===============
        # Process rows
        #===============
        rows = []
        for row_idx, row in self.data.iterrows():
            
            row_data = dict()
            for key, val in row.items():
                if isinstance(val, Image.Image):
                    if self.store_image == 'local':
                        if self.resize_image is not None:
                            val = resize_longest_edge(val, self.resize_image)
                        val.save(os.path.join(self.save_dir, "images", f"image_{row_idx}_{key}.jpg"))
                        row_data[key] = {
                            'value': os.path.join("images", f"image_{row_idx}_{key}.jpg"),
                            'dtype': 'image'
                        }
                    elif self.store_image == 'base64':
                        img = encode_base64_image(val, 'JPEG')
                        row_data[key] = {
                            'value': f'data:image/jpeg;base64,{img}',
                            'dtype': 'image'
                        }
                    else:
                        row_data[key] = {
                            'value': '[Image]',
                            'dtype': 'str'
                        }
                elif isinstance(val, numbers.Number):
                    row_data[key] = {'dtype': 'number'}
                    if isinstance(val, numbers.Integral):
                        row_data[key]['value'] = f'{val}'
                    elif isinstance(val, numbers.Real):
                        row_data[key]['value'] = f'{val:.3f}'
                else:
                    row_data[key] = {
                        'value': val,
                        'dtype': 'string'
                    }
            
            rows.append((row_idx, row_data))

        columns = self.data.columns
        if self.display_index:
            columns = ['#'] + columns
        
        return self.template.render(
            columns=columns,
            rows=rows,
            display_index=self.display_index,
        )
    
    def save(self):
        """Save the rendered table to a html file"""
        html = self.render()
        with open(os.path.join(self.save_dir, 'index.html'), 'w') as f:
            f.write(html)
        