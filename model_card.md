# 🎧 Model Card: Music Recommender Simulation

## 1. Model Name

**VibeMatch 1.0**

---

## 2. Intended Use

This recommender is designed for classroom exploration and small-scale simulation. It generates a list of songs that best fit a user's preferred genre, mood, and activity energy level. The model assumes the user has a few clear preferences, such as wanting pop music, a happy mood, and songs that are energetic but not overwhelming.

It is not intended to be a production-grade recommendation engine for real listeners. Instead, it is a transparent example of how a simple content-based recommender can convert song features into ranked suggestions.

---

## 3. How the Model Works

The model uses a small set of song attributes: genre, mood, energy, and acousticness. It compares those features against a user profile with a favorite genre, preferred mood, and target energy value. Each song earns points when it matches the user's genre and mood, and it also gets a score based on how similar the song's energy is to the target energy.

For example, a pop song with a happy mood and an energy value close to 0.8 will score higher than a lofi track with a calm mood and a lower energy level. The system also slightly rewards or penalizes acousticness depending on whether the user likes acoustic songs.

This is a simple content-based recommender, which means it relies on the features of the music itself rather than the behaviors of other listeners.

---

## 4. Data

The dataset contains a small catalog of songs with fields such as title, artist, genre, mood, energy, tempo, valence, danceability, and acousticness. The catalog includes a range of genres and moods, including pop, lofi, rock, ambient, jazz, synthwave, and indie pop.

The dataset is intentionally small and highly curated, which makes it easier to understand the logic but means it does not reflect the full richness of real music listening. It also leaves out large parts of musical taste, such as cultural context, lyrics, social trends, and user listening history.

---

## 5. Strengths

This model is strong at transparent, explainable ranking. If a user says they want happy, moderately energetic pop songs, the system can clearly explain why it chose a specific track. It also works well in a demo setting because the logic is simple enough to debug and inspect.

It tends to do a good job when a user has a few consistent preferences and the catalog is relatively small. In those cases, the ranking matches the intuition that songs that align with genre, mood, and energy should be prioritized.

---

## 6. Limitations and Bias

The system has several limitations. It does not look at lyrics, artist popularity, tempo patterns beyond the listed values, or the actual behavior of the user over time. That means it can miss songs that would be a good fit for reasons beyond the numeric features.

Bias is also possible. Because the system strongly values genre and mood, it may over-favor a narrow musical lane and reduce diversity in the recommendations. A user who likes pop may never see excellent experimental or niche songs that do not match the selected profile as closely. This creates the same kind of filter-bubble behavior seen in more advanced recommendation systems.

---

## 7. Evaluation

I checked the recommender by testing a few example user profiles. For a pop, happy, high-energy profile, the top songs were the ones that matched genre and mood while staying close to the energy target. For calmer profiles, lofi or ambient songs moved upward because their energy values aligned with the user’s target.

The main thing I looked for was whether the ranking was explainable and intuitive. The system passed that test: the output was easy to understand, and the top-ranked songs made sense for the profile.

---

## 8. Future Work

Future improvements could include more features such as tempo preference, danceability target, or user listening history. The model could also add diversity controls so the top recommendations do not all come from one genre or mood. A better next step would be to explain each recommendation in plain language and allow users to tune weights interactively.

---

## 9. Personal Reflection

This project helped me see that recommender systems are not magic; they are structured scoring systems that turn features into predictions. Even a simple model can feel surprisingly effective when the features are meaningful and the ranking logic is transparent.

It also made me think about bias. A system that is too rigid about genre or mood may keep people stuck in a narrow comfort zone, even when a broader range of music could be enjoyable. That lesson matters for all recommendation systems, from streaming platforms to search and shopping tools.

