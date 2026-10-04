# PR #2291: Per-key token bucket rate limiting (merged)

Author: @mkowalski · Reviewers: @ana-r, @tjb · Closes INC-4471 ("customer X burst killed shard 3")

## Summary

Replaces the old fixed-window limiter (100 req per calendar minute per API key) with a token bucket per API key, enforced at the gateway.

- Each key has a bucket with `capacity` tokens (default 100) that refills at `rate` tokens/sec (default 100/60 ≈ 1.67/s), continuously, not once a minute.
- Each request costs 1 token; `/search` and `/export` cost 5 and 20 tokens.
- If the bucket has fewer tokens than the request costs, the gateway returns 429 with `Retry-After` = seconds until enough tokens refill (rounded up).
- Buckets live in Redis; check-and-decrement is one Lua script (`ratelimit.lua`) so concurrent gateway pods can't double-spend. Each gateway pod also keeps a local 50ms cache of "definitely over limit" keys to avoid hammering Redis during floods.
- Plan tiers: free (cap 100, 1.67/s), pro (cap 600, 10/s), enterprise (custom).
- Headers on every response: `X-RateLimit-Limit` (capacity), `X-RateLimit-Remaining` (tokens left, floored), `X-RateLimit-Reset` (seconds until full).

## Why

Fixed windows let a client send 100 requests at 12:00:59 and 100 more at 12:01:00, so 200 in two seconds; that's what hit shard 3. Token bucket smooths it: a full bucket allows a burst of `capacity`, then the client is held to the refill rate.

## Behaviour changes customers may notice

- "I only sent 60 requests this minute and got a 429": they probably sent a burst that emptied the bucket, or used `/export` (20 tokens each). The limit is no longer "N per minute".
- `X-RateLimit-Remaining` can go up between requests (refill), which confused one SDK that assumed it only decreases.
- Remaining is floored, so it can show 0 while a 1-token request still succeeds a moment later.

## Review notes

@ana-r asked for a sliding-window log as a fallback if Redis is down; we went with fail-open + local per-pod bucket at 1/N of the rate instead (N = pod count). @tjb flagged clock skew between pods; irrelevant because refill math runs in Redis with Redis TIME.
