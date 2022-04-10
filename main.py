from dataclasses import asdict, dataclass, fields, is_dataclass
from dacite import from_dict
from typing import Any


def convert_data_class(value, class_from: Any, class_to: Any) -> Any:
  if not _has_required_fields_for_conversion(class_from, class_to):
    raise Exception("Missing required fields for conversion")
  payload = asdict(value)
  return from_dict(data_class=class_to, data=payload)

def _has_required_fields_for_conversion(class_from, class_to):
  flatten_fields_from = flatten_dataclass_fields(class_from)
  flatten_fields_to = flatten_dataclass_fields(class_to)
  result = True
  for field_name, field_type in flatten_fields_to.items():
    if (
      field_name not in flatten_fields_from 
      or flatten_fields_from[field_name] != field_type
    ):
      result = False
  return result



def flatten_dataclass_fields(cls, parent_field_name: str = '', sep: str = '.'):
    return dict(_flatten_dataclass_fields_gen(cls, parent_field_name, sep))

def _flatten_dataclass_fields_gen(cls, parent_field_name, sep):
    for field in fields(cls):
        new_field_name = parent_field_name + sep + field.name if parent_field_name else field.name
        if is_dataclass(field.type):
            yield from flatten_dataclass_fields(field.type, new_field_name, sep=sep).items()
        else:
            yield new_field_name, field.type
          
@dataclass
class C:
    x: int

@dataclass
class B:
    x: int
    c: C

@dataclass
class D:
    b: B


@dataclass
class D2:
    x: int
    b: B
b = B(1, C(2))
d2 = D2(1, b)
d = convert_data_class(d2, D2, D)
print(d)

res = flatten_dataclass_fields(D2)
print(res)

convert_data_class(C(1), C, D)