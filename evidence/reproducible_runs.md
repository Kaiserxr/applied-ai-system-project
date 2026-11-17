# Reproducible execution evidence

Run these commands from the repository root with Python 3.8+ and `pytest` installed. The CLI uses the bundled `data/songs.csv`; the runtime itself has no third-party dependencies.

## Pop / happy / energetic

Command:

```powershell
python -m src.main --genre pop --mood happy --energy 0.8 --top-k 3
```

Output:

```text
User profile: genre=pop, mood=happy, energy=0.80, likes_acoustic=False

Top recommendations:

Sunrise City - Score: 5.45
Because: Genre match; Mood match; Energy is close to your target

Rooftop Lights - Score: 4.40
Because: Related genre; Mood match; Energy is close to your target

Gym Hero - Score: 4.17
Because: Genre match; Energy is close to your target
```

## Lofi / chill

Command:

```powershell
python -m src.main --genre lofi --mood chill --energy 0.4 --top-k 2
```

Output:

```text
User profile: genre=lofi, mood=chill, energy=0.40, likes_acoustic=False

Top recommendations:

Midnight Coding - Score: 5.45
Because: Genre match; Mood match; Energy is close to your target

Library Rain - Score: 4.88
Because: Genre match; Mood match; Energy is close to your target; Acoustic-heavy sound is less aligned with your preference
```

## Jazz / relaxed / acoustic

Command:

```powershell
python -m src.main --genre jazz --mood relaxed --energy 0.4 --top-k 2 --likes-acoustic
```

Output:

```text
User profile: genre=jazz, mood=relaxed, energy=0.40, likes_acoustic=True

Top recommendations:

Coffee Shop Stories - Score: 5.92
Because: Genre match; Mood match; Energy is close to your target; Acoustic sound matches your taste

Focus Flow - Score: 3.00
Because: Energy is close to your target; Acoustic sound matches your taste
```

## Automated tests

Command:

```powershell
python -m pytest -q
```

Output:

```text
.....                                                                    [100%]
5 passed in 0.02s
```

The tests cover score ordering and explanations, profile-driven CLI output, result limits, and invalid energy/result-count inputs. Test duration varies by environment.

## Input guardrails

Commands:

```powershell
python -m src.main --energy 1.5
python -m src.main --top-k 0
```

Each command prints an argparse usage header followed by its respective error:

```text
error: --energy must be between 0.0 and 1.0
error: --top-k must be at least 1
```

Both commands exit with status `2`.
