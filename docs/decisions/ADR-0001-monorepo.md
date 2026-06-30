# ADR-0001 — Use a Monorepo for Jacob 0.1

## Status

Accepted

## Context

The initial idea was to create multiple repositories:

- jacob-core
- jacob-memory
- jacob-connect
- jacob-agents
- jacob-voice

However, Jacob 0.1 is being developed by a very small founding team. Multiple repositories would add unnecessary coordination, permissions and versioning complexity.

## Decision

Jacob 0.1 will use a single repository:

```text
jacob
```

With internal folders for each module.

## Consequences

### Positive

- Faster development.
- Simpler organization.
- Easier documentation.
- Easier onboarding.

### Negative

- May need to split services later.

## Review

This decision should be reviewed when the project has multiple active developers or production services requiring independent deployment.