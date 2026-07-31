# Codex Project Workflow

Codex workflow - Automatically set up and configure Luna subagent + main agent as Orchestrator for optimize token usage and managing long-running implementation plans across multiple sessions

> Note: This workflow has scope only within the current project. When you start a new project, you will need to install the workflow again. 

Zip file contains the following files:
- `workflows_setup_guide.md` - The installation guide for the workflow for Codex setup agent.
- `AGENTS.md` - The main agent file.
- `tester.toml` - The tester subagent configuration file.
- `doc-writer.toml` - The doc-writer subagent configuration file.
- `executor_luna.toml` - The executor_luna subagent configuration file.
- `executor_sol.toml` - The executor_sol subagent configuration file.
- `heavy_route.md` - The heavy route workflow files.
- `medium_route.md` - The medium route workflow file.

## Installation

### 1. Move the ZIP file to the project

Download the ZIP file and move it to the root directory of the project where you want to use the workflow.

```text
my-project/
├── codex_workflows.zip
└── ...
```

### 2. launch Codex app or Codex cli in the project directory, tell it to install the default workflow

Send the following request to Codex:
> Please extract `codex_workflows.zip`, read the extracted `workflows_setup_guide.md` file, and perform the entire installation process within it.

Codex will create two workflow files, main documentation framework in agent_docs/ and agent file `AGENTS.md` in your workspace, along with initializing the subagent set including `tester`, `doc-writer`, `executor_luna`, `executor_sol` inside ~/.codex/agents/

Done! At this point, the basic installation process is complete. Codex will ask some additional optional advanced questions below to further optimize the current project.

## Configuration Questions

After installation, Codex will ask the following questions in sequence.

### 1. Workflow Style and Design Principles (optinal)

Codex will ask about the project's workflow style and core design principles.
You can describe requirements such as:

- Prioritize modular design;
- Keep dependencies low;
- Do not change public APIs without prior approval;
- Prioritize C/C++ and limit dynamic allocation;
- Always run relevant tests after modifications.

### 2. Power Configuration

The default workflow is designed to save tokens for the ChatGPT Plus plan. Codex will ask if you want to enable each advanced option individually.

- Allow more subagents (currently a maximum of 3) and allow more than one `executor_sol` call.
- Set `executor_luna` and `tester` to the `max` model_reasoning_effort. Currently `xhigh`. 
- Allow subagents to send more detailed report packets to the main agent (event and final report are currently limited to 150 & 250 words).
- Allow subagents to retry more times when stuck/blocked before replacing them (currently 2). The new subagent will have to reload the context packet, but this will reduce the risk of getting stuck; consider this.

### Restart codex after installation

## What is a workflow route?

There are 3 work routes:
- Light route: Default, for light and medium tasks. Original Codex, minimal context, no need for further explanation.
- Heavy route: For the deployment of heavy plans and tasks. The main agent will coordinate the workers. Sol medium -> Sol xhigh is recommended. 
- Medium route: Coordinating multiple sub-agents for a medium-sized task can sometimes cost more tokens and be slower than letting the main agent perform the work independently. Sol medium is recommended.

### How to use 
- Normally, for simple work or general Q&A, you don't need to do anything.
- When starting or continuing a plan in progress, just tell Codex in the prompt: "use medium route / use heavy route. [your task description]".

(Codex will not automatically activate the medium/heavy route. The selected route will be maintained throughout the work session unless you actively change the route.)

- When you want to end a session, clean up and update documents, commit, etc., tell Codex: "end this session. [tell Codex more details if need]". End-of-Session handoff will be performed (see AGENTS.md for details about the handoff). This process updates the main document framework so that subsequent sessions can seamlessly continue the ongoing work.

You can still continue the session after that message if needed. 

### Customize the workflow

- Customize the End-of-Session handoff to suit your needs in AGENTS.md
- Add the custom subagents you want in ~/.codex/agents

.... 