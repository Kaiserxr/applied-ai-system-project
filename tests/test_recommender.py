from src.recommender import Song, UserProfile, Recommender
from src.main import main

def make_small_recommender() -> Recommender:
    songs = [
        Song(
            id=1,
            title="Test Pop Track",
            artist="Test Artist",
            genre="pop",
            mood="happy",
            energy=0.8,
            tempo_bpm=120,
            valence=0.9,
            danceability=0.8,
            acousticness=0.2,
        ),
        Song(
            id=2,
            title="Chill Lofi Loop",
            artist="Test Artist",
            genre="lofi",
            mood="chill",
            energy=0.4,
            tempo_bpm=80,
            valence=0.6,
            danceability=0.5,
            acousticness=0.9,
        ),
    ]
    return Recommender(songs)


def test_recommend_returns_songs_sorted_by_score():
    user = UserProfile(
        favorite_genre="pop",
        favorite_mood="happy",
        target_energy=0.8,
        likes_acoustic=False,
    )
    rec = make_small_recommender()
    results = rec.recommend(user, k=2)

    assert len(results) == 2
    # Starter expectation: the pop, happy, high energy song should score higher
    assert results[0].genre == "pop"
    assert results[0].mood == "happy"


def test_explain_recommendation_returns_non_empty_string():
    user = UserProfile(
        favorite_genre="pop",
        favorite_mood="happy",
        target_energy=0.8,
        likes_acoustic=False,
    )
    rec = make_small_recommender()
    song = rec.songs[0]

    explanation = rec.explain_recommendation(user, song)
    assert isinstance(explanation, str)
    assert explanation.strip() != ""


def test_cli_uses_requested_profile_and_limits_results(capsys):
    main(
        [
            "--genre",
            "lofi",
            "--mood",
            "chill",
            "--energy",
            "0.4",
            "--top-k",
            "2",
        ]
    )

    output = capsys.readouterr().out
    assert "genre=lofi, mood=chill, energy=0.40" in output
    assert "Midnight Coding" in output
    assert "Library Rain" in output
    assert "Sunrise City" not in output


def test_cli_rejects_out_of_range_energy(capsys):
    import pytest

    with pytest.raises(SystemExit) as exc_info:
        main(["--energy", "1.5"])

    assert exc_info.value.code == 2
    assert "--energy must be between 0.0 and 1.0" in capsys.readouterr().err


def test_cli_rejects_non_positive_result_count(capsys):
    import pytest

    with pytest.raises(SystemExit) as exc_info:
        main(["--top-k", "0"])

    assert exc_info.value.code == 2
    assert "--top-k must be at least 1" in capsys.readouterr().err
