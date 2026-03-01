# ProTemp.AI — Project Template

ProTemp is a ready-to-use **project template** that provides a standardised folder structure, document templates, and AI-agent personas for managing the full lifecycle of a software project — from vision and requirements through architecture, implementation, testing, and documentation.

Clone or fork this repository to bootstrap a new project with sensible defaults for project management, quality assurance, and architecture documentation.

## Key Features

- **Structured project management** — predefined folders for vision, planning boards, roadmaps, and reporting.
- **Arc42-based architecture docs** — both a vision layer (what should be) and an implementation layer (what is), following the proven 12-section arc42 template.
- **Document templates** — ready-made templates for requirements, architecture decisions, constraints, work items, test reports, security reviews, security analysis scopes, technical debt records, and more.
- **Documentation standards** — a central registry that defines document types, naming conventions, storage locations, and linked templates.
- **Kanban-style planning board** — work items flow through `funnel → analyze → ready → backlog → implementing → done` (plus obsoleted/rejected).
- **AI-agent personas** — seven specialised GitHub Copilot agent definitions (Architect, Developer, Tester, Requirements, Security, Documentation, License) with clear responsibilities, inputs, outputs, and limitations.
- **Workflow definitions** — documented workflows for requirements engineering and implementation that agents can follow autonomously.

## Repository Structure

```
ProTemp/
├── .devcontainer/                       # VS Code dev container configuration
│   ├── devcontainer.json                # Container settings and extensions
│   ├── Dockerfile                       # Ubuntu 24.04 LTS with dev tools
│   └── README.md                        # Container documentation
│
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
│   │   └── 04_security_concept/         # Security methodology, asset catalog, threat models
│   │       ├── 01_security_concept.md   # STRIDE/DREAD framework
│   │       ├── 02_asset_catalog.md      # CIA-rated asset inventory
│   │       └── SAS_XXXX_*.md            # Security analysis scopes (threat models)
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
├── AGENTS.md                            # Central registry of all available agents
├── CREDITS.md
├── LICENSE.md
└── README.md
```

## Development Environment

ProTemp includes a pre-configured development container for VS Code that provides a consistent development environment across all platforms.

### Using the Dev Container

