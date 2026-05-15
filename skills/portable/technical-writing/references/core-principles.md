# Core Principles of Technical Writing

## 1. Audience First

Every document exists to help a specific reader accomplish a specific goal. Before writing:
- Name the audience (e.g., "backend engineers new to the payment service")
- State what they should be able to do after reading
- Cut everything that doesn't serve that goal

## 2. Clarity Over Cleverness

- One idea per sentence
- Active voice: "The service processes requests" not "Requests are processed by the service"
- Short paragraphs (3-5 sentences max)
- Define jargon on first use or link to a glossary

## 3. Structure Before Prose

Write the outline first:
1. List the headings
2. Write one sentence summarizing each section
3. Get feedback on the structure before filling in details

This prevents rambling and ensures logical flow.

## 4. Scannable Layout

Readers scan before they read. Help them:
- **Headings** — descriptive, not clever ("How to deploy" not "Blast off!")
- **Lists** — for 3+ related items
- **Tables** — for comparisons or structured data
- **Bold** — for key terms on first introduction
- **Code blocks** — for anything the reader types or reads in a terminal/editor

## 5. Testable Instructions

Every instruction should be verifiable:
- Bad: "Make sure the service is configured correctly"
- Good: "Run `curl localhost:8080/health` and verify the response is `{"status": "ok"}`"

## 6. Link, Don't Duplicate

When information exists elsewhere:
- Link to the source
- Add a one-sentence summary of what the reader will find there
- Never maintain the same information in two places

## 7. Date and Attribute

- Include "Last updated" or "Last reviewed" dates
- Name the author or team responsible
- Make staleness visible so readers can judge reliability
