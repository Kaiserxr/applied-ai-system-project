# Model Card: VibeMatch Music Recommender

## Model overview

**Name:** VibeMatch (rule-based content recommender)
**Version:** 1.1
**Task:** Rank a small catalog of songs for a user-supplied preference profile.

VibeMatch is a deterministic scoring program, not a trained statistical model or generative AI. It compares catalog metadata with a listener's preferred genre, mood, target energy, and acoustic preference, then sorts tracks by score and provides feature-based explanations.

## Intended use and out-of-scope use

The system is intended for educational demonstrations of recommendation, explainability, and software testing on a small curated catalog. It is not intended to infer sensitive traits, make high-stakes decisions, or represent the full range of music or listeners.

## Inputs, data, and outputs

Inputs are a free-text genre, free-text mood, normalized target energy from `0.0` to `1.0`, an acoustic preference toggle, and a requested number of results. The bundled CSV has ten fictional tracks with manually supplied genre, mood, energy, tempo, valence, danceability, and acousticness values.

The output is an ordered list of track metadata, numeric scores, and explanations based on the scoring rules. Scores are relative to the current catalog and should not be read as probabilities or confidence estimates.

## Method and design choices

Exact genre matches add 2 points, related genre names add 1, exact mood matches add 1, and energy similarity contributes up to 2.5 points. Acousticness can add or subtract 0.5 points based on the profile. Ties are resolved by title. The rules are intentionally small and visible so users can inspect how a result was produced.

## Testing and evaluation results

The automated tests cover object-based recommendation ordering, non-empty explanations, CLI profile application and result limits, and validation of energy and result count. Run:

```text
python -m pytest -q
```

The committed reproducible run record contains the exact test output and example CLI transcripts. These tests verify the implementation and guardrails; they do not establish that the recommendations match human taste. No formal human-subject evaluation or accuracy benchmark has been performed. A surprising behavior during testing was that the acoustic penalty can appear in the explanation even when a track still ranks highly; the reason describes one factor, not the entire ranking.

## Limitations and biases

- The catalog is tiny, curated, fictional, and not representative of different cultures, regions, eras, or musical communities.
- Genre and mood labels are subjective. Hand-labeled categories and fixed weights can encode the labeler's assumptions.
- Fixed rules can reinforce a narrow profile and repeatedly favor familiar genres, creating a filter-bubble effect. There is no diversity or novelty constraint.
- The system does not use lyrics, artist identity, listening history, popularity, context, or feedback. Energy and acousticness alone cannot capture musical fit.
- The recommendation explanations list scoring factors, but do not claim that a person will enjoy the track.
- Free-text preferences have no synonym or spelling normalization, and the scores are not calibrated confidence values.

## Risks and misuse prevention

The principal risks are presenting a toy catalog as representative, treating its scores as objective judgments, or using the preference interface to infer personal characteristics. The program does not collect user accounts, persist listener preferences, or connect to a network service. Keep it limited to its educational purpose; do not use its rankings for consequential decisions or claim that they reflect real-world popularity or audience preference. Broader deployments would need representative data, privacy review, diversity evaluation, and ongoing human oversight.

## Human oversight

Users can inspect the scoring implementation, data, and per-track reasons. A human should review recommendations and the catalog labels rather than treating the numeric order as authoritative. The current test suite checks software behavior, not the cultural quality or fairness of recommendations.

## AI collaboration reflection

An AI coding assistant was used to help make the command-line runner accept profiles, add input guardrails, and prepare reproducible documentation and tests. One suggestion accepted was exposing genre, mood, energy, acoustic preference, and result count as command-line options: it makes the same recommender straightforward to exercise with different inputs. One suggestion not adopted was introducing a hosted generative model; this was deliberately kept out because the existing task is transparent feature ranking, and an external model would add credentials, network dependence, and less reproducible outputs without addressing an identified need.

AI-generated changes were checked against the existing scorer, exercised with the bundled data, and covered by automated tests. Human review remains necessary for whether the manually assigned metadata and recommendations are musically appropriate.

## Future work

Potential improvements include a larger, responsibly sourced catalog, diversity-aware ranking, preference normalization, explicit weight tuning, and a documented human evaluation protocol. Each would require evaluation beyond the current software correctness tests.
