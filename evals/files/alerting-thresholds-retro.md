# On-call retro: checkout alerting (Sept) — notes by Farah, reviewed with Tomasz and Ines

Ticket: OPS-1187 "Pager fatigue on checkout rotation"

## Where we are

- Current paging alert: `checkout_p95_latency > 800ms for 5m` OR `checkout_error_rate > 1% for 5m`.
- September: **42 pages**, **9 actionable**. 33 were false or self-resolving (deploy blips, one noisy region, a single slow payment provider for 6 minutes).
- Meanwhile we *missed* a real slow burn on Sept 19: error rate sat at 0.6% for 9 hours (below the 1% line), ~5,400 failed checkouts, found by a customer email.
- People on the rotation now ack and ignore. Ines: "we've trained ourselves to snooze it".

## The SLO

- Checkout availability SLO: **99.5%** of checkout requests succeed over 30 days → error budget = 0.5% of requests ≈ 3.6 hours of total outage per 30 days.
- ~2M checkout requests/day, so budget ≈ 300k failed requests per 30 days.

## Proposal (Tomasz): multi-window burn-rate alerts

Burn rate = how fast we spend the error budget relative to "exactly on budget". Burn rate 1 = would use the whole budget in exactly 30 days.

- **Page (fast burn):** burn rate > 14.4 over the last 1h AND > 14.4 over the last 5m. (14.4× burns 2% of the monthly budget in 1 hour.)
- **Page (medium burn):** burn rate > 6 over 6h AND > 6 over 30m. (6× burns 5% in 6 hours.)
- **Ticket, not page (slow burn):** burn rate > 1 over 3 days.
- The short window (5m / 30m) makes the alert stop quickly once the problem is fixed, so it doesn't keep paging after recovery.

Back-test on September data (Farah ran it in the notebook): would have paged **11 times, 9 of them actionable**, and the Sept 19 slow burn would have paged after ~2h40m (medium-burn rule) instead of never.

## Concerns raised

- Tomasz: latency isn't covered by the availability SLO. Proposal: a separate latency SLO (99% of checkouts under 1.5s) with the same burn-rate shape, phase 2.
- Ines: "a threshold is a threshold, why is this better?" → the answer is it's tied to user impact over time instead of a single instant number, and the two windows trade detection speed against noise.
- Low-traffic hours (3–6am): a few failures can spike the burn rate. Suggest a minimum request count before alerting.

Rollout: shadow mode for 2 weeks (alerts go to a Slack channel, not the pager), then switch.
