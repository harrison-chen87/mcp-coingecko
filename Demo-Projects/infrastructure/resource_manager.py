import base64

            notebook_payload = {
                "path": notebook_path,
                "format": "PYTHON",  # Upload as Python file, not JUPYTER
                "content": base64.b64encode(python_content.encode('utf-8')).decode('utf-8'),
                "overwrite": True
            } 