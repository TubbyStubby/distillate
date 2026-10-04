# Postmortem: order-processing latency during the Autumn Sale (INC-5530)

Authors: Gabriel M., Sunita R. · Incident commander: Joe · Status: action items open

## Summary

During the sale peak (Oct 3, 19:00–19:40), order confirmation p99 went from ~120ms to **9.2s**. p50 only moved from 40ms to 70ms, and average latency stayed under 200ms, so the main dashboard (which shows the average) looked green. Customers saw spinning confirmation pages and ~3,100 double-submitted orders.

## System

- Orders land on a queue; a pool of workers (`order-worker`, 24 pods × 8 threads = 192 workers) processes them. Each order takes ~35ms of work on average, with a long tail (payment provider calls: 1% take ~800ms).
- Normal peak arrival: ~4,400 orders/s → utilisation ≈ 4,400 × 0.035 / 192 ≈ 80%.
- Sale peak arrival: ~5,200 orders/s → utilisation ≈ 95%. Briefly 5,400/s ≈ 98%.
- Autoscaler scales `order-worker` on **average CPU > 70%**, with a 3-minute cooldown and ~90s pod start. Workers spend most of their time waiting on I/O, so CPU stayed ~55% the whole time and the autoscaler never fired.

## What happened

- At ~95% utilisation, queue depth went from ~50 to ~38,000 in 12 minutes. Every order waited behind the queue, so the tail exploded while the median (orders that arrived at quiet moments) stayed fine.
- Little's law check: 38,000 queued ÷ 5,200/s ≈ 7.3s wait, which matches the observed p99.
- Clients retried after 5s timeouts, adding ~8% more arrivals and making it worse.

## Action items

1. **Scale on queue depth / wait time, not CPU** (Sunita): target queue wait < 200ms; scale out when depth > 2× (arrival rate × 0.2s). Pre-scale before announced sales.
2. **Keep headroom:** plan capacity for ≤ 70% utilisation at forecast peak.
3. **Dashboards show p99 and queue depth**, not just the average (Gabriel).
4. **Client retries with jitter and an idempotency key** to stop double submits.
5. Load test with the payment-provider tail included (the old load test used a constant 35ms).

Team will build item 1 next sprint. Joe asked for "something that explains to everyone why 95% is not fine when 80% is".
