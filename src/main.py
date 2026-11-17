"""
Command line runner for the Music Recommender Simulation.
"""

import argparse
from pathlib import Path
from typing import List, Optional

try:
    from src.recommender import load_songs, recommend_songs
except ModuleNotFoundError:
    from recommender import load_songs, recommend_songs


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Recommend songs from the bundled catalog based on your preferences."
    )
    parser.add_argument("--genre", default="pop", help="Preferred genre (default: pop)")
    parser.add_argument("--mood", default="happy", help="Preferred mood (default: happy)")
    parser.add_argument(
        "--energy",
        type=float,
        default=0.8,
        help="Target energy from 0.0 to 1.0 (default: 0.8)",
    )
    parser.add_argument(
        "--likes-acoustic",
        action="store_true",
        help="Prefer acoustic tracks",
    )
    parser.add_argument(
        "--top-k",
        type=int,
        default=5,
        help="Number of recommendations to show (default: 5)",
    )
    return parser


def main(argv: Optional[List[str]] = None) -> None:
    parser = build_parser()
    args = parser.parse_args(argv)
    if not 0.0 <= args.energy <= 1.0:
        parser.error("--energy must be between 0.0 and 1.0")
    if args.top_k < 1:
        parser.error("--top-k must be at least 1")

    project_root = Path(__file__).resolve().parent.parent
    songs = load_songs(str(project_root / "data" / "songs.csv"))

    user_prefs = {
        "genre": args.genre,
        "mood": args.mood,
        "energy": args.energy,
        "likes_acoustic": args.likes_acoustic,
    }

    recommendations = recommend_songs(user_prefs, songs, k=args.top_k)

    print(
        "User profile: "
        f"genre={args.genre}, mood={args.mood}, energy={args.energy:.2f}, "
        f"likes_acoustic={args.likes_acoustic}"
    )
    print("\nTop recommendations:\n")
    for rec in recommendations:
        song, score, explanation = rec
        print(f"{song['title']} - Score: {score:.2f}")
        print(f"Because: {explanation}")
        print()


if __name__ == "__main__":
    main()
