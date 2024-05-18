from ..yaml import load_yaml
from .validate_dags import validate_dags
from ..config import Config


class InvalidConfigError(ValueError):
    pass


class Validator:
    def __init__(self) -> None:
        pass

    @staticmethod
    def validate_file(path, raise_on_err=False, config:Config|None=None) -> list[bool, str|None]:
        contents = load_yaml(path)
        return Validator.validate(contents, raise_on_err)
    
    @staticmethod
    def validate(y: dict, raise_on_err=False, config:Config|None=None) -> list[bool, str|None]:
        result, msg = Validator._validate(y)
        if result is False and raise_on_err:
            raise InvalidConfigError(msg)
        return result
    
    @staticmethod
    def _validate(y: dict, config:Config|None=None) -> list[bool, str|None]:
        if not isinstance(y, dict):
            return False, "Incorrectly formatted (not a dict)"
        _config = config or Config()
        for k, v in y.items():
            if k == "dags":
                res, msg = validate_dags(v, config)
            else:
                return False, f"Unknown entry {k}"
            if res is False:
                return msg
        return True, None

