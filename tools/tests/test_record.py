"""Tests for tools/record.py. Run: uv run --with pytest --with pyyaml pytest tools/tests -q"""
import datetime as dt
import shutil
import sys
from pathlib import Path

import pytest
import yaml

HERE = Path(__file__).resolve().parent
REPO = HERE.parent.parent                      # the .github repo
sys.path.insert(0, str(HERE.parent))
import record  # noqa: E402

TODAY = dt.date.today().isoformat()


@pytest.fixture
def repo(tmp_path, monkeypatch):
    root = tmp_path / "demo-repo"
    std = root / "tools" / "standards"
    std.mkdir(parents=True)
    for f in ("workstreams.yaml", "people.yaml"):
        shutil.copy(REPO / "standards" / f, std / f)
    monkeypatch.setenv("NP_OUTPUTS", str(tmp_path / "out"))
    monkeypatch.setenv("NP_AUTHOR", "Dewmina Wijekoon")
    monkeypatch.setenv("NP_HOST", "testhost")
    monkeypatch.delenv("NP_REPO", raising=False)
    monkeypatch.delenv("NP_ROOT", raising=False)
    monkeypatch.setattr(record, "ADOPTION_DATE", dt.date(2026, 1, 1))  # today's entries use the new format
    return root


def rec(root, *args):
    return record.main(["--root", str(root), *args])


def fill_study(root, study, **over):
    f = root / "studies" / study / "study.yaml"
    s = yaml.safe_load(f.read_text())
    s.update(summary="We test whether the demo works.", question="Does the demo work?",
             hypothesis="It works because it is simple.",
             success_criterion="The command exits with code zero.", status="running")
    s.update(over)
    f.write_text(yaml.safe_dump(s, sort_keys=False))
    return s


def close_study(root, study):
    fill_study(root, study, status="closed-positive", closed=TODAY,
               verdict="The demo works.",
               key_results=[{"label": "exit code", "value": 0, "unit": "code", "split": "val",
                             "n_seeds": 1}])
    (root / "studies" / study / "FINDINGS.md").write_text("We found that it works.\n")


def test_templates_and_standards_parse():
    ws = yaml.safe_load((REPO / "standards" / "workstreams.yaml").read_text())
    assert [w["id"] for w in ws] == ["W0", "W1", "W2", "W3", "W4", "W5"]
    pp = yaml.safe_load((REPO / "standards" / "people.yaml").read_text())
    assert all("name" in p and "role" in p for p in pp)
    s = yaml.safe_load((REPO / "templates" / "study.yaml").read_text())
    for k in record.STUDY_REQUIRED:
        assert k in s, k
    r = yaml.safe_load((REPO / "templates" / "run.yaml").read_text())
    for k in record.RUN_REQUIRED:
        assert k in r, k


def test_new_then_check_ok_with_planned_warnings(repo, capsys):
    assert rec(repo, "new", "demo", "--workstream", "W1", "--owner", "dewminawijekoon") == 0
    s = yaml.safe_load((repo / "studies/demo/study.yaml").read_text())
    assert s["owner"] == ["Dewmina Wijekoon"] and s["status"] == "planned"
    assert rec(repo, "check") == 0                      # TODOs are only warnings while planned
    assert rec(repo, "check", "--strict") == 1


def test_new_rejects_unknown_owner_and_workstream(repo):
    with pytest.raises(SystemExit):
        rec(repo, "new", "demo", "--workstream", "W1", "--owner", "Nobody")
    with pytest.raises(SystemExit):
        rec(repo, "new", "demo", "--workstream", "W9", "--owner", "Dewmina Wijekoon")


@pytest.mark.parametrize("change,expect", [
    ({"status": "finished"}, "status"),
    ({"owner": ["Nobody"]}, "not in standards/people.yaml"),
    ({"workstream": "W9"}, "workstream"),
    ({"criterion": "maybe"}, "criterion"),
    ({"status": "closed-negative"}, "key_results: missing"),
    ({"summary": "TODO: later"}, "TODO placeholder"),
])
def test_check_catches_bad_study(repo, capsys, change, expect):
    rec(repo, "new", "demo", "--workstream", "W1", "--owner", "Dewmina Wijekoon")
    fill_study(repo, "demo", **change)
    assert rec(repo, "check") == 1
    assert expect in capsys.readouterr().out


def test_closed_study_needs_findings(repo, capsys):
    rec(repo, "new", "demo", "--workstream", "W1", "--owner", "Dewmina Wijekoon")
    close_study(repo, "demo")
    assert rec(repo, "check") == 0
    (repo / "studies/demo/FINDINGS.md").unlink()
    assert rec(repo, "check") == 1
    assert "FINDINGS.md" in capsys.readouterr().out


def test_key_results_need_split(repo, capsys):
    rec(repo, "new", "demo", "--workstream", "W1", "--owner", "Dewmina Wijekoon")
    close_study(repo, "demo")
    fill_study(repo, "demo", status="closed-positive",
               key_results=[{"label": "acc", "value": 1, "unit": "%", "n_seeds": 3}])
    assert rec(repo, "check") == 1
    assert "split" in capsys.readouterr().out


