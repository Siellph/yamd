"""Временная разведка: задержки повторных поисковых запросов."""
import time

import config
from ym_client import YMClient

cfg = config.load()
c = YMClient()
c.ensure(cfg.get("token", ""))
cl = c._client

for q in ("зем", "земф", "земфи", "земфир", "земфира"):
    t = time.time()
    cl.search(q, type_="all", nocorrect=False)
    a = time.time() - t
    t = time.time()
    cl.search_suggest(q)
    b = time.time() - t
    print(f"{q:10s} search={a:.2f}s suggest={b:.2f}s")