**Prerequisites:**
- [Visual Studio Code](https://code.visualstudio.com/)
- [Dev Containers extension](https://marketplace.visualstudio.com/items?itemName=ms-vscode-remote.remote-containers)
- [Docker Desktop](https://www.docker.com/products/docker-desktop/) or compatible container runtime

**Setup:**
1. Clone or fork this repository
2. Open the folder in VS Code
3. When prompted, click "Reopen in Container" (or use Command Palette: `Dev Containers: Reopen in Container`)
4. VS Code will build and start the container automatically

**Included Tools:**
- Ubuntu 24.04 LTS base
- Git and GitHub CLI
- Python (latest) - for running project tools
- Node.js LTS - for JavaScript/TypeScript tooling
- Bash shell with common utilities

See [.devcontainer/README.md](.devcontainer/README.md) for configuration details.

### Alternative Setup

If you prefer not to use the dev container, you can work with ProTemp directly on your host machine. The only requirement is **Python 3.7+** for running the utility scripts in `project_management/00_tools/`.

## Getting Started

### Quick Start

1. **Clone or fork** this repository
2. **(Optional)** Set up the development environment (see [Development Environment](#development-environment) above)
3. **Replace placeholder content** in `project_management/02_project_vision/01_project_goals/` with your project's vision and goals
4. **Start deriving requirements** — use the Requirements agent or follow the workflow in [project_management/01_guidelines/workflows/requirements_engineering_workflow.md](project_management/01_guidelines/workflows/requirements_engineering_workflow.md)
5. **Use document templates** from [project_management/01_guidelines/documentation_standards/doc_templates/](project_management/01_guidelines/documentation_standards/doc_templates/) whenever creating artifacts
6. **Follow naming conventions** defined in [project_management/01_guidelines/documentation_standards/documentation-standards.md](project_management/01_guidelines/documentation_standards/documentation-standards.md)
7. **Review** [AGENTS.md](AGENTS.md) to understand available agents, workflows, and supporting standards

### Understanding the Template Structure

ProTemp separates **vision** (what should be) from **reality** (what is):

- **`project_management/02_project_vision/`** — Target state: goals, requirements, architecture vision, and security concept
- **`project_documentation/01_architecture/`** — Current state: implemented architecture following arc42
- **`project_management/03_plan/02_planning_board/`** — Work items flow through: funnel → analyze → ready → backlog → implementing → done

This separation ensures your vision remains stable while implementation evolves incrementally.

## Tools

ProTemp includes Python utility scripts in [project_management/00_tools/](project_management/00_tools/) to automate project maintenance tasks. These tools help maintain reference integrity and support safe refactoring of project structure.

**Requirements:** Python 3.7+

### File/Directory Rename and Reference Updater

Automatically rename or move files and directories while updating all references throughout the workspace. Essential for refactoring project structure without breaking links.

```bash
# Preview changes before applying (recommended)
python3 project_management/00_tools/rename_and_update_refs.py \
  old_file.md new_file.md --dry-run

# Rename a file and update all references
python3 project_management/00_tools/rename_and_update_refs.py \
  old_file.md new_file.md

# Move a directory and update all nested file references  
python3 project_management/00_tools/rename_and_update_refs.py \
  old_folder/ new_folder/
```

**Features:**
- Updates references in markdown links, code, configs, and documentation
- Handles both files and directories recursively
- Supports various reference formats (plain text, quoted, backticks, markdown links)
- Dry-run mode to preview changes before applying
- Automatic workspace detection

### Broken Reference Finder

Scan the workspace for broken references — links and textual references pointing to files that don't exist.

```bash
# Find all broken references
python3 project_management/00_tools/find_broken_refs.py

# Show detailed output with path resolution
python3 project_management/00_tools/find_broken_refs.py --verbose

# Output in different formats (full, simple, json)
python3 project_management/00_tools/find_broken_refs.py --format simple
```

**Features:**
- Detects broken markdown links, quoted paths, and backticked references
- Scans documentation, code, and configuration files
- Reports line numbers and reference types
- Multiple output formats (full, simple, JSON)
- Useful for pre-commit checks and CI/CD pipelines
- Exit code 1 if broken references found (CI-friendly)

See [project_management/00_tools/TOOLS.md](project_management/00_tools/TOOLS.md) for complete documentation, advanced usage, and examples.

## AI Agent System

ProTemp ships with seven specialized GitHub Copilot agent personas defined in [.github/agents/](.github/agents/). Each agent has clearly defined responsibilities, expertise, inputs, outputs, and limitations.

An orchestration layer in [.github/copilot-instructions.md](.github/copilot-instructions.md) automatically routes tasks to the most appropriate agent, enabling autonomous execution of complex, multi-step workflows.

See [AGENTS.md](AGENTS.md) for the complete agent registry, including supporting standards ([communication_standards.md](project_management/01_guidelines/agent_behavior/communication_standards.md)) and workflow definitions.

| Agent | Responsibility |
|-------|---------------|
| **Architect** | Architecture vision maintenance & implementation compliance reviews |
| **Developer** | Backlog item selection, implementation, and work item close-out |
| **Tester** | Test planning, test creation, execution, and test reporting |
| **Requirements** | Requirements elicitation, derivation, and specification |
| **Security** | Security reviews, threat modeling, and security concept maintenance |
| **Documentation** | User guides, operations guides, and developer documentation |
| **License** | License compliance auditing and dependency attribution |

## License

This project is licensed under the [Creative Commons Attribution-ShareAlike 4.0 International (CC BY-SA 4.0)](https://creativecommons.org/licenses/by-sa/4.0/) license. See [LICENSE.md](LICENSE.md) for details.

## Credits

Architecture documentation structure based on the [arc42](https://arc42.org) template by Dr. Gernot Starke and Dr. Peter Hruschka. See [CREDITS.md](CREDITS.md).
