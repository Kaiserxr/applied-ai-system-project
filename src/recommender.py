import csv
from typing import Any, Dict, List, Tuple
from dataclasses import asdict, dataclass


@dataclass
class Song:
    """
    Represents a song and its attributes.
    Required by tests/test_recommender.py
    """
    id: int
    title: str
    artist: str
    genre: str
    mood: str
    energy: float
    tempo_bpm: float
    valence: float
    danceability: float
    acousticness: float


@dataclass
class UserProfile:
    """
    Represents a user's taste preferences.
    Required by tests/test_recommender.py
    """
    favorite_genre: str
    favorite_mood: str
    target_energy: float
    likes_acoustic: bool


def _as_float(value: Any, default: float = 0.0) -> float:
    try:
        return float(value)
    except (TypeError, ValueError):
        return default


def _normalize_song(song: Any) -> Dict[str, Any]:
    if isinstance(song, Song):
        song_dict = asdict(song)
    else:
        song_dict = dict(song)

    for numeric_key in ("energy", "tempo_bpm", "valence", "danceability", "acousticness"):
        if numeric_key in song_dict:
            song_dict[numeric_key] = _as_float(song_dict[numeric_key])
    return song_dict


def _normalize_user_prefs(user_prefs: Dict[str, Any]) -> Dict[str, Any]:
    if not isinstance(user_prefs, dict):
        raise TypeError("user_prefs must be a dictionary")

    return {
        "genre": str(user_prefs.get("genre", user_prefs.get("favorite_genre", ""))).strip(),
        "mood": str(user_prefs.get("mood", user_prefs.get("favorite_mood", ""))).strip(),
        "energy": _as_float(user_prefs.get("energy", user_prefs.get("target_energy", 0.0))),
        "likes_acoustic": bool(user_prefs.get("likes_acoustic", False)),
    }


class Recommender:
    """
    OOP implementation of the recommendation logic.
    Required by tests/test_recommender.py
    """

    def __init__(self, songs: List[Song]):
        self.songs = songs

    def recommend(self, user: UserProfile, k: int = 5) -> List[Song]:
        results = []
        user_prefs = {
            "genre": user.favorite_genre,
            "mood": user.favorite_mood,
            "energy": user.target_energy,
            "likes_acoustic": user.likes_acoustic,
        }

        for song in self.songs:
            score, _ = score_song(user_prefs, song)
            results.append((song, score))

        results.sort(key=lambda item: (-item[1], item[0].title))
        return [song for song, _ in results[:k]]

    def explain_recommendation(self, user: UserProfile, song: Song) -> str:
        user_prefs = {
            "genre": user.favorite_genre,
            "mood": user.favorite_mood,
            "energy": user.target_energy,
            "likes_acoustic": user.likes_acoustic,
        }
        _, reasons = score_song(user_prefs, song)
        explanation = "; ".join(reasons)
        return explanation if explanation else "This song is a reasonable match for the user's taste profile."


def load_songs(csv_path: str) -> List[Dict]:
    """
    Loads songs from a CSV file.
    Required by src/main.py
    """
    songs: List[Dict] = []
    with open(csv_path, "r", newline="", encoding="utf-8") as csv_file:
        reader = csv.DictReader(csv_file)
        for row in reader:
            if not row:
                continue
            song = {key: value for key, value in row.items()}
            if "id" in song:
                song["id"] = int(float(song["id"]))
            for numeric_key in ("energy", "tempo_bpm", "valence", "danceability", "acousticness"):
                if numeric_key in song:
                    song[numeric_key] = _as_float(song[numeric_key], 0.0)
            songs.append(song)
    return songs


def score_song(user_prefs: Dict, song: Dict) -> Tuple[float, List[str]]:
    """
    Scores a single song against user preferences.
    Required by recommend_songs() and src/main.py
    """
    prefs = _normalize_user_prefs(user_prefs)
    song_data = _normalize_song(song)

    score = 0.0
    reasons: List[str] = []

    user_genre = prefs["genre"].lower()
    song_genre = str(song_data.get("genre", "")).lower()
    if user_genre and song_genre == user_genre:
        score += 2.0
        reasons.append("Genre match")
    elif user_genre and (user_genre in song_genre or song_genre in user_genre):
        score += 1.0
        reasons.append("Related genre")

    user_mood = prefs["mood"].lower()
    song_mood = str(song_data.get("mood", "")).lower()
    if user_mood and song_mood == user_mood:
        score += 1.0
        reasons.append("Mood match")

    target_energy = prefs["energy"]
    track_energy = _as_float(song_data.get("energy", 0.0))
    energy_distance = abs(track_energy - target_energy)
    energy_similarity = max(0.0, 1.0 - energy_distance)
    score += energy_similarity * 2.5
    if energy_distance <= 0.15:
        reasons.append("Energy is close to your target")
    elif track_energy > target_energy:
        reasons.append("The track is slightly more energetic than your target")
    else:
        reasons.append("The track is slightly calmer than your target")

    likes_acoustic = prefs["likes_acoustic"]
    acousticness = _as_float(song_data.get("acousticness", 0.0))
    if likes_acoustic and acousticness >= 0.6:
        score += 0.5
        reasons.append("Acoustic sound matches your taste")
    elif not likes_acoustic and acousticness >= 0.75:
        score -= 0.5
        reasons.append("Acoustic-heavy sound is less aligned with your preference")

    return round(score, 2), reasons


def recommend_songs(user_prefs: Dict, songs: List[Dict], k: int = 5) -> List[Tuple[Dict, float, str]]:
    """
    Functional implementation of the recommendation logic.
    Required by src/main.py
    """
    ranked: List[Tuple[Dict, float, str]] = []
    for song in songs:
        score, reasons = score_song(user_prefs, song)
        explanation = "; ".join(reasons) if reasons else "No strong match"
        ranked.append((song, score, explanation))

    ranked.sort(key=lambda item: (-item[1], str(item[0].get("title", ""))))
    return ranked[:k]
