
"""Loads PDF file into settings
"""

import json
import yaml

from tools.conf import settings

def load_pdf():
    """
    Updates settings with PDF data
    """
    filename = settings.getValue('pdf_file')
    with open(filename) as handle:
        data = handle.read()

    try:
        pdf = json.loads(data)
    except:
        try:
            pdf = yaml.safe_load(data)
        except:
            raise Exception(f"Invalid PDF file: {filename}")

    settings.setValue('pdf_file', pdf)
