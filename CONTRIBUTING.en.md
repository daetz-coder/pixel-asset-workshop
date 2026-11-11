# Contributing

[简体中文](CONTRIBUTING.md) · [Project home](README.md)

Reproducible bug reports, style profiles, batch configs and tool improvements are welcome. Include minimal inputs, expected behavior and actual behavior. For extraction issues, include the layout, output manifest and frame numbers. Share videos, prompts and screenshots you have permission to share publicly.

Install the local dependencies and run `python -m unittest discover -s tests -v`. Try composition changes with the six-unit sample and check video request changes with `--dry-run`. Local tests and CI run without an API key. For new asset examples, record the inputs, exact prompts, tools, outputs, reference sources and review status. Check proportions at the intended in-game size. [Setup](README.md#reproduce-the-example-offline) · [Six-unit sample config](examples/tiny-swords/batch-walk.json)

Before committing, check the diff for local references, credentials, workspace IDs, task links and temporary outputs. For comparisons with source art, share the reproduction commands, annotations or written observations and keep the images containing source frames local. [Sources and distribution](NOTICE.en.md)
