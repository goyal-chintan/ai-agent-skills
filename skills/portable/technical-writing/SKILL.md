---
name: technical-writing
description: "Use when creating or improving technical documentation, concept docs, concept explainers, technical explainers, Confluence pages, internal docs, wiki articles, or READMEs. Applies plain-language principles, audience framing, and doc-type-first workflows for clear writing and structured technical writing."
---

# Technical Writing

## Overview

Produce clear, structured, audience-aware documentation. Every document starts by identifying its **type** and **audience**, then follows the workflow for that type.

This skill covers:
- Technical documentation (API docs, architecture docs, runbooks)
- Concept explainers and onboarding guides
- Confluence pages and internal knowledge-base articles
- READMEs and project documentation
- General clear-writing improvements

## Core Principles

Load `references/core-principles.md` for the full set. Summary:

1. **Audience first** — identify who reads this and what they need to do after reading.
2. **One idea per sentence** — short sentences, active voice, no jargon without definition.
3. **Structure before prose** — outline headings and key points before writing paragraphs.
4. **Scannable** — use headings, lists, tables, and bold for key terms.
5. **Testable** — every instruction should be verifiable by the reader.

## Workflow

### Step 1: Identify Document Type

Before writing anything, classify the document. Load `references/document-types.md` for the full catalog. Common types:

| Type | Purpose | Key sections |
|------|---------|-------------|
| Concept explainer | Teach a mental model | Overview, How it works, Examples, Related |
| Technical explainer | Explain system internals | Scope, Context, Mechanism, Trade-offs, Ops details |
| How-to guide | Walk through a task | Prerequisites, Steps, Verification |
| Reference | Look up details | Organized by entity, consistent format |
| Confluence page | Share team knowledge | Context, Details, Action items |
| README | Orient newcomers | What, Why, Quick start, Contributing |
| Architecture / design document | Record decisions | Context, Options, Decision, Consequences |

### Step 2: Frame Audience and Purpose

Answer these before drafting:

1. **Who** is the reader? (role, experience level)
2. **What** do they need to accomplish after reading?
3. **What** do they already know? (skip what's obvious to them)
4. **Where** will they read this? (IDE, browser, terminal)

### Step 3: Outline First

Write the heading structure and one-line summary per section before any prose. Get approval on the outline if collaborating.

### Step 4: Draft

Follow the template for the identified document type. Load `references/templates.md` for starter templates.

Rules during drafting:
- Active voice by default
- Present tense for descriptions, imperative for instructions
- Define acronyms on first use
- One topic per paragraph
- Code examples must be runnable or clearly marked as pseudocode
- Link to sources rather than duplicating content

### Step 5: Review Checklist

Before delivering any document, verify:

- [ ] Title clearly states what the document covers
- [ ] Audience and purpose are stated or obvious from context
- [ ] Headings form a scannable table of contents
- [ ] No undefined jargon or acronyms
- [ ] Instructions are testable / verifiable
- [ ] Code examples are syntactically correct
- [ ] Links are valid and point to the right target
- [ ] Length is appropriate — cut anything that doesn't serve the reader

## Concept Docs

Use when the reader needs to understand *what something is* and *why it matters* before they can act.

1. **Open with a one-paragraph overview** — state what the concept is and why the reader should care, in plain language.
2. **Explain how it works** — build a mental model. Use analogies, diagrams, or step-by-step breakdowns. Avoid implementation details unless they clarify the model.
3. **Define key terms** — if the concept introduces domain vocabulary, add a short definitions table.
4. **Show concrete examples** — at least one scenario that demonstrates the concept in a real context the reader recognizes.
5. **Link to related concepts** — prerequisites the reader may need and follow-up topics for deeper understanding.

**Pitfalls to avoid:**
- Jumping into details before establishing the big picture
- Mixing "how it works" with "how to use it" — keep concept docs separate from how-to guides
- Assuming motivation — always answer "why should I care?" early

## Technical Explainers

Use when the reader needs a deeper, implementation-aware explanation of a system, protocol, or architecture component.

1. **State the scope** — what this explainer covers and what it deliberately excludes.
2. **Provide context** — where this component fits in the larger system. A simple diagram or list of adjacent components helps.
3. **Walk through the mechanism** — explain the internals step by step. Use numbered sequences for processes, diagrams for data flow.
4. **Highlight trade-offs and constraints** — why was it built this way? What are the known limitations?
5. **Include operational details** — configuration, failure modes, observability hooks — anything an engineer needs to work with this in production.
6. **End with references** — link to source code, design docs, and related explainers.

**When to use a technical explainer vs. a concept doc:**
- Concept doc → teaches a mental model to a broad audience; implementation-agnostic
- Technical explainer → dives into how a specific system implements the concept; audience is engineers working on or near the system

## Confluence Pages

When writing for Confluence specifically:

1. **Start with a summary panel** — 2-3 sentences at the top answering "what is this and why should I care?"
2. **Use Confluence macros** — status labels, expand sections for optional detail, info/warning panels
3. **Link liberally** — connect to related pages, Jira tickets, and external docs
4. **Add a "Last reviewed" date** — Confluence pages rot; make staleness visible
5. **Keep pages focused** — one topic per page; use parent/child hierarchy for organization

## External References

Load `references/source-guides.md` for curated links and summaries of:
- Google Technical Writing courses
- Microsoft Writing Style Guide
- Write the Docs community guides
- Plain-language guidance (PlainLanguage.gov lineage)

## Anti-Patterns

- **Wall of text** — no headings, no lists, no visual breaks
- **Curse of knowledge** — assuming the reader knows what you know
- **Copy-paste documentation** — duplicating content instead of linking
- **Undated pages** — no way to tell if information is current
- **Passive instructions** — "the button should be clicked" instead of "click the button"
