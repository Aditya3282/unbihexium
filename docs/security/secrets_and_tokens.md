# Secrets and Tokens

This document describes the tokens and secrets used in CI/CD workflows.

## Required Tokens

| Token | Service | Purpose | Required |
|-------|---------|---------|----------|
| `CODECOV_TOKEN` | Codecov | Upload coverage reports | Optional |
| `SCORECARD_TOKEN` | OpenSSF | Security scorecard | Optional |
| `PYPI_API_TOKEN` | PyPI | Package publishing | For releases |

## Configuration

### Codecov

1. Visit [codecov.io](https://codecov.io)
2. Add your repository
3. Copy the upload token
4. Add to GitHub Secrets as `CODECOV_TOKEN`

### OpenSSF Scorecard

1. Create a fine-grained PAT with `public_repo` scope
2. Add to GitHub Secrets as `SCORECARD_TOKEN`

### PyPI Publishing

For trusted publishing (recommended):
1. Go to PyPI project settings
2. Add trusted publisher with GitHub repository details
3. No token needed; OIDC handles authentication

For token-based publishing:
1. Create API token at pypi.org
2. Add to GitHub Secrets as `PYPI_API_TOKEN`

## Workflow Guards

All token-dependent workflow steps include guards:

```yaml
- name: Upload coverage
  if: ${{ secrets.CODECOV_TOKEN != '' }}
  uses: codecov/codecov-action@v4
  with:
    token: ${{ secrets.CODECOV_TOKEN }}
```

This ensures CI does not fail if tokens are not configured.

## Navigation

[Security](../index.md) | [Home](../index.md) | [CI/CD](../development/ci.md)