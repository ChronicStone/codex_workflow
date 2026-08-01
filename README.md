<h3 align="center"><big><big><strong>SIMPLE&emsp;&emsp;───&emsp;&emsp;EASY&emsp;&emsp;───&emsp;&emsp;EFFICIENT</strong></big></big></h3>
<p align="center"><small>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;(to use)&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;(to install)&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;(token consumption)</small></p>
<hr>

A project-scoped Codex workflow that configures **GPT-5.6 Sol as the main orchestrator** and **GPT-5.6 Luna as the default subagent** on heavy tasks.

The workflow is designed to optimize token usage and manage long-running implementation plans across multiple Codex sessions. It includes bounded subagent context, executor–tester repair loops, worker lifecycle management, project-state tracking, protected documentation, and an End-of-Session handoff.

> **Note:** The workflow is installed per project. Install it again when starting a new project.


## Installation

### 1. Download the repository

Use either of these methods:

* Select **Code → Download ZIP** on GitHub and extract it.
* Clone the repository with Git.

Place or rename the downloaded repository folder as `codex_workflows` inside your project directory:

```text
my-project/
├── codex_workflows/
│   ├── workflows_setup_guide.md
│   ├── AGENTS.md
│   ├── heavy_route.md
│   ├── medium_route.md
│   ├── executor_luna.toml
│   ├── executor_sol.toml
│   ├── tester.toml
│   └── doc-writer.toml
└── ...
```

### 2. Ask Codex to install the workflow

Launch Codex CLI or the Codex app from your project directory and send:

```text
Read `codex_workflows/workflows_setup_guide.md` and perform the complete installation process described in it.
```

Done! At this point, the basic installation process is complete. Codex will ask some additional optional advanced questions below to further optimize the current project.

## Configuration Questions

After basic installation, Codex will ask the following advanced configuration questions. You can answer them or skip them. If you skip, the default settings will be used.

### 1. Workflow Style and Design Principles (optinal)

Codex will ask about the project's workflow style and core design principles.
You can describe requirements such as:

- Prioritize modular design;
- Keep dependencies low;
- Do not change public APIs without prior approval;
- Prioritize C/C++ and limit dynamic allocation;
- Always run relevant tests after modifications.

### 2. Frontend Project Profile (optional)

The default workflow is designed primarily for backend work (Very heavily focused on testing). If the current project is a frontend project, Codex will ask whether you want to minimize testing, modularization, or similar requirements for the project. 

### 3. Power Configuration

The default workflow is designed to save tokens for the ChatGPT Plus plan. Codex will ask if you want to enable each advanced option individually.

- Allow more subagents (currently a maximum of 3) and allow more than one `executor_sol` call.
- Set `executor_luna` and `tester` to the `max` model_reasoning_effort. Currently `xhigh`. 
- Allow subagents to send more detailed report packets to the main agent (event and final report are currently limited to 150 & 250 words).
- Allow subagents to retry more times when stuck/blocked before replacing them (currently 2). The new subagent will have to reload the context packet, but this will reduce the risk of getting stuck; consider this.

### Restart codex after installation

### What is a workflow route?

There are 3 work routes:
- Light route: Default, for light and medium tasks. Original Codex, minimal context, no need for further explanation.
- Heavy route: For the deployment of heavy plans and tasks. The main agent will coordinate the workers. Sol medium -> Sol xhigh is recommended. 
- Medium route: Coordinating multiple sub-agents for a medium-sized task can sometimes cost more tokens and be slower than letting the main agent perform the work independently. Sol medium is recommended.

## HOW TO USE

- Normally, for simple work or general Q&A, you don't need to do anything.
- When starting or continuing a plan in progress, just tell Codex in the prompt: "

```text
use medium route / use heavy route. [your task description]".
```
Codex will switch to a full workflow with a medium/heavy route.  Codex will not automatically switch to other routes and will be maintained throughout the work session unless you actively change the route, so u dont need to repeat the route selection in every prompt.

- When you want to end current session, clean up and update documents, commit, etc., tell Codex: 

```text
end this session. [tell Codex more details if necessary]".
```
`End-of-Session` handoff will be performed (see `heavy_rote.md`/ `medium_route.md` for details about the handoff). This process updates the main document framework so that subsequent sessions can seamlessly continue the ongoing work.

You can still continue the session after that message if needed. 

### Customize the workflow

- Customize the End-of-Session handoff to suit your needs in `agent_docs/workflows/heavy_route.md` and `agent_docs/workflows/medium_route.md`.
- Add the custom subagents you want in `~/.codex/agents`

.... 
