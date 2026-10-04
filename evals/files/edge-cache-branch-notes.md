# feature/edge-cache-v2 — notes (Priya, last updated Mar 14)

Branch is ~60 commits ahead of main, PR #812 (draft). Owner moving to payments team next sprint, Dan takes over eviction tuning.

## What's in the branch

- `imgcache/lru.go`: in-memory LRU with per-entry TTL (default 10 min). Byte-budgeted, not entry-count budgeted (images vary 4KB–3MB).
- `imgcache/policy/`: pluggable eviction policies behind `EVICTION_POLICY` flag: `lru`, `lfu`, `arc`, `s3fifo` (s3fifo half done, Priya says "probably the winner but haven't proven it").
- `Policy` interface: `Get(key) (hit bool)`, `Admit(key, size)`, `Evict() key`. Each node runs one policy instance per shard (16 shards).
- Warmup job: on deploy, pre-fetches top 5k keys from yesterday's access log. Took 4 min on staging, people complained.
- Admin dashboard (`/admin/cache`): live hit rate per shard, top keys, "evict now" button. No auth yet (TODO).
- Prometheus metrics: hit/miss, bytes, evictions, origin fetch latency.
- `cache-sim/`: docker-compose with redis (unused by the cache itself, used to store results), 3 app nodes, nginx in front, origin mock, and k6 replaying access logs at 1× real time. Comparing two policies takes a full replay per policy; a 24h log takes 24h. Priya started adding a "speedup" flag but nginx/k6 timing gets flaky above 4×.
- Notebook `analysis/hitrate.ipynb`: plots hit rate per policy from the redis results.

## Findings so far

- On a 2h slice: LRU 71% hit, LFU 69%, ARC 74%. Byte hit rate differs a lot from request hit rate because big images are rare but expensive.
- Hit rate drops for ~20 min after every deploy (cold cache) even with warmup.
- Scan traffic (crawler sweeps through old images) flushes LRU badly; ARC and S3-FIFO resist it.
- Access logs have: timestamp (ms), key, size, status, user agent. ~40M requests/day at peak region.

## Open questions

- Is S3-FIFO actually better on a full day?
- Should we optimise request hit rate or byte hit rate (origin egress cost is per byte)?
- How big should the cache be per node? Currently 8GB.

Dan's plan (Slack, Mar 13): "I'll get cache-sim running on my laptop first, then try to get it to 10× speed, then compare policies."
