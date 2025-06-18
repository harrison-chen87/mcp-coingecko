import base64
import requests

            notebook_api_url = f"{self.host}api/2.0/workspace/import"
            
            # Create a unique notebook path in the workspace
            notebook_path = f"/Workspace/{pipeline_name}_dlt_pipeline.ipynb"
            
            notebook_payload = {
                "path": notebook_path,
                "format": "JUPYTER",
                "content": base64.b64encode(notebook_content.encode("utf-8")).decode("utf-8"),
                "overwrite": True
            }
            response = requests.post(notebook_api_url, headers=self.headers, json=notebook_payload)
            if response.status_code != 200:
                raise Exception(f"Failed to upload notebook: {response.text}") 