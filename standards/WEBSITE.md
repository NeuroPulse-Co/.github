# Working with the website

The website [neuropulse-co.github.io](https://neuropulse-co.github.io) is our public lab notebook. This guide explains where its content comes from, how to add to it, and how to check your change before it goes live. Read [RECORDS.md](RECORDS.md) for the record standard and [STYLE.md](STYLE.md) for how to write.

## The one idea to remember

**You almost never edit the website repository.** The website shows what the research repositories publish in their `showcase/` folder on `main`. When you record your work properly in your study folder and run `record.py promote`, the site updates itself.

```
your study folder ──record.py promote──► showcase/ on main ──automatic──► website rebuild
(study.yaml, LOG.md,                     (study page, figures,            (within minutes, and
 FINDINGS.md, runs/)                      data, lab-note drafts)            every night)
```

## What goes where

| You want to… | Edit this | In which repo |
|---|---|---|
| Change a study's question, status, verdict or key numbers | `studies/<id>/study.yaml` | the research repo |
| Change the reasoning text on a study page | `studies/<id>/FINDINGS.md` | the research repo |
| Add a diagram, chart, table or figure to a study page | the `evidence:` list in `study.yaml` (see below) and [DIAGRAMS.md](DIAGRAMS.md) | the research repo |
| Publish a lab note | `showcase/posts/<date>-<id>.md` | the research repo |
| Change a workstream's explainer | `src/content/workstreams/W*.md` | NeuroPulse-Co.github.io |
| Add a glossary term | `src/data/glossary.yaml` | NeuroPulse-Co.github.io |
| Update the timeline | `src/data/timeline.yaml` (set `done: true`) | NeuroPulse-Co.github.io |
| Change names, roles or workstream owners | `standards/people.yaml`, `standards/workstreams.yaml` | .github |
| Add a new research repository | `registry.yaml` | NeuroPulse-Co.github.io |

**Never edit these by hand.** They are generated and will be overwritten:
- `showcase/manifest.yaml`
- `showcase/studies/*.md`
- anything in `showcase/figures/` or `showcase/data/`

To change a study page, edit the study folder and run `promote` again.

## Study pages and lab notes are different things

- **A study page is the record.** It holds the question, the success criterion, the verdict, the evidence and our reasoning. It changes every time you promote while the study runs. People cite it.
- **A lab note is the story.** It is written once, at a milestone, by a named team member. It says why we asked the question, what surprised us and what it changes for the project. It runs to 800–1500 words and uses one or two figures from the study. Lab notes double as drafts of thesis chapters.

The rule: **numbers live on study pages, narrative lives in lab notes.** A lab note can quote a number from its study page but never introduces a new one; it links to the study page instead. Not every study needs a lab note. Write one when there is a story worth telling, such as a milestone, a negative result or a change of plan.

## Common tasks

### Show progress on a study
```bash
uv run tools/record.py log <study-id>       # add today's LOG entry, then fill it in
# edit studies/<study-id>/study.yaml: key_results, status, verdict when it closes
# edit studies/<study-id>/FINDINGS.md
uv run tools/record.py promote <study-id>
uv run tools/record.py check
```
Then commit and merge to `main`. A `running` study appears on the site as "In progress", and its numbers are labelled interim.

### Add evidence (diagrams, charts, tables, figures)
A study page leads with pictures, in this order:
1. the method diagram
2. the charts
3. the key numbers
4. the tables and figures
5. our reasoning.

You list them in `study.yaml` under `evidence:`. The full field reference is in [RECORDS.md](RECORDS.md) (Evidence).

```yaml
evidence:
  - type: diagram                   # how to draw one: DIAGRAMS.md
    source: diagrams/method.excalidraw.svg
    title: How we tested each step against the paper
    caption: >-
      Each box is one step of ASF-S. Steps 0 to 7 match the paper; the amber step does not.
  - type: chart                     # drawn by the website from a CSV: one dot per row (seed)
    source: runs/<run-id>/results.csv
    filter: {scope: paper, ft_mode: fc}
    x: method
    y: d_acc
    y_label: Change in accuracy after pruning (points)
    split: test
    labels: {pgi_aligned: PGI, random: Random filters}
    reference: {label: Paper, value: -3.78}
    title: Accuracy lost after pruning, by method
    caption: >-
      Each dot is one seed. Every method sits far below the paper's line, so the gap is not
      caused by PGI alone.
  - type: table
    source: runs/<run-id>/results.csv
    filter: {scope: paper}
    columns: {method: Method, ft_mode: Retraining, ft_seed: Seed, d_acc: "Change (points)"}
    split: test
    title: Every run behind the chart
    caption: One row per method, retraining mode and seed.
  - type: figure                    # an image your code made
    source: runs/<run-id>/fig6_pareto.png
    title: Accuracy against parameters removed
    caption: >-
      Look at where the paper's point sits: above every curve we measured.
```

Rules:
- **Every item needs a caption** that says what to look at and what it means. A caption is not a title.
- **Charts and graphs must answer part of the study's question.** If a chart does not help a reader decide whether the hypothesis held, leave it out.
- **Say which data the numbers come from** (`split`): validation data unless the study says otherwise. The test set is looked at once, at the end (see RECORDS.md).
- **Show the seeds.** Charts draw one dot per row, so keep one row per seed, and readers see the spread.
- **Keep sources small.** `promote` keeps only the columns you use and at most 200 rows. Big files stay on the server.

Then run `record.py check` (it names any wrong column, empty filter or missing caption) and `record.py promote <id>`. `promote` also adds a table of the study's runs, built from the `run.yaml` files.

### Publish a lab note
1. When a study closes, `promote` creates a draft at `showcase/posts/<date>-<id>.md` with `draft: true`.
2. Write it in our voice (see STYLE.md): first person plural, full sentences, every abbreviation spelled out on first use.
3. Remove every `TODO` and HTML comment.
4. Set `draft: false`, and put your name in `authors`.
5. Ask one teammate to read it, then merge it to `main`.

A post about someone else's work, such as the ASF-S authors' paper, is sent to them before it goes live.

### Change the site itself
Work on a branch of `NeuroPulse-Co.github.io` and open a pull request. The pull request is built and link-checked but not deployed. Merging to `main` deploys it. The visual rules are in the site's `DESIGN.md`, and the colour and type tokens are in `src/styles/base.css`.

## Preview before you merge

You need Node 22 or newer. Put the repositories side by side (`NeuroPulse-Co/ASF-S`, `NeuroPulse-Co/AFC-Prune`, `NeuroPulse-Co/NeuroPulse-Co.github.io` and so on).

```bash
cd NeuroPulse-Co.github.io
npm install                          # first time only
SHOWCASE_LOCAL=.. npm run dev        # uses your local showcase/ folders, uncommitted changes included
# open http://localhost:4321
npm run build && npm run check-links # what CI runs
```

Without `SHOWCASE_LOCAL`, the site fetches every `showcase/` from GitHub `main`, exactly as the live build does.

## When something goes wrong

| Symptom | Cause and fix |
|---|---|
| Build fails with `InvalidContentEntryDataError` naming a file and field | A showcase file breaks the standard. Fix the study folder, `promote` again, and run `record.py check`. |
| `check-links` reports a broken link | A relative link in `FINDINGS.md` points to a file that is not in the repo, or a page was renamed. `promote` turns links to repo files into GitHub links, so re-run it. |
| My change merged but the site did not update | Look at the Actions tab of `NeuroPulse-Co.github.io`. If no run started, the `SITE_DISPATCH_TOKEN` org secret is missing or expired. Start the workflow by hand ("Run workflow"); the nightly build also picks it up. |
| A new repository does not appear | It needs a line in `registry.yaml` and a `showcase/` folder on `main`. |
| A lab note does not appear | It still has `draft: true`, or it is not on `main`. |

## Who to ask

The records and site owner is listed in [people.yaml](people.yaml). For a question about the standard itself, open an issue in `NeuroPulse-Co/.github`.
