# VibeMatch presentation outline (5–7 minutes)

Target length: about 6 minutes. This outline is designed for a live walkthrough; the project does not depend on a video for evaluation.

## 0:00–0:45 — Problem and project context

- Introduce the base project: the Modules 1–3 Music Recommender Simulation.
- Explain the goal: turn a listener's preferences into a ranked list of tracks with understandable reasons.
- State the scope clearly: this is a deterministic content-based recommender, not a generative model.

## 0:45–1:30 — What changed

- Show the CLI options for genre, mood, energy, acoustic preference, and top result count.
- Explain the reliability extension: input guardrails and automated tests make expected behavior reproducible.
- Mention the bundled catalog keeps the demo offline and avoids API keys.

## 1:30–2:15 — Architecture

- Open `diagrams/architecture.mmd` or its rendered Mermaid view.
- Trace the flow: listener input and CSV catalog → loader/runner → scorer → ranking → recommendations with explanations.
- Point out that pytest checks both recommendation behavior and CLI guardrails.

## 2:15–4:15 — Live demo

Run these commands from the repository root:

```powershell
python -m src.main --genre pop --mood happy --energy 0.8 --top-k 3
python -m src.main --genre lofi --mood chill --energy 0.4 --top-k 2
python -m src.main --genre jazz --mood relaxed --energy 0.4 --top-k 2 --likes-acoustic
```

Call attention to how changing inputs changes the order and explanations. Then demonstrate a rejected input:

```powershell
python -m src.main --energy 1.5
```

The CLI exits with status `2` and explains that energy must be between `0.0` and `1.0`.

## 4:15–5:15 — Testing and lessons

- Run `python -m pytest -q`; the current suite has five passing tests.
- Explain that these tests establish software behavior, not human preference quality.
- Discuss the trade-off: a small transparent catalog is easy to inspect and reproduce, but cannot represent real-world taste or musical diversity.

## 5:15–6:00 — Responsible use and close

- Mention subjective genre/mood labels, possible filter bubbles, and the risk of treating a score as certainty.
- Explain that the model card records limitations, potential misuse, and human oversight.
- Close with the engineering takeaway: a useful AI system needs clear assumptions, guardrails, and reproducible tests—not only a compelling output.

## Demo checklist

- Start in the repository root with dependencies installed.
- Keep the README, architecture diagram, and model card available to show.
- The same command outputs and reliability evidence are also recorded in `evidence/reproducible_runs.md`.
