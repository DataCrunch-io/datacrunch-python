# Contributing

Any contributions are welcome!

Open new issues at https://github.com/DataCrunch-io/datacrunch-python/issues.

You can open pull requests by following the steps:

## Code Contribution

Prerequisite: install [`uv`](https://docs.astral.sh/uv/).

1. Fork the `datacrunch-python` repo on GitHub.

2. Clone your fork locally:

   ```bash
   git clone git@github.com:{your_username}/datacrunch-python.git
   cd datacrunch-python
   ```

3. Set up local environment and install dependencies:

   ```bash
   uv sync
   ```

4. Create a new branch:

   if it's a feature:

   ```bash
   git checkout -b feature/new-feature-name
   ```

   or a bugfix:

   ```bash
   git checkout -b fix/some-bugfix
   ```

5. Make your local changes

6. Run tests:

   ```bash
   uv run pytest
   ```

7. Commit and push:

   ```bash
   git commit -am "Detailed commit message"
   git push origin {branch-name}
   ```

8. Submit a pull request in GitHub.

## Pull Request Guidelines

1. The pull request should include tests.
2. Please add documentation docstrings and type hinting to any new feature.

## Release Guidelines

To release a new version:

1. Bump version:
   ```bash
   uv version --bump minor # also `major` or `patch`
   ```

2. Update `CHANGELOG.md`

3. Commit and push:
   ```bash
   git commit -m v$(uv version --short) CHANGELOG.md pyproject.toml uv.lock
   git tag v$(uv version --short)
   git push origin master
   git push --tags
   ```

4. [Draft and publish](https://github.com/DataCrunch-io/datacrunch-python/releases) a new release.

5. Check that package is automatically published to [PyPI](https://pypi.org/project/datacrunch/) via [GitHub action](https://github.com/DataCrunch-io/datacrunch-python/actions/workflows/publish_package.yml).
