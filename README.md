# ProTemp.AI — Project Template

ProTemp is a ready-to-use **project template** that provides a standardised folder structure, document templates, and AI-agent personas for managing the full lifecycle of a software project — from vision and requirements through architecture, implementation, testing, and documentation.

Clone or fork this repository to bootstrap a new project with sensible defaults for project management, quality assurance, and architecture documentation.

## Key Features

- **Structured project management** — predefined folders for vision, planning boards, roadmaps, and reporting.
- **Arc42-based architecture docs** — both a vision layer (what should be) and an implementation layer (what is), following the proven 12-section arc42 template.
- **Document templates** — ready-made templates for requirements, architecture decisions, constraints, work items, test reports, security reviews, technical debt records, and more.
- **Documentation standards** — a central registry that defines document types, naming conventions, storage locations, and linked templates.
- **Kanban-style planning board** — work items flow through `funnel → analyze → ready → backlog → implementing → done` (plus obsoleted/rejected).
- **AI-agent personas** — seven specialised GitHub Copilot agent definitions (Architect, Developer, Tester, Requirements, Security, Documentation, License) with clear responsibilities, inputs, outputs, and limitations.
- **Workflow definitions** — documented workflows for requirements engineering and implementation that agents can follow autonomously.

## Repository Structure

```
ProTemp/
├── .github/
│   ├── copilot-instructions.md          # Copilot agent orchestration rules
│   └── agents/                          # Agent persona definitions
│       ├── architect.agent.md
│       ├── developer.agent.md
│       ├── documentation.agent.md
│       ├── license.agent.md
│       ├── requirements.agent.md
│       ├── security.agent.md
│       └── tester.agent.md
│
├── project_management/
│   ├── 01_guidelines/                   # Standards, templates, workflows
│   │   ├── documentation_standards/
│   │   │   ├── documentation-standards.md
│   │   │   └── doc_templates/           # All document templates
│   │   └── workflows/                   # Process workflow definitions
│   ├── 02_project_vision/               # Vision & requirements
│   │   ├── 01_project_goals/
│   │   ├── 02_requirements/             # Funnel → Analyze → Accepted / Obsoleted / Rejected
│   │   ├── 03_architecture_vision/      # Arc42 sections 1–12 (target state)
│   │   └── 04_security_concept/
│   ├── 03_plan/
│   │   ├── 01_roadmap/
│   │   └── 02_planning_board/           # Kanban columns (funnel → done)
│   └── 04_reporting/
│       ├── 01_architecture_reviews/
│       ├── 02_tests_reports/
│       └── 03_security_reviews/
│
├── project_documentation/
│   ├── 01_architecture/                 # Arc42 sections 1–12 (implemented state)
│   ├── 02_ops_guide/
│   ├── 03_user_guide/
│   └── 04_dev_guide/
│
├── CREDITS.md
├── LICENSE.md
└── README.md
```

## Getting Started

1. **Clone or fork** this repository.
2. Replace placeholder content in `project_management/02_project_vision/01_project_goals/` with your project's vision.
3. Start deriving requirements — the Requirements agent or the workflow in `project_management/01_guidelines/workflows/requirements_engineering_workflow.md` will guide you.
4. Use the document templates in `project_management/01_guidelines/documentation_standards/doc_templates/` whenever you create a new artifact.
5. Consult `project_management/01_guidelines/documentation_standards/documentation-standards.md` for naming conventions and storage locations.

## AI Agent System

ProTemp ships with seven GitHub Copilot agent personas defined in `.github/agents/`. An orchestration layer in `.github/copilot-instructions.md` routes tasks to the most appropriate agent automatically.

| Agent | Responsibility |
|-------|---------------|
| **Architect** | Architecture vision & implementation compliance |
| **Developer** | Backlog selection, implementation, and close-out |
| **Tester** | Test planning, execution, and reporting |
| **Requirements** | Requirements elicitation and specification |
| **Security** | Security reviews and security concept maintenance |
| **Documentation** | User, ops, and dev guide maintenance |
| **License** | License compliance and dependency auditing |

## License

This project is licensed under the [Creative Commons Attribution-ShareAlike 4.0 International (CC BY-SA 4.0)](https://creativecommons.org/licenses/by-sa/4.0/) license. See [LICENSE.md](LICENSE.md) for details.

## Credits

Architecture documentation structure based on the [arc42](https://arc42.org) template by Dr. Gernot Starke and Dr. Peter Hruschka. See [CREDITS.md](CREDITS.md).
