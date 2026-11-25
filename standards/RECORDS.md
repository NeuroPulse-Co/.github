# The NeuroPulse record standard

This document explains how we record our research: what we ran, what we found, and what we
concluded. Every NeuroPulse repository follows it. The project website reads only records that
follow it. So if you join the project in the middle, or start a new repository, this page is all
you need.

The tool that creates and checks these records is [`tools/record.py`](../tools/record.py). Each
research repository keeps its own copy at `tools/record.py`. Run it with
`uv run tools/record.py <command>`, which installs PyYAML on the fly, or with any Python that has
PyYAML installed.

---

## 1. The four levels

Our work is organised in four levels, from broadest to smallest:

| Level | What it is | Lives in | Who writes it |
|---|---|---|---|
| **Workstream** | A major research thread that lasts the whole project (W0 to W5). | [`standards/workstreams.yaml`](workstreams.yaml) | The team, by agreement |
| **Study** | One question, with a hypothesis, a success criterion and, at the end, a verdict. | `studies/<study-id>/study.yaml` | The study owner |
| **Run** | One execution of code: a command, a commit, a seed and its outputs. | `studies/<study-id>/runs/<run-id>/run.yaml` | `record.py run` (automatically) |
| **Log entry** | One dated lab-notebook entry: what we ran, what we found, and what comes next. | `studies/<study-id>/LOG.md` | Whoever did the work |

The rule of thumb is that a **study** is the unit we report on. If you can't state a study's
question in one sentence, split it into smaller studies.

### Workstreams

| Id | Title |
|---|---|
| W0 | Foundations: literature review and proposal |
| W1 | Reproducing ASF-S (Artificial Structure Function Search) |
| W2 | AFC (Artificial Functional Connectivity) pruning protocol |
| W3 | Continual learning: hard freezing |
| W4 | Continual learning: metaplastic soft consolidation |
| W5 | Benchmarking and thesis |

[`workstreams.yaml`](workstreams.yaml) is the authoritative list, and also holds each
workstream's question and owner. The people who may be named as owners and authors are listed in
[`people.yaml`](people.yaml).

---

## 2. Repository layout

```
<repo>/
  README.md                 what the repo is for, its workstream, a table of its studies
  studies/
    <study-id>/
      study.yaml            the study record (section 3)
      LOG.md                the lab log, newest entry first (section 5)
      FINDINGS.md           written when the study closes (section 6)
      runs/<run-id>/        one folder per run: run.yaml + small outputs (section 4)
      ...code...            the study's own code, if it has any
  showcase/                 the curated public copy the website reads (section 7); main branch only
  tools/record.py           vendored copy of the tool
  tools/standards/          vendored copies of workstreams.yaml and people.yaml
```

**IDs.**
- A study id is lowercase letters, digits and hyphens, and must equal its folder name, for example
  `cifar10-repro`. Its global id is `<repo>/<study-id>`.
- A run id is `YYYYMMDD-HHMM-<host>-<tag>`, for example `20261124-1340-server-clean_s42`.
  `record.py run` creates it for you.

**Large files never go into git.** Checkpoints, activation dumps and `.npy`/`.npz` arrays stay on
the machine that made them. `run.yaml` records where they are (`outputs_dir`). Only files up to
2 MB of these types are copied into the repository: yaml, csv, json, png, svg, md and txt.

---

## 3. `study.yaml`

Start a study with:

```bash
uv run tools/record.py new <study-id> --workstream W2 --owner "Your Name" --title "A question-like title"
```

Then fill in the fields marked TODO **before the first run**. A filled example is in
[`templates/study.yaml`](../templates/study.yaml).

