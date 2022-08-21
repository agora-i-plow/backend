from json import loads
from json.decoder import JSONDecodeError

from fastapi import UploadFile

from app.utils.exceptions import BadRequest

# TODO: Maybe there is aiojson


def parse_json_file(file: UploadFile) -> list[dict]:
    data = file.file.read()
    try:
        result = loads(data)
        return result
    except JSONDecodeError as e:
        raise BadRequest("File is not in json format", e)
