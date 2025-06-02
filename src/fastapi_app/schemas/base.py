from pydantic import BaseModel, ConfigDict


class BaseSchema(BaseModel):
    model_config = ConfigDict(
        arbitrary_types_allowed=True  # just in case you use non-builtins
    )