| Field | Required | Meaning |
|---|---|---|
| `id` | always | Equals the folder name. |
| `title` | always | A short title, ideally phrased as the question. |
| `workstream` | always | An id from `workstreams.yaml`. |
| `status` | always | One of `planned`, `running`, `closed-positive`, `closed-negative`, `closed-inconclusive`, `abandoned`. |
| `owner` | always | A list of names from `people.yaml`. |
| `started` | always | A date, `YYYY-MM-DD`. |
| `summary` | always | One or two plain-language sentences. The website shows this on cards. |
| `question` | always | The single question this study answers. |
| `hypothesis` | always | What we expect, and why. |
| `success_criterion` | always | The measurable result that would confirm the hypothesis. |
| `criterion` | always | `pre_registered` if the success criterion was written before any results existed, otherwise `post_hoc`. |
| `code` | always | Paths to the code this study uses. Use `[]` for a study without code, such as a literature review. |
| `closed` | when closed or abandoned | The date it closed. |
| `verdict` | when closed or abandoned | Two or three sentences: what we concluded, or why we stopped. |
| `key_results` | when closed | One to five headline numbers (see below). |
| `paper_targets`, `links` | optional | Numbers from a paper we compare against, and related links. |

**Statuses.**
- `closed-positive`: the hypothesis held.
- `closed-negative`: the hypothesis did not hold, or the result did not reproduce. A negative
  result is a result, and we report it just as fully.
- `closed-inconclusive`: the evidence can't separate the outcomes, for example because the
  differences are within seed-to-seed noise.
- `abandoned`: we stopped without an answer. The verdict says why.

**`key_results`** are the numbers the website puts on a study's scorecard. Each one needs:
- `label`
- `value` (a number)
- `unit`
- `split`, which says which data the number comes from: `val`, `test`, or `none` for numbers not measured on data (parameter counts, passing tests)
- `n_seeds`

Each one may also have `std` or `ci95`, and `compare: {label, value}`, for example the paper's
number.

---

## 4. Runs

### Recording a run

Wrap the command you would normally run:

```bash
uv run tools/record.py run <study-id> --tag <short-tag> --seed 42 -- python train.py --lr 0.01
```

`record.py run` does the following:

1. It creates `$NP_OUTPUTS/<repo>/<study-id>/<run-id>/`. `NP_OUTPUTS` defaults to `./outputs`,
   which is gitignored. On the server we set `NP_OUTPUTS=~/np_outputs`, so outputs stay outside
   the repository and `git pull` never conflicts with them.
2. Before starting, it writes `run.yaml` with the author, host, start time, git commit, branch,
   whether the working tree had uncommitted changes (`dirty`), the command, the seed, the GPU and
   the Python and PyTorch versions. A crashed run still leaves a record.
3. It runs the command with these environment variables set: `NP_RUN_DIR` (write your outputs
   here), `NP_RUN_ID`, `NP_STUDY` and `NP_SEED`. Everything the command prints goes to the screen
   and to `console.log`.
4. Afterwards it adds the finish time, exit code and duration to `run.yaml`.

**Older scripts** that write somewhere else, for example `$ASFS_OUTPUTS/run01/...`, are wrapped
with `--outputs-dir <that folder>`. `harvest` then also collects from there.

**On the server**, set these once in your shell profile:
- `export NP_AUTHOR="Your Name"`. The server's login name isn't in `people.yaml`, and
  `record.py run` refuses to start without a known author.
- `export NP_HOST=server`.
- `export NP_OUTPUTS=~/np_outputs`.

### Bringing results home

The GPU server can `git pull` but never commits. Results travel to the laptop, where we commit
them:

```bash
uv run tools/record.py harvest --from user@server:/home/user/np_outputs   # all studies
uv run tools/record.py harvest cifar10-repro --from user@server:/home/user/np_outputs
```

`harvest` copies each run's `run.yaml`, its small outputs, and the last 200 lines of its console
output (`console.tail.log`) into `studies/<study-id>/runs/<run-id>/`. Large files stay on the
server.

### Backfilled runs

Runs made before this standard existed may be recorded by hand from
[`templates/run.yaml`](../templates/run.yaml). They **must** say `backfilled: true` and give a
`source`, which names where the information came from (a LOG entry, a `gate.json`, a
`RUN_INFO.md`). Unknown values are `null`; we never guess them. This keeps reconstructed records
from passing as original ones.

---

## 5. `LOG.md`

The lab log is the day-to-day record. Add an entry whenever you run something, find something,
or decide something:

```bash
uv run tools/record.py log <study-id>
```

This inserts a pre-filled skeleton at the top of the log. Its format, also shown in
[`templates/LOG-entry.md`](../templates/LOG-entry.md), is:

