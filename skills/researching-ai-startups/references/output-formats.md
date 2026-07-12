# Output Formats

Honor the user’s requested destination and the project’s existing conventions. Do not hard-code a home directory, private note system, server, or renderer.

## Supported outputs

### One report

Use when the user wants a quick answer rather than a durable collection. Include scope, company comparison or company overview, evidence labels, sources, contradictions, and gaps.

### Markdown collection

Use for durable research. A logical single-company collection may contain:

```text
<company>/
├── index.md
├── company-overview.md
├── founders.md
├── product-and-technology.md
├── business-model.md
├── culture.md
├── careers.md
├── sources/
│   ├── sources.json
│   ├── metadata/
│   └── transcripts/
└── interviews/
```

This is a suggested structure, not a required path. Adapt it to the project.

### Markdown with HTML companions

Create HTML only when the user or project requests it. Markdown remains the editable source unless the project says otherwise. Use the project’s existing HTML renderer or a dedicated HTML-note skill; do not embed a private visual shell in this skill.

Keep one shared page system across a company series. Individual notes may vary in thesis, section order, and diagram shape, but should not invent unrelated typography, navigation, spacing, or page chrome.

## File ownership

- Raw transcripts and metadata remain separate from edited notes.
- One source note covers one important source.
- One coordinator owns shared indexes and source lists during parallel work.
- A company index distinguishes completed notes from source backlog.
- Existing files must be audited before creating new paths or duplicate notes.

## Required index content

A company index should contain:

- research purpose and evidence policy;
- company summary;
- coverage table;
- completed notes;
- source and transcript backlog;
- current facts and important claims;
- contradictions;
- evidence gaps and next research targets;
- related files.

Start from `templates/company-index.md` when creating a collection.

## Completion checks

Before claiming completion:

1. every output file exists at the reported path;
2. important claims have source records;
3. discovered sources and completed notes are not mixed;
4. raw transcript content is not presented as edited analysis;
5. unknowns and contradictions remain visible;
6. links and machine-readable metadata parse successfully;
7. project-specific Markdown or HTML checks pass.
