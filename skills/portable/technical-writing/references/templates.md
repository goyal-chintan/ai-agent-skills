# Document Templates

Starter templates for common document types. Copy the relevant template and fill in the sections.

---

## Concept Explainer Template

```markdown
# [Concept Name]

## Overview

[One paragraph: what is this concept and why does it matter to the reader?]

## How It Works

[Explain the mental model. Use diagrams, analogies, or step-by-step breakdowns.]

## Key Terms

| Term | Definition |
|------|-----------|
| [Term] | [Definition] |

## Examples

### [Example 1 title]

[Concrete scenario showing the concept in action.]

## Related

- [Link to prerequisite concept]
- [Link to follow-up reading]
```

---

## Technical Explainer Template

```markdown
# [System/Component Name]

## Scope

[What this explainer covers. What it deliberately excludes.]

## Context

[Where this fits in the larger system. List or diagram of adjacent components.]

## How It Works

[Step-by-step walkthrough of the mechanism. Use numbered sequences for processes, diagrams for data flow.]

### [Sub-mechanism 1]

[Details.]

### [Sub-mechanism 2]

[Details.]

## Trade-offs and Constraints

| Decision | Why | Limitation |
|----------|-----|-----------|
| [Design choice] | [Rationale] | [Known downside] |

## Operational Details

- **Configuration:** [Key config options and their effects]
- **Failure modes:** [What breaks and how to detect it]
- **Observability:** [Metrics, logs, or traces to monitor]

## References

- [Link to source code]
- [Link to design doc / ADR]
- [Link to related explainers]
```

---

## How-To Guide Template

```markdown
# How to [accomplish task]

## Goal

[One sentence: what the reader will accomplish by following this guide.]

## Prerequisites

- [Tool, access, or knowledge required]

## Steps

1. [First action — imperative verb]
2. [Second action]
3. [Third action]

## Verify

[How to confirm the task succeeded. Include expected output.]

## Troubleshooting

| Symptom | Cause | Fix |
|---------|-------|-----|
| [Error or unexpected result] | [Why it happens] | [What to do] |
```

---

## Confluence Page Template

```markdown
> **Summary:** [2-3 sentences: what this page covers and why it matters.]
>
> **Status:** [Draft | Current | Needs Review]
> **Last reviewed:** [YYYY-MM-DD]
> **Owner:** [Team or person]

## Context

[Background the reader needs to understand this page.]

## Details

[Main content. Use headings, lists, and tables.]

## Action Items

- [ ] [Action item with owner and due date]

## Related

- [Link to related Confluence page]
- [Link to Jira ticket]
```

---

## README Template

```markdown
# [Project Name]

[One-line description of what this project does.]

## Why

[The problem this solves, in 2-3 sentences.]

## Quick Start

\`\`\`bash
# Install
[install command]

# Run
[run command]
\`\`\`

## Usage

[Key commands, API surface, or configuration options.]

## Contributing

[How to make changes: branch strategy, test commands, PR process.]

## License

[License name or "See LICENSE file."]
```

---

## Reference Documentation Template

```markdown
# [API / CLI / Config] Reference

[One sentence: what this reference covers.]

## [Entity Group]

### `[entity-name]`

| Field | Value |
|-------|-------|
| **Type** | [type] |
| **Default** | [default or "required"] |
| **Description** | [What it does] |

**Example:**

\`\`\`
[usage example]
\`\`\`

### `[entity-name-2]`

| Field | Value |
|-------|-------|
| **Type** | [type] |
| **Default** | [default or "required"] |
| **Description** | [What it does] |
```

---

## Architecture / Design Document Template

```markdown
# [Decision or Design Title]

**Date:** [YYYY-MM-DD]
**Author:** [Name or team]
**Status:** [Draft | In Review | Accepted | Superseded by [link]]

## Summary

[1-2 sentences: what was decided or designed, and why it matters.]

## Context

[The problem, constraints, and forces that led to this document. What triggered the need for a decision or design?]

## Options Considered

### Option A: [Name]
- **Pros:** [advantages]
- **Cons:** [disadvantages]

### Option B: [Name]
- **Pros:** [advantages]
- **Cons:** [disadvantages]

## Decision

[What was chosen and why. Reference the option above.]

## Consequences

[What changes as a result — both positive and negative. Include migration steps, operational impact, or follow-up work if applicable.]
```

> **ADR variant:** For repositories using numbered Architecture Decision Records, prefix the title with `ADR-[number]:` and file as `docs/adr/NNNN-title.md`.
