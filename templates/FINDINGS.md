<!-- studies/<id>/FINDINGS.md: written when the study closes. `record.py promote` turns it into
     the study's page on the website, so write for a reader who has not seen the LOG.
     Images are relative to the study folder, e.g. ![caption](runs/<run-id>/fig.png);
     promote copies them into showcase/figures/. -->

## Verdict

One paragraph: what we asked, what we found, and whether the hypothesis held.

## Evidence

The key table or figure. Every figure gets a caption that says what to look at and what it means.

![Accuracy change against the share of parameters removed. Look at where the PGI curve sits relative to L1: below it at every budget.](runs/20261124-1340-server-clean_s42/fig_budget.png)

| Selector | Accuracy change (points, validation, 3 seeds) |
|---|---|
| L1 magnitude | −7.1 ± 0.9 |
| PGI (corrected) | −8.4 ± 1.0 |

## Why we think this happened

Our explanation, how confident we are, and what would change our mind.

## Limits

What this study does not show (models, datasets, seeds, splits).

## What this means for the project

The decision this result leads to, and links to the next study.
