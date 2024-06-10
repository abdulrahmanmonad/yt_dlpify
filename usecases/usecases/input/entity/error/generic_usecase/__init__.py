from dataclasses import dataclass


@dataclass(frozen=True, slots=True, kw_only=True)
class UseCaseExecutionError[T]:
    invalid_entity: T
