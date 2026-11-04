.PHONY: check test install clean help
PY ?= python3

help:
	@echo "make check    Validate skills and run tests"
	@echo "make test     Run the test suite only"
	@echo "make install  Copy skills/* into .claude/skills/"
	@echo "make clean    Remove caches"

check:
	$(PY) scripts/validate_skills.py
	$(PY) -m unittest discover -s tests -v

test:
	$(PY) -m unittest discover -s tests -v

install:
	@mkdir -p .claude/skills
	@for d in skills/*/; do \
		name=$$(basename $$d); \
		rm -rf ".claude/skills/$$name"; \
		cp -R "$$d" ".claude/skills/$$name"; \
		echo "installed $$name"; \
	done
	@echo "done — skills are in .claude/skills/"
	@echo "note: shared/ docs stay at the repo root; run Claude Code from there."

clean:
	@find . -name __pycache__ -type d -prune -exec rm -rf {} + 2>/dev/null || true
	@rm -rf .pytest_cache
	@echo "clean"
