# Contributing

Thanks for helping improve GitHub World Records.

## Claiming a record

Prefer the **Record Claim** issue template.

Include:

- the exact record category;
- the GitHub username or `owner/repository`;
- the claimed value;
- the public GitHub URL;
- the date/time checked;
- a reproducible verification method.

## Evidence quality

Preferred evidence, strongest first:

1. GitHub API response or reproducible API query.
2. GitHub's own public UI.
3. A transparent public dataset/query.
4. Secondary sources only when GitHub does not expose the metric directly.

Screenshots alone are not sufficient because counts change and screenshots are difficult to reproduce.

## Candidate-based records

GitHub does not provide a global sort for every metric. For those categories, add strong candidates to `data/candidates.json`.

The project will describe the result as **candidate-based** until a global discovery method exists.

## Real projects vs synthetic records

Artificially generated record attempts are valid curiosities, but they must not be mixed with records from ordinary software projects.

For commit records we therefore maintain separate categories.

## Pull requests

Keep PRs focused. If adding a new category, include:

- discovery logic;
- verification logic;
- README label;
- failure behavior when the API is unavailable.

Never commit GitHub tokens or other credentials.
