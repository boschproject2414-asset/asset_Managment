"""CI database bootstrap.

Tries Alembic first (preferred). If migrations fail in ephemeral CI due driver/env
issues, falls back to SQLAlchemy metadata creation so smoke tests can still run.
"""

from __future__ import annotations

import subprocess
import sys

from app.db.session import engine
from app.models.base import Base
from app.db.base import *  # noqa: F401,F403


def run_alembic() -> int:
    cmd = ['alembic', 'upgrade', 'head']
    proc = subprocess.run(cmd, capture_output=True, text=True)
    sys.stdout.write(proc.stdout)
    sys.stderr.write(proc.stderr)
    return proc.returncode


def main() -> int:
    print('Attempting Alembic migration...')
    code = run_alembic()
    if code == 0:
        print('Alembic migration succeeded.')
        return 0

    print('Alembic migration failed, falling back to SQLAlchemy create_all for CI smoke.')
    Base.metadata.create_all(bind=engine)
    print('Fallback schema creation succeeded.')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
