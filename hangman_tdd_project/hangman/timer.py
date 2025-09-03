from __future__ import annotations

import queue
import threading
import time
from typing import Optional, Tuple


def input_with_timeout(prompt: str, timeout: float) -> Tuple[Optional[str], bool]:

    q: "queue.Queue[str]" = queue.Queue()

    def _reader() -> None:
        try:
            text = input(prompt)
        except Exception: 
            text = ""
        q.put(text)

    t = threading.Thread(target=_reader, daemon=True)
    t.start()

   
    start = time.time()
    remaining = int(timeout)
    while t.is_alive():
        elapsed = time.time() - start
        new_remaining = int(timeout - elapsed)
        if new_remaining != remaining and new_remaining >= 0:
            remaining = new_remaining
            print(f"  ⏱  {remaining:2d}s left...", end="\r", flush=True)
        try:
            text = q.get(timeout=0.1)
            print(" " * 30, end="\r", flush=True)  
            return text, False
        except queue.Empty:
            pass
        if elapsed >= timeout:
            print(" " * 30, end="\r", flush=True)
            return None, True

    try:
        text = q.get_nowait()
    except queue.Empty:
        text = None
    return text, False
