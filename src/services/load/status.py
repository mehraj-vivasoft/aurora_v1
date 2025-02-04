from enum import Enum


class LoadStatus(Enum):
    """
    Enum for load status
    """

    UNPROCESSED = "unprocessed"
    SUCCESS = "success"
    PENDING = "pending"    