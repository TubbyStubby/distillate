# #search-relevance thread export (Jun 2–6)

**Leo:** Every ranking tweak goes straight to an A/B test. Each test needs ~2 weeks to reach significance on CTR, and we can run about 3 at once without traffic getting too thin. That's ~6 experiments a month. We have a backlog of 40 ideas.

**Mei:** Proposal: offline replay harness. Take logged queries + the candidate set retrieved at the time + what users clicked, re-rank with the new model, and score with offline metrics (NDCG@10 using clicks as labels, plus a "would the clicked doc still be in the top 3" rate). Runs in minutes per idea.

**Sam:** Offline metrics lie. We've seen NDCG go up and CTR go down before (position bias: users click what's on top, so click labels favour the old ranking).

**Mei:** Yes, which is why the harness isn't a replacement. It's a filter: only ideas that pass offline go to A/B. We'd correct position bias with inverse propensity weighting using the position-randomised 1% traffic slice we already log.

**Leo:** Cost? Mei estimated 3 weeks for one engineer for the basic harness (log export, re-rank, NDCG), +2 weeks for IPW correction, +1 week to calibrate: run the last 10 past A/B tests through it and check whether offline direction matches online direction.

**Sam:** If calibration shows it agrees with A/B less than ~70% of the time, it's worse than useless.

**Raj (infra):** Logs are in BigQuery already, 90 days retention, candidate sets are logged for 100% of queries since April. Re-ranking needs the model server; can run batch mode on the spare GPU pool at night.

**Leo:** Also nice-to-haves people mentioned: a per-query diff viewer (old vs new ranking side by side), a "slices" breakdown (head vs tail queries, locales), and auto-generating the A/B config from a passing offline run.

**Mei:** Alternative cheaper option: interleaving experiments online. Mix old and new rankings in one result list, see which side gets clicks. Needs ~10× less traffic than A/B, so ~2–3 days per idea, but needs frontend work (~2 weeks) and still uses live traffic.

**Leo:** I need to take a recommendation to Priyanka (director) on Monday.
