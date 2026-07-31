# Codex Project Workflow

Codex workflow for optimize token usage and managing long-running implementation plans across multiple sessions

> Note: This workflow has scope only within the current project. When you start a new project, you will need to install the workflow again. 

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

Codex will create two workflow files and the main documentation framework in agent_docs/, agent file `AGENTS.md` in your workspace, along with initializing the subagent set including `tester`, `doc-writer`, `executor_luna`, `executor_sol` inside ~/.codex/agents/

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
- Normally, for simple or general Q&A, you don't need to do anything.
- When starting or continuing a plan in progress, just tell Codex in the prompt: "use medium route / use heavy route. ..."

(Codex will not automatically activate the medium/heavy route. The selected route will be maintained throughout the work session unless you actively change the route.)
- When you want to end a session, clean up and update documents, commit, etc., tell Codex: "end this session. ...". 

Follow this procedure so that ongoing projects can be smoothly resumed in a future session. You can still continue the session after that if needed. 

### Customize the workflow

- Customize the End-of-Session handoff to suit your needs in AGENTS.md
- Add the custom subagents you want in ~/.codex/agents

.... 