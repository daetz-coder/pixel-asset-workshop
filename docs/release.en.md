# First release checklist

[简体中文](release.md) · [Project home](../README.en.md)

- Confirm the license for the code and documentation and add a formal `LICENSE` at the repository root. If the example images and video have separate terms, document them individually in the notice. The current preparation version carries no open license grant. [Sources and distribution](../NOTICE.en.md)
- Review the files intended for release for original pack assets, reference-derived images, private configuration and temporary archives. Git still tracks files that were added before an ignore rule. Run the README commands from a clean checkout and verify that the sample PNG, MP4 and layout JSON are included. [Local example](../README.en.md#reproduce-the-example-offline)
- Wait for CI to pass before creating a public release. Update the project links when the public repository and release URLs are available. Verify public access while signed out.
