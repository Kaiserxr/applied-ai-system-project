# 🎵 Music Recommender Simulation

## Project Summary

This project builds a lightweight content-based music recommender that uses a user's preferred genre, mood, and target energy level to rank songs in a small catalog. The system models each track as structured data and scores every song against the user's taste profile, then returns the strongest matches in order.

The goal is to make the recommendation logic transparent: rather than a mysterious black-box model, this version shows exactly how features like genre, mood, and energy are combined into a numeric score. That makes it easier to explain how real recommendation platforms turn listening habits into predictions.

---

## How The System Works

My design uses a simple content-based recommender. Each `Song` stores attributes such as genre, mood, energy, tempo, valence, danceability, and acousticness. The `UserProfile` stores a favorite genre, favorite mood, a target energy level, and whether the user prefers more acoustic or more energetic tracks.

The recommendation process works in three steps:

1. Input: user preferences are compared against each song in the dataset.
2. Process: the system gives points for matching genre, mood, and close energy values. It also applies a small acousticness bonus or penalty depending on the user's taste.
3. Output: all songs are ranked by score, and the top `k` are returned as recommendations.

A simple data-flow view is:

`User preferences -> Score each song -> Rank songs -> Recommend top K`

This approach is intentionally simple, but it mirrors how real platforms translate user signals into a ranked list of plausible next listens.

---

## Getting Started

### Setup

1. Create a virtual environment (optional but recommended):

   ```bash
   python -m venv .venv
   source .venv/bin/activate      # Mac or Linux
   .venv\Scripts\activate         # Windows

2. Install dependencies

```bash
pip install -r requirements.txt
```

3. Run the app:

```bash
python -m src.main
```

### Running Tests

Run the starter tests with:

```bash
pytest
```

You can add more tests in `tests/test_recommender.py`.

---

## Sample Recommendation Output

Example output for a user who likes pop, happy tracks with moderate-to-high energy:

```
User profile: genre=pop, mood=happy, energy=0.8

Top recommendations:

Sunrise City - Score: 5.45
Because: Genre match; Mood match; Energy is close to your target

Rooftop Lights - Score: 4.40
Because: Related genre; Mood match; Energy is close to your target

Gym Hero - Score: 4.17
Because: Genre match; Energy is close to your target
```

**Screenshot or video** *(optional)*: <!-- Insert a screenshot or demo video link here -->

---

## Experiments You Tried

I tested a few profile types to see how the ranking changed:

- Pop + happy + high energy profile preferred tracks like "Sunrise City" and "Rooftop Lights" because they matched both the requested genre and mood.
- A chill/low-energy profile would rank lofi and ambient songs higher because the energy similarity term rewards closeness to the target value.
- When I increased the acousticness penalty for users who do not like acoustic tracks, songs with very warm, mellow timbres were pushed lower in the ranking.

This showed that genre and mood dominate the score, while energy and acousticness act as tie-breakers and fine-tuning factors.

---

## Limitations and Risks

This recommender works on a small catalog and does not understand lyrics, artist identity, or listening history. It can also over-favor a single genre if a user’s profile is too narrow, which creates a filter-bubble effect. Because the system relies on manually chosen features, it may miss songs that are emotionally or culturally meaningful but do not match the numerical profile closely.

You will go deeper on this in your model card.

---

## Reflection

Read and complete `model_card.md`:

[**Model Card**](model_card.md)

This project taught me that recommendation systems are really just structured ways of turning data into a ranking. Even a small system can appear smart when it combines a few well-chosen features like genre, mood, and energy into a clear scoring rule.

I also saw how bias can creep in: if the model overweights genre or treats a narrow preference as universal, it can hide great content outside the user’s current taste cluster. That is one reason real recommendation systems add user history, diversity rules, and human oversight to avoid reinforcing narrow patterns.



