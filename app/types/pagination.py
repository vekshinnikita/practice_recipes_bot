

from typing import Any, Generic, Literal, TypeVar

RecordType = TypeVar('RecordType')

class PaginatedResult(Generic[RecordType]):

    def __init__(self, total: int, records: list[RecordType], offset: int, limit: int ):
        self.total = total
        self.records = records
        self.offset = offset
        self.limit = limit

    def _is_previous(self):
        if self.offset - self.limit >= 0:
            return True
        return False

    def _is_next(self):
        if self.total - (self.offset + self.limit) > 0:
            return True
        return False
    
    def get_direction(self) -> Literal['only_prev', 'only_next', 'both', 'none']:
        is_previous = self._is_previous()
        is_next = self._is_next()

        if is_previous and is_next:
            return 'both'
        elif is_previous and not is_next:
            return 'only_prev'
        elif not is_previous and is_next:
            return 'only_next'
        else:
            return 'none'
        
    def len(self):
        return len(self.records)
    
    def is_previous(self):
        return self._is_previous()

    def is_next(self):
        return self._is_next()
    
    
