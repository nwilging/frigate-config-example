import re
import os


def build(loaded_yaml):
    built = {}
    for key in loaded_yaml:
        built[key] = __parse(loaded_yaml[key])

    return built


def __parse(value):
    if isinstance(value, dict):
        rebuild = {}
        for key in value:
            rebuild[key] = __parse(value[key])
        return rebuild

    if isinstance(value, list):
        rebuild = []
        for element in value:
            rebuild.append(__parse(element))
        return rebuild

    if not isinstance(value, str):
        return value

    match = re.findall("{{ ([a-zA-Z0-9_]*) }}", value)
    if not match:
        return value

    for var in match:
        env = os.getenv(var)
        if not env:
            continue
        value = value.replace('{{ ' + var + ' }}', env)

    return value
