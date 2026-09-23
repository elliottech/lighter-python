"""Normalize integer enums in openapi.json before running openapi-generator.

goctl-swagger emits every `options=` tag as a list of strings, even on integer
fields. Named members (`options=Cross:0|Isolated:1` in server.api) therefore
arrive as `"enum": ["Cross:0", "Isolated:1"]`, which the Python generator turns
into `set([null, null])` validators.

This script rewrites those into real integer enums:

* every integer enum keeps its shape but its members become ints;
* fully named integer enums additionally get a standalone
  `<Schema><Property>Enum` component schema (`enum: [0, 1]`,
  `x-enum-varnames: ["Cross", "Isolated"]`), so the generator emits an
  `IntEnum` class such as `AccountPositionMarginModeEnum`. The property itself
  stays an integer (rather than a `$ref`) because models are built with
  `model_construct`, which would leave raw ints in an enum-typed field and make
  pydantic warn on every `to_json()`;
* mixing named and unnamed members is an error.

Usage: python3 scripts/openapi_postprocess.py [openapi.json]
"""

import json
import re
import sys

FILE = sys.argv[1] if len(sys.argv) > 1 else "openapi.json"

INTEGER_ENUM_FORMATS = {
    "int8": "int32",
    "uint8": "int32",
    "int16": "int32",
    "uint16": "int32",
    "uin16": "int32",
    "int32": "int32",
    "uint32": "int64",
    "int64": "int64",
    "uint64": "int64",
}

ENUM_MEMBER_RE = re.compile(r"^(?:(?P<name>[A-Za-z_]\w*):)?(?P<value>-?\d+)$")


def _pascal(snake):
    return "".join(part[:1].upper() + part[1:] for part in snake.split("_"))


def _parse_members(schema, path):
    values = []
    names = []
    for raw in schema["enum"]:
        match = ENUM_MEMBER_RE.match(str(raw))
        if not match:
            raise ValueError(f"{path}: invalid integer enum member {raw!r}")
        values.append(int(match.group("value")))
        names.append(match.group("name"))
    if any(names) and not all(names):
        raise ValueError(f"{path}: every enum member must be named, or none")
    return values, names


def normalize_integer_enums(spec):
    if "components" in spec:
        schemas = spec["components"].setdefault("schemas", {})
    else:
        schemas = spec.setdefault("definitions", {})

    named_enums = {}
    for schema_name, schema in schemas.items():
        for prop_name, prop in schema.get("properties", {}).items():
            if prop.get("type") != "integer" or "enum" not in prop:
                continue
            path = f"{schema_name}.{prop_name}"
            values, names = _parse_members(prop, path)
            prop["enum"] = values
            if not any(names):
                continue

            enum_name = f"{schema_name}{_pascal(prop_name)}Enum"
            if enum_name in schemas or enum_name in named_enums:
                raise ValueError(f"{path}: enum schema {enum_name} already exists")
            named_enums[enum_name] = {
                "type": "integer",
                "format": INTEGER_ENUM_FORMATS.get(prop.get("format"), "int64"),
                "enum": values,
                "x-enum-varnames": names,
                "description": f"Named values of {schema_name}.{prop_name}",
            }
            prop["description"] = f"See {enum_name}"

    schemas.update(named_enums)
    return spec


def main():
    with open(FILE, "r", encoding="utf-8") as f:
        spec = json.load(f)

    normalize_integer_enums(spec)

    with open(FILE, "w", encoding="utf-8") as f:
        json.dump(spec, f, indent=2, ensure_ascii=False)


if __name__ == "__main__":
    main()
