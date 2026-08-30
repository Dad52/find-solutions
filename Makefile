.PHONY: validate test check package

validate:
	python3 scripts/validate_repo.py

test:
	python3 -m unittest discover -s tests -v

check: validate test

package: check
	python3 scripts/package_release.py
