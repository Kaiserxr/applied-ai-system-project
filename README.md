# VibeMatch: Transparent Music Recommender

VibeMatch is a small, runnable content-based recommender. It ranks songs from a bundled catalog according to a listener's preferred genre, mood, energy, and acoustic preference, and explains each result using the matching features.

This project uses deterministic scoring rules, not a generative AI model or an external API. Its applied-AI extension is a reliability/testing system: the ranking logic is explainable and covered by automated tests, and invalid CLI values are rejected before recommendations are produced.

## Base project

This project extends the **Music Recommender Simulation** starter project from Modules 1–3. The base project's goal was to represent tracks and listener preferences as structured data, score songs based on genre, mood, energy, and acousticness, and return explainable ranked recommendations. This version preserves that scoring approach while making the command-line application configurable, adding input guardrails, and documenting reproducible evaluation evidence.

## Architecture

The application reads the curated song catalog from `data/songs.csv`, accepts preferences through the CLI, scores and ranks each track, and prints a short explanation for each recommendation. Automated tests exercise ranking, CLI behavior, and invalid-input handling. The human reviewer can inspect the rules and catalog directly; no model endpoint or hidden data source is involved.

See the Mermaid source at [`diagrams/architecture.mmd`](diagrams/architecture.mmd).

## Setup and usage

Requirements: Python 3.8 or newer. The runtime application uses only the Python standard library. `pytest` is required to run the test suite.

From the repository root:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
```

Run with the defaults (pop, happy, energy 0.8, top five):

```powershell
python -m src.main
```

Set a profile and result count:

```powershell
python -m src.main --genre lofi --mood chill --energy 0.4 --top-k 3 --likes-acoustic
```

`--energy` must be between `0.0` and `1.0`; `--top-k` must be at least `1`. Run the module command from the repository root so Python can resolve the `src` package. The catalog path itself is resolved relative to the application file.

Run the automated checks:

```powershell
python -m pytest -q
```

## Sample interactions

These are command outputs from the bundled catalog and the commands above. More complete reproducible transcripts and the test summary are in [`evidence/reproducible_runs.md`](evidence/reproducible_runs.md).

**1. Happy, energetic pop**

```text
> python -m src.main --genre pop --mood happy --energy 0.8 --top-k 3
User profile: genre=pop, mood=happy, energy=0.80, likes_acoustic=False

Top recommendations:

Sunrise City - Score: 5.45
Because: Genre match; Mood match; Energy is close to your target

Rooftop Lights - Score: 4.40
Because: Related genre; Mood match; Energy is close to your target

Gym Hero - Score: 4.17
Because: Genre match; Energy is close to your target
```

**2. Chill lofi**

```text
> python -m src.main --genre lofi --mood chill --energy 0.4 --top-k 2
User profile: genre=lofi, mood=chill, energy=0.40, likes_acoustic=False

Top recommendations:

Midnight Coding - Score: 5.45
Because: Genre match; Mood match; Energy is close to your target

Library Rain - Score: 4.88
Because: Genre match; Mood match; Energy is close to your target; Acoustic-heavy sound is less aligned with your preference
```

**3. Acoustic jazz**

```text
> python -m src.main --genre jazz --mood relaxed --energy 0.4 --top-k 2 --likes-acoustic
User profile: genre=jazz, mood=relaxed, energy=0.40, likes_acoustic=True

Top recommendations:

Coffee Shop Stories - Score: 5.92
Because: Genre match; Mood match; Energy is close to your target; Acoustic sound matches your taste

Focus Flow - Score: 3.00
Because: Energy is close to your target; Acoustic sound matches your taste
```

## Design decisions and trade-offs

- **Content-based scoring:** genre and mood matches contribute fixed points; energy similarity contributes a continuous score; acousticness can add or subtract a small amount. This is easy to inspect and explain, but the weights are hand-chosen rather than learned from listener feedback.
- **Local CSV catalog:** keeps setup and evaluation reproducible without credentials or network access. The ten-track sample is not representative of a real music library.
- **CLI input guardrails:** reject energy values outside the supported normalized range and non-positive result counts. Other preferences are free text, so misspellings can yield few exact matches.
- **No hosted model:** a generative model would add complexity and make outputs less deterministic without improving this feature-scoring task.

## Testing summary

The test suite checks object-based ranking and explanations, CLI profile application and result limits, and rejection of invalid energy and result-count values. Run `python -m pytest -q` to reproduce the current result. The transcript file records the exact output from the runnable examples and test run; these checks establish implementation behavior, not real-world recommendation quality.

Reproducible reliability and guardrail check:

```text
> python -m pytest -q
.....                                                                    [100%]
5 passed in 0.02s

> python -m src.main --energy 1.5
error: --energy must be between 0.0 and 1.0

> python -m src.main --top-k 0
error: --top-k must be at least 1
```

The test duration and argparse usage header can vary by local environment. The two invalid-input commands exit with status `2`.

## Reflection

Building this system reinforced that AI-like behavior can come from transparent ranking rules as well as a large language model. Defining the input ranges, explaining each recommendation, and testing edge cases made the result easier to reason about. The model card contains the responsible-AI reflection, including collaboration choices, limitations, and potential misuse.

## Portfolio artifact

**Code:** [Kaiserxr/applied-ai-system-project](https://github.com/Kaiserxr/applied-ai-system-project)

**What this project says about me as an AI engineer:** I value building AI systems that are understandable and reproducible, not just impressive in a demo. This project shows that I can turn a starter recommender into a usable tool, make its assumptions visible, test expected and invalid inputs, and be clear about the limits of what its results mean.

**Presentation:** Use [`presentation.md`](presentation.md) for a timed 5–7 minute walkthrough outline and demo commands.

## Repository contents

- `src/`: application and recommendation logic
- `data/songs.csv`: bundled song catalog
- `tests/`: automated tests
- `diagrams/`: Mermaid system architecture source
- `evidence/`: reproducible command transcripts
- [`presentation.md`](presentation.md): timed presentation outline
- [`model_card.md`](model_card.md): intended use, evaluation, limitations, and reflection
