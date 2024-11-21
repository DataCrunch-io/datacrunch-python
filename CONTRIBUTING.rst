============
Contributing
============
Any contributions are welcome!

Open new issues at https://github.com/DataCrunch-io/datacrunch-python/issues.

You can open pull requests by following the steps:

Code Contribution:
------------------

1. Fork the `datacrunch-python` repo on GitHub.

2. Clone your fork locally::

    git clone git@github.com:{your_username}/datacrunch-python.git

    cd datacrunch-python

3. Create virtual environment & install this local copy into the virtual environment::
    
    python3 -m venv datacrunch_env && source ./datacrunch_env/bin/activate
    
    python3 setup.py develop

4. Create a new branch:

    if it's a feature::

        git checkout -b feature/new-feature-name

    or a bugfix::

        git checkout -b hotfix/some-bugfix

5. Make your local changes 

6. Install dependencies for test::
    
    pip3 install -e .[test]

    pip3 install -U pytest

7. Run tests::

    pytest

8. Commit and push::

    git commit .am "Detailed commit message"

    git push origin {branch-name}

9. Submit a pull request in GitHub.

Pull Request Guidelines
------------------------

1. The pull request should include tests.
2. Please add documentation docstrings and type hinting to any new feature.

Release Guidelines
------------------------
Some steps for releasing a new version:

1. Update the version in `__version__.py`
2. Add an entry to the CHANGELOG.rst file
3. `git tag vX.Y.Z`
4. `git push master`
5. `git push --tags`
6. `Draft and publish`_ a new release.
7. Check that package is automatically published to `PyPI`_ via `GitHub action`_.

.. _Draft and publish: https://github.com/DataCrunch-io/datacrunch-python/releases
.. _PyPI: https://pypi.org/project/datacrunch/
.. _GitHub action: https://github.com/DataCrunch-io/datacrunch-python/actions/workflows/publish_package.yml
