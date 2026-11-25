## What this changes

<!-- One or two sentences. Link the study: studies/<id>/ -->

## Records checklist

- [ ] A `LOG.md` entry describes what was run, found and decided (`record.py log <study>`)
- [ ] New runs have a `run.yaml` (recorded with `record.py run`, brought in with `record.py harvest`)
- [ ] `uv run tools/record.py check` passes
- [ ] If a study closed: `status`, `closed`, `verdict`, `key_results` and `FINDINGS.md` are filled in, and `record.py promote <study>` was run
- [ ] Public text (`FINDINGS.md`, posts, README) follows [STYLE.md](https://github.com/NeuroPulse-Co/.github/blob/main/standards/STYLE.md): full sentences, abbreviations spelled out, every number with its split and seed count
- [ ] No large files (checkpoints, arrays) added; no secrets
