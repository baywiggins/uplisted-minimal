"""Read-only readiness checks; --write-report records the observed setup status.

This does not install application dependencies, start providers, or run app tests.
Run through scripts/with-tools.sh so project runtimes are selected.
"""
from __future__ import annotations
import argparse
import json
from pathlib import Path
import re
import shutil
import subprocess
import sys
from datetime import datetime, timezone

ROOT = Path(__file__).resolve().parents[1]


def command_version(name: str, args: list[str]) -> tuple[bool, str]:
    executable = shutil.which(name)
    if not executable:
        return False, f'{name} missing from PATH'
    try:
        result = subprocess.run([executable, *args], capture_output=True, text=True, timeout=15, cwd=ROOT)
    except (OSError, subprocess.TimeoutExpired) as exc:
        return False, f'{name}: {type(exc).__name__}'
    lines = (result.stdout or result.stderr).strip().splitlines()
    return result.returncode == 0, lines[0] if lines else f'{name}: no version output'


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--write-report', action='store_true')
    args = parser.parse_args()
    checks: list[tuple[str, bool, str]] = []
    for name, flags, pattern in [
        ('git', ['--version'], r'^git version '),
        ('uv', ['--version'], r'^uv '),
        ('node', ['--version'], r'^v24\.'),
        ('npm', ['--version'], r'^\d+\.'),
        ('python', ['--version'], r'^Python 3\.12\.'),
    ]:
        ok, output = command_version(name, flags)
        checks.append((name, ok and bool(re.search(pattern, output)), output))
    checks.append(('standalone Git repository', (ROOT / '.git').is_dir(), 'local repository; no remote required'))
    for path in ['COPILOT-START.md', 'AGENTS.md', '.github/copilot-instructions.md',
                 '.env.example', 'docs/03-build-plan.md', 'learning/stages.json',
                 'evals/dev/scenarios.jsonl', 'uplisted-interview.code-workspace']:
        checks.append((path, (ROOT / path).is_file(), 'file present' if (ROOT / path).is_file() else 'missing file'))
    try:
        stages = json.loads((ROOT / 'learning/stages.json').read_text())['stages']
        valid = len(stages) == 15 and [s['stage'] for s in stages] == [f'{n:02}' for n in range(1, 16)]
        valid = valid and all((ROOT / row[key]).is_file() for row in stages for key in ('section', 'prompt', 'checkpoint'))
        checks.append(('learning map', valid, '15 ordered stages with existing sections/prompts/checkpoints'))
    except (OSError, ValueError, KeyError, TypeError):
        checks.append(('learning map', False, 'invalid or unreadable stage mapping'))
    app = Path('/Applications/Visual Studio Code.app')
    if sys.platform == 'darwin':
        checks.append(('VS Code', app.is_dir(), 'installed' if app.is_dir() else 'not at standard Applications path'))
        cli = app / 'Contents/Resources/app/bin/code'
        if cli.is_file():
            try:
                result = subprocess.run([str(cli), '--list-extensions'], capture_output=True, text=True, timeout=20)
                installed = result.returncode == 0 and 'github.copilot-chat' in result.stdout.lower().splitlines()
                checks.append(('Copilot extension', installed, 'installed; account sign-in not checked' if installed else 'not detected'))
            except (OSError, subprocess.TimeoutExpired):
                checks.append(('Copilot extension', False, 'extension inventory unavailable'))
    for name, ok, detail in checks:
        print(f'{"PASS" if ok else "FAIL"} | {name} | {detail}')
    passed = all(ok for _, ok, _ in checks)
    print('Application implementation/tests: not started by this folder setup.')
    if args.write_report:
        stamp = datetime.now(timezone.utc).isoformat()
        lines = ['# Prepared folder: setup verification', '', f'Checked at {stamp}.', '',
                 'These checks cover the prepared folder and local prerequisites, not the application or model performance.', '',
                 '| Check | Result | Observed detail |', '|---|---|---|']
        lines += [f'| {name} | {"PASS" if ok else "FAIL"} | {detail.replace("|", "/")} |' for name, ok, detail in checks]
        lines += ['', '## Scope', '',
                  '- Node 24 is installed under ignored `.tools/`; global Node settings are unchanged.',
                  '- Python 3.12 is linked to the existing uv-managed installation.',
                  '- Copilot account sign-in and VS Code workspace trust remain editor-controlled; no account or approval setting was changed.',
                  '- Application dependencies, source code, lockfiles, and tests are intentionally left to Copilot Stage 01 onward.',
                  '- No model/RentCast credentials were read or configured, and no paid provider was invoked.',
                  '- All 15 application stages remain not started until Copilot implements and verifies them.', '',
                  'Rerun: `./scripts/with-tools.sh python scripts/doctor.py`.', '']
        (ROOT / 'docs/SETUP-STATUS.md').write_text('\n'.join(lines))
    return 0 if passed else 1


if __name__ == '__main__':
    raise SystemExit(main())
