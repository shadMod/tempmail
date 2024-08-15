from typing import TypedDict


class AttachmentTypedDict(TypedDict):
    filename: str
    contentType: str
    size: int
