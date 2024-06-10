from dataclasses import dataclass


@dataclass(frozen=True, slots=True, kw_only=True)
class GenericError[T]:
    error_msg: str
    invalid_entity: T
