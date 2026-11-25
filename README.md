# NeuroPulse-Co/.github

The shared foundation for every NeuroPulse repository. GitHub uses this repository in three ways:
- it shows `profile/README.md` on the [organisation page](https://github.com/NeuroPulse-Co)
- it applies the issue and pull-request templates to every repository that has none of its own
- it hosts the reusable workflows that other repositories call

| Path | What it is |
|---|---|
| [`standards/RECORDS.md`](standards/RECORDS.md) | **The record standard**: how we record studies, runs, logs and results |
| [`standards/STYLE.md`](standards/STYLE.md) | How we write anything a reader outside the team will see |
| [`standards/PLAN.md`](standards/PLAN.md) | The project-wide plan: architecture, research plan, timeline and rollout |
| [`standards/workstreams.yaml`](standards/workstreams.yaml) | The authoritative list of workstreams (W0 to W5) |
| [`standards/people.yaml`](standards/people.yaml) | Who can be named as a study owner or an author |
| [`templates/`](templates/) | Filled examples of every record type |
| [`tools/record.py`](tools/record.py) | The tool that creates, collects, checks and publishes records (tests in `tools/tests/`) |
| `.github/workflows/validate-records.yml` | Reusable workflow: `record.py check` |
| `.github/workflows/notify-site.yml` | Reusable workflow: tells the website to rebuild when `showcase/` changes |
| `profile/README.md` | The organisation landing page |

## Changing the standard

Open a pull request that changes `RECORDS.md`, `record.py` and `tools/tests/` together. Run the
tests with:

```bash
uv run --no-project --with pytest --with pyyaml pytest tools/tests -q
```

After it merges, each research repository picks up the change with
`uv run tools/record.py self-update`.
