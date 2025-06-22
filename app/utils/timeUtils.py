from typing import Optional

import pytz
from dateutil.parser import isoparse


def parse_to_utc(s: Optional[str]) -> Optional[object]:
    if not s:
        return None
    dt = isoparse(s)
    if dt.tzinfo is not None:
        return dt.astimezone(pytz.UTC)
    shanghai = pytz.timezone('Asia/Shanghai')
    dt = shanghai.localize(dt)
    return dt.astimezone(pytz.UTC)