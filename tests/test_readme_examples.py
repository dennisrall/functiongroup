from functiongroup import FunctionGroup
from typing import Protocol
import json
import pytest


class DictIO(Protocol):
    def save_dict(self, dict_: dict[str, str], file_name: str) -> None:
        ...

    def load_dict(self, file_name: str) -> dict[str, str]:
        ...


class JsonDictIO(DictIO):
    def save_dict(self, dict_: dict[str, str], file_name: str) -> None:
        with open(file_name, "w") as f:
            json.dump(dict_, f)

    def load_dict(self, file_name: str) -> dict[str, str]:
        with open(file_name) as f:
            return json.load(f)


json_dict_io = FunctionGroup()


@json_dict_io.register
def save_dict(dict_: dict[str, str], file_name: str) -> None:
    with open(file_name, "w") as f:
        json.dump(dict_, f)


@json_dict_io.register
def load_dict(file_name: str) -> dict[str, str]:
    with open(file_name) as f:
        return json.load(f)


@pytest.mark.parametrize("json_io", [JsonDictIO(), json_dict_io()])
def test_json_io(tmp_path: str, json_io: DictIO):
    d = {"function": "group"}
    json_file = tmp_path / "test.json"
    json_io.save_dict(d, json_file)
    assert json_io.load_dict(json_file) == d
    with open(json_file) as f:
        assert f.read() == '{"function": "group"}'
