<h3 align="center"><big><big><strong>SIMPLE&emsp;&emsp;───&emsp;&emsp;EASY&emsp;&emsp;───&emsp;&emsp;EFFICIENT</strong></big></big></h3>
<p align="center"><small>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;(to use)&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;(to install)&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;(token consumption)</small></p>
<hr>

![Workflow illustration](illustration.png)

A workflow designed to drastically reduce overall token usage, support seamless deployment across multiple sessions, and remain extremely simple to use.

Beneath the simplicity is a tightly engineered agent orchestration system: a purpose-built documentation framework, strict responsibility boundaries, main agent's second brain, compact work-package communication, anti-stall and worker-replacement mechanisms, executor–tester repair loops, worker lifecycle management, persistent project-state tracking. Everything is optimized to keep each agent focused on exactly what it needs. 

> 💡 For lightweight tasks, it won’t overdo things. Light route is default.

## 1. Quick installation ⚙️

### Open Codex CLI / Codex app from your project directory 

▶️ Send:

```text
Download the prerelease GitHub Release tagged `v1.1.0` from https://github.com/viettran-edgeAI/codex_workflow/releases. Download the universal asset `codex_workflow-1.1.0.zip` and `SHA256SUMS`, verify the ZIP checksum, and extract the ZIP to a temporary directory. Do not clone the repository, download a source-code archive, or use `README.md` as an installation source. Then read the extracted `codex_workflow/install.md` and follow it exactly to complete the first installation for this project.
```

🔄 Restart Codex after installation

## 2. Workflow usage 

### This workflow has 3 routes:
- Light route : No subagents, no workflow, minimal context.
- Heavy route : Deploy subagents, full workflow.
- Medium route: No subagents, full workflow.  

### How to use
- Normally, for simple work, general Q&A, you don't need to do anything. `light route` is the default route.

--------------------------------
- When starting or continuing a plan in progress, just tell Codex in the prompt: "

```text
use medium route / use heavy route. [your task description]".
```
> Codex stays on the selected route until you change it, so you don’t need to repeat it in every prompt.

--------------------------------
If the implementation plan is not yet complete, but the context window is nearly full, the conversation has already been compacted too many times, or you simply want to pause the work, trigger the **End-of-Session** procedure by sending:

```text
end this session. [more details if needed].
```
> You can still continue the session after that message if needed. 

To resume the unfinished work in a new session, send:

```text
use heavy route. continue the unfinished work.
```
---------------
> **⭐ Recommendation:** Assign very large and complex tasks to the `heavy route` to make the most of its capabilities and maximize token usage savings.

## 3. More details 🧭 
For the complete command reference, installed-file map, manual customization
guide, and Heavy-route design, see [workflow_usage.md](workflow_usage.md).
