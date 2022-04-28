import os
from PyInquirer import prompt


class ClientGeneratorError(SystemExit):
    pass


def create_dir(directory):
    generated_folder = directory
    isExist = os.path.exists(generated_folder)
    if not isExist:
        os.mkdir(generated_folder)


def generate_client(write_live: bool):
    if write_live and os.path.exists(os.path.join("src", "client")):
        raise ClientGeneratorError(
            "A client already exists. I cannot overwrite a client, you must delete the client first")

    questions = [
        {
            'type': 'input',
            'name': 'client_name',
            'message': 'What is the name of the client? (CamelCase)?'
        }]
    answers = prompt(questions)
    client_name = answers.get("client_name") + "Client"
    exception_name = client_name + "Exception"

    init_file_name = '__init__.py'
    client_file_name = 'client.py'

    if write_live:
        create_dir(os.path.join("src", "client"))
        init_file_location = os.path.join("src", "client", init_file_name)
        client_file_loc = os.path.join("src", "client", client_file_name)
    else:
        init_file_location = os.path.join("generated", "client", init_file_name)
        client_file_loc = os.path.join("generated", "client", client_file_name)
        create_dir("generated")
        create_dir(os.path.join("generated", "client"))

    init_content = f"from .client import {client_name}, {exception_name}  # noqa"

    with open(init_file_location, 'w') as f:
        f.write(init_content)

    client_content = f"""from keboola.http_client import HttpClient
from requests.exceptions import HTTPError
    
BASE_URL = \"\"
    
    
class {exception_name}(Exception):
    pass
        
        
class {client_name}(HttpClient):
    def __init__(self, token):
        self.token = token
        super().__init__(BASE_URL)
            
    def get_endpoint(self, endpoint):
        try:
            return self.get(endpoint_path=endpoint)
        except HTTPError as http_err:
            raise {exception_name}(http_err) from http_err
"""

    with open(client_file_loc, 'w') as f:
        f.write(client_content)
