# Document Types

## Concept Explainer

**Purpose:** Teach the reader a mental model or explain how something works.

**When to use:** The reader needs to understand *why* before they can act.

**Structure:**
1. **Overview** — one paragraph: what is this and why does it matter?
2. **How it works** — the mental model, with diagrams if helpful
3. **Key terms** — definitions table if there's domain vocabulary
4. **Examples** — concrete scenarios showing the concept in action
5. **Related** — links to prerequisite or follow-up reading

---

## Technical Explainer

**Purpose:** Provide an implementation-aware explanation of a system, protocol, or architecture component.

**When to use:** The reader is an engineer who needs to understand how a specific system works internally — its mechanisms, trade-offs, and operational characteristics.

**Structure:**
1. **Scope** — what this explainer covers and what it excludes
2. **Context** — where this component fits in the larger system
3. **Mechanism** — step-by-step walkthrough of internals (processes, data flow)
4. **Trade-offs and constraints** — why it was built this way, known limitations
5. **Operational details** — configuration, failure modes, observability
6. **References** — links to source code, design docs, related explainers

**vs. Concept Explainer:** A concept explainer teaches a mental model to a broad audience and is implementation-agnostic. A technical explainer dives into how a specific system implements the concept.

---

## How-To Guide

**Purpose:** Walk the reader through completing a specific task.

**When to use:** The reader needs to *do* something and wants step-by-step instructions.

**Structure:**
1. **Goal** — one sentence: what the reader will accomplish
2. **Prerequisites** — what they need before starting (tools, access, knowledge)
3. **Steps** — numbered, imperative, one action per step
4. **Verify** — how to confirm the task succeeded
5. **Troubleshooting** — common errors and fixes

---

## Reference Documentation

**Purpose:** Let the reader look up specific details quickly.

**When to use:** The reader already knows the concept and needs precise information.

**Structure:**
- Organized by entity (endpoint, config key, CLI flag)
- Consistent format for every entry (name, type, default, description)
- Alphabetical or logical grouping
- No narrative — just facts

---

## Confluence Page

**Purpose:** Share team knowledge, decisions, or processes.

**When to use:** Information needs to be discoverable by the team in a wiki.

**Structure:**
1. **Summary** — 2-3 sentences: what and why
2. **Context** — background the reader needs
3. **Details** — the main content, using headings and lists
4. **Action items** — if applicable
5. **Related** — links to related pages, Jira tickets; include status, owner, and last-reviewed date in the summary panel

---

## README

**Purpose:** Orient newcomers to a project or repository.

**When to use:** Someone encounters the repo for the first time.

**Structure:**
1. **Project name** and one-line description
2. **Why** — the problem it solves
3. **Quick start** — minimal steps to get running
4. **Usage** — key commands or API surface
5. **Contributing** — how to make changes
6. **License** — if applicable

---

## Architecture / Design Document

**Purpose:** Record technical decisions and system design.

**When to use:** A design needs review, or future engineers need to understand past decisions.

**Structure:**
1. **Summary** — what was decided and why
2. **Context** — the problem and constraints
3. **Options considered** — with trade-offs
4. **Decision** — what was chosen and why
5. **Consequences** — what changes as a result