```markdown
# 2026-11-26 — The main finding of this session, as one full sentence
Study: <study-id> · Author: <name> · Host: <host> · Commit: <hash> · Runs: <run ids or none>

## Run
## Findings
## Next
```

The rules are:
- Entries go newest first.
- Headings are `# YYYY-MM-DD — ` or `# YYYY-MM-DD HH:MM — `, followed by the headline.
- Entries dated **2026-11-25 or later** must have the `Study:` line and the three sections, and
  must contain no `TODO` left over from the skeleton.
- Older entries keep their original format.
- Anything above the first dated heading, such as a title or a comment, is allowed.

---

## 6. Closing a study: `FINDINGS.md`

When a study answers its question:

1. Set `status` to `closed-positive`, `closed-negative` or `closed-inconclusive`, and fill in
   `closed`, `verdict` and `key_results`.
2. Write `FINDINGS.md`, following [`templates/FINDINGS.md`](../templates/FINDINGS.md). It has
   five sections: verdict, evidence, why we think this happened, limits, and what this means for
   the project. Write it for a reader who has never seen the log. It becomes the study's page on
   the website.
3. Images are linked relative to the study folder, for example
   `![caption](runs/<run-id>/fig.png)`.

---

## 7. Publishing: `showcase/`

`showcase/` is the curated, public part of a repository. The website reads it **only from the
`main` branch**. Never edit `showcase/manifest.yaml` or `showcase/studies/*.md` by hand, because
they are generated.

```bash
uv run tools/record.py promote <study-id>
```

`promote` does four things:
- It writes `showcase/studies/<id>.md` from `study.yaml` and `FINDINGS.md`.
- It copies the figures that `FINDINGS.md` links to into `showcase/figures/<id>/`.
- The first time a study is closed, it creates a **draft** blog post,
  `showcase/posts/<date>-<id>.md`, with `draft: true`.
- It regenerates `showcase/manifest.yaml`.

You can also promote a `running` study. It then appears on the website as "in progress".

A post is published by editing it until it follows [STYLE.md](STYLE.md) and contains no `TODO`,
then setting `draft: false`. Post frontmatter is:
- `title`
- `date`
- `authors` (names from `people.yaml`)
- `workstream`
- `summary`
- optionally `study`, `cover` and `draft`

The file name is `YYYY-MM-DD-<slug>.md`. Posts are written to double as thesis-chapter drafts.

---

## 8. Checking

```bash
uv run tools/record.py check            # errors fail; warnings are printed
uv run tools/record.py check --strict   # warnings fail too
```

`check` validates every `study.yaml`, `run.yaml`, `LOG.md` and `showcase/` file against this
document, including names and workstreams, required fields, image links and an up-to-date
manifest. It runs in CI on every push and pull request (the `records` workflow), so a broken
record can't reach `main`. Errors look like
`studies/x/study.yaml: status: 'done' must be one of [...]`.

---

## 9. Integrity rules

These rules exist so that our records can be trusted by examiners, reviewers and our future
selves:

1. **Pre-registration is honest.** `criterion: pre_registered` only if the success criterion was
   written before any results existed. Otherwise it is `post_hoc`.
2. **Every number says where it comes from**: validation or test split, and how many seeds.
3. **The test set is looked at once**, at the end of a study, unless the study protocol says
   otherwise. Tuning uses validation data.
4. **Reconstructed records are labelled** as `backfilled: true` with a `source`.
5. **Negative results are recorded and published** with the same care as positive ones.
6. **Uncommitted code is flagged.** A run with `dirty: true` is valid but shows a warning.
   Commit before long runs.

---

## 10. Keeping the tool and the standard up to date

The canonical copies of `record.py`, `workstreams.yaml` and `people.yaml` live in
[NeuroPulse-Co/.github](https://github.com/NeuroPulse-Co/.github). In a research repository, run:

```bash
uv run tools/record.py self-update      # shows a diff for each file and asks before replacing
```

To change the standard itself, open a pull request on `NeuroPulse-Co/.github` that updates this
document, `record.py` and its tests together.

New repositories are created from the
[research-template](https://github.com/NeuroPulse-Co/research-template) repository, which already
contains the tool, the standards and the CI workflow.
