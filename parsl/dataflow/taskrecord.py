import threading
import datetime
from typing_extensions import TypedDict
from concurrent.futures import Future

# only for type checking:
from typing import Any, Callable, Dict, Optional, List, Sequence

from parsl.dataflow.futures import AppFuture
from parsl.dataflow.states import States

# this is the (very loose) type for the type of a parsl dfk task record
# I want to flesh it out using PEP 589 TypedDicts
# TaskRecord = Dict[str, Any]


class TaskRecord(TypedDict, total=False):
    func_name: str
    status: States
    depends: List[Future]

    app_fu: AppFuture
    exec_fu: Optional[Future]
    callback: None  # I think this might be unused? PR#1514 removes this field.

    executor: str

    retries_left: int
    fail_count: int
    fail_history: List[Any]

    checkpoint: bool  # this change is also in #1516
    hashsum: Optional[str]  # hash for checkpointing/memoization.

    task_launch_lock: threading.Lock

    # these three could be more strongly typed perhaps but I'm not thinking about that now
    func: Callable
    fn_hash: Any
    args: Sequence[Any]  # in some places we uses a Tuple[Any, ...] and in some places a List[Any]. This is an attempt to correctly type both of those.
    kwargs: Dict[str, Any]

    # env: None  # removed by PR#1517

    time_submitted: Optional[datetime.datetime]
    time_returned: Optional[datetime.datetime]

    memoize: bool
    ignore_for_cache: Sequence[str]

    id: int