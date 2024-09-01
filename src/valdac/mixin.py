from dataclasses_json import DataClassJsonMixin
from beartype.door import is_bearable
from dataclasses import fields
from typing import get_type_hints, Any, Dict
from pydantic import TypeAdapter


class DataClassMixin(DataClassJsonMixin):

    def validate(self) -> bool:
        """
        Validate the dataclass instance against its type hints.

        This method checks each field of the dataclass against its
        corresponding type hint using beartype's is_bearable function.

        Returns:
            bool: True if all fields are valid according to their type hints.

        Raises:
            ValueError: If any field's value does not match its expected type.
        """
        type_hints = get_type_hints(self.__class__)

        for field in fields(self):
            field_name = field.name
            field_value = getattr(self, field_name)

            if field_name in type_hints:
                expected_type = type_hints[field_name]
                if not is_bearable(field_value, expected_type):
                    raise ValueError(
                        f"Field '{field_name}' with value '{
                            field_value}' does not match the expected type '{expected_type}'"
                    )

        return True

    @classmethod
    def json_schema(cls) -> Dict[str, Any]:
        """
        Generate a JSON schema for the dataclass.

        This method creates a temporary Pydantic dataclass based on the
        current class and uses Pydantic's TypeAdapter to generate the
        JSON schema.

        Returns:
            Dict[str, Any]: A dictionary representing the JSON schema of the dataclass.
        """
        type_adapter = TypeAdapter(cls)
        return type_adapter.json_schema()
