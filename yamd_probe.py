"""Временная разведка: задержки повторных поисковых запросов."""
import time

import config
from ym_client import YMClient

cfg = config.load()
c = YMClient()
c.ensure(cfg.get("token", ""))

for q in ("зем", "земф", "земфи", "земфир", "земфира"):
    t = time.time()
    c.search_all(q)
    a = time.time() - t
    print(f"{q:10s} search={a:.2f}s")