def test_run_records_success_and_failure(repo, tmp_path):
    rec(repo, "new", "demo", "--workstream", "W1", "--owner", "Dewmina Wijekoon")
    fill_study(repo, "demo")
    assert rec(repo, "run", "demo", "--tag", "ok", "--seed", "7", "--",
               sys.executable, "-c", "import os; print('hello', os.environ['NP_SEED'])") == 0
    runs = list((tmp_path / "out" / "demo-repo" / "demo").iterdir())
    assert len(runs) == 1
    r = yaml.safe_load((runs[0] / "run.yaml").read_text())
    assert r["exit_code"] == 0 and r["seed"] == 7 and r["author"] == "Dewmina Wijekoon"
    assert r["backfilled"] is False and r["finished"] and r["host"] == "testhost"
    assert "hello 7" in (runs[0] / "console.log").read_text()
    assert rec(repo, "run", "demo", "--tag", "bad", "--",
               sys.executable, "-c", "raise SystemExit(3)") == 3
    bad = next((tmp_path / "out" / "demo-repo" / "demo").glob("*-bad"))
    assert yaml.safe_load((bad / "run.yaml").read_text())["exit_code"] == 3


def test_run_refuses_unknown_author(repo, monkeypatch):
    rec(repo, "new", "demo", "--workstream", "W1", "--owner", "Dewmina Wijekoon")
    monkeypatch.setenv("NP_AUTHOR", "stranger")
    with pytest.raises(SystemExit):
        rec(repo, "run", "demo", "--tag", "x", "--author", "stranger", "--", "true")


def test_harvest_log_promote_check_roundtrip(repo, tmp_path):
    rec(repo, "new", "demo", "--workstream", "W1", "--owner", "Dewmina Wijekoon")
    fill_study(repo, "demo")
    rec(repo, "run", "demo", "--tag", "fig", "--", sys.executable, "-c",
        "import os,pathlib; d=pathlib.Path(os.environ['NP_RUN_DIR']); "
        "(d/'results.csv').write_text('a,b\\n1,2\\n'); (d/'fig.png').write_bytes(b'png'); "
        "(d/'big.pt').write_bytes(b'x')")
    assert rec(repo, "harvest", "--from", str(tmp_path / "out")) == 0
    run_dir = next((repo / "studies/demo/runs").glob("*-fig"))
    assert (run_dir / "results.csv").exists() and (run_dir / "console.tail.log").exists()
    assert not (run_dir / "big.pt").exists() and not (run_dir / "console.log").exists()

    # log: a fresh entry fails check until filled in
    rec(repo, "log", "demo")
    assert rec(repo, "check") == 1
    log = repo / "studies/demo/LOG.md"
    text = log.read_text()
    text = text.replace("<headline: the main finding, in one sentence>", "The demo works")
    text = text.replace("| TODO | TODO | TODO |", "| demo | fig | ok |")
    text = text.replace("- TODO: what we saw, in full sentences, with numbers and their split "
                        "(validation or test).", "- It works on the validation split.")
    text = text.replace("- [ ] TODO", "- [ ] Nothing")
    log.write_text(text)
    assert rec(repo, "check") == 0

    # promote: figures relinked, manifest + draft post generated, check passes
    close_study(repo, "demo")
    (repo / "studies/demo/FINDINGS.md").write_text(
        f"It works.\n\n![The figure](runs/{run_dir.name}/fig.png)\n")
    assert rec(repo, "promote", "demo") == 0
    page = (repo / "showcase/studies/demo.md").read_text()
    assert "../figures/demo/" in page and "repo: demo-repo" in page
    assert list((repo / "showcase/figures/demo").iterdir())
    post = next((repo / "showcase/posts").glob("*-demo.md"))
    assert "draft: true" in post.read_text()
    assert rec(repo, "check") == 0

    # a published post with TODOs fails; a stale manifest fails
    post.write_text(post.read_text().replace("draft: true", "draft: false"))
    assert rec(repo, "check") == 1
    post.write_text(post.read_text().replace("draft: false", "draft: true"))
    (repo / "showcase/manifest.yaml").write_text("repo: other\n")
    assert rec(repo, "check") == 1
    assert rec(repo, "check", "--fix-manifest") == 0


def test_backfilled_run_needs_source(repo, capsys):
    rec(repo, "new", "demo", "--workstream", "W1", "--owner", "Dewmina Wijekoon")
    fill_study(repo, "demo")
    rid = "20261020-0900-server-run01"
    d = repo / "studies/demo/runs" / rid
    d.mkdir(parents=True)
    r = yaml.safe_load((REPO / "templates/run.yaml").read_text())
    r.update(id=rid, study="demo", backfilled=True, source=None)
    (d / "run.yaml").write_text(yaml.safe_dump(r))
    assert rec(repo, "check") == 1
    assert "source" in capsys.readouterr().out
    r["source"] = "cifar10/LOG.md 2026-10-20 entry"
    (d / "run.yaml").write_text(yaml.safe_dump(r))
    assert rec(repo, "check") == 0


def test_legacy_log_entries_are_exempt_but_order_is_checked(repo, capsys):
    rec(repo, "new", "demo", "--workstream", "W1", "--owner", "Dewmina Wijekoon")
    log = repo / "studies/demo/LOG.md"
    log.write_text("# demo log\n\n# 2025-10-21 — later\nfree text\n\n"
                   "# 2025-10-20 12:00 — earlier\nmore\n")
    assert rec(repo, "check") == 0
    log.write_text("# 2025-10-20 — earlier\n\n# 2025-10-21 — later\n")
    assert rec(repo, "check") == 1
    assert "newest first" in capsys.readouterr().out
