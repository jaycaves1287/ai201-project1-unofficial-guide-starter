import argparse
import re
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from unofficial_guide.ingest import fetch_html
from unofficial_guide.models import ProfessorSource, ReviewChunk
from unofficial_guide.pipeline import build_chunks_from_html, write_chunks_jsonl


RMP_SOURCES = [
    ProfessorSource(
        "Alexander Rudnick",
        "https://www.ratemyprofessors.com/professor/2762323",
    ),
    ProfessorSource(
        "Cormac Flanagan",
        "https://www.ratemyprofessors.com/professor/454089",
    ),
    ProfessorSource(
        "Owen Arden",
        "https://www.ratemyprofessors.com/professor/2473496",
    ),
    ProfessorSource(
        "Lindsey Kuper",
        "https://www.ratemyprofessors.com/professor/2493257",
    ),
    ProfessorSource(
        "David Harrison",
        "https://www.ratemyprofessors.com/professor/2328264",
    ),
    ProfessorSource(
        "Liting Hu",
        "https://www.ratemyprofessors.com/professor/2915058",
    ),
    ProfessorSource(
        "Kerry Veenstra",
        "https://www.ratemyprofessors.com/professor/1883634",
    ),
    ProfessorSource(
        "Scott Brandt",
        "https://www.ratemyprofessors.com/professor/629552",
    ),
    ProfessorSource(
        "Christina Parsa",
        "https://www.ratemyprofessors.com/professor/2351640",
    ),
    ProfessorSource(
        "Chen Qian",
        "https://www.ratemyprofessors.com/professor/2345038",
    ),
    ProfessorSource(
        "Nikos Tziavelis",
        "https://www.ratemyprofessors.com/professor/3086025",
    ),
    ProfessorSource(
        "Matthew Guthaus",
        "https://www.ratemyprofessors.com/professor/1073316",
    ),
]


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Build review-level chunks from live Rate My Professors pages."
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=ROOT / "data" / "chunks" / "rmp_chunks.jsonl",
        help="JSONL file to write chunks into.",
    )
    parser.add_argument(
        "--cache-dir",
        type=Path,
        default=ROOT / "data" / "raw" / "rmp_html",
        help="Directory for raw fetched RMP HTML. Use --no-cache to skip.",
    )
    parser.add_argument(
        "--no-cache",
        action="store_true",
        help="Do not save fetched HTML pages.",
    )
    parser.add_argument(
        "--limit",
        type=int,
        default=len(RMP_SOURCES),
        help="Number of RMP sources to fetch from the first-pass source list.",
    )
    parser.add_argument(
        "--sample-size",
        type=int,
        default=5,
        help="Number of sample chunks to print after writing JSONL.",
    )
    args = parser.parse_args()

    sources = RMP_SOURCES[: args.limit]
    cache_dir = None if args.no_cache else args.cache_dir
    chunks = _build_chunks(sources, cache_dir)
    write_chunks_jsonl(chunks, args.output)
    _print_summary(sources, chunks, args.output, args.sample_size)
    return 0


def _build_chunks(
    sources: list[ProfessorSource],
    cache_dir: Path | None,
) -> list[ReviewChunk]:
    all_chunks: list[ReviewChunk] = []
    for source in sources:
        print(f"Fetching {source.professor}...")
        html = fetch_html(source)
        if cache_dir is not None:
            _write_raw_html(cache_dir, source, html)
        chunks = build_chunks_from_html(source, html)
        print(f"  extracted {len(chunks)} chunks")
        all_chunks.extend(chunks)
    return all_chunks


def _write_raw_html(cache_dir: Path, source: ProfessorSource, html: str) -> None:
    cache_dir.mkdir(parents=True, exist_ok=True)
    filename = _safe_filename(source.professor) + ".html"
    (cache_dir / filename).write_text(html, encoding="utf-8", newline="\n")


def _safe_filename(value: str) -> str:
    return re.sub(r"[^a-z0-9]+", "_", value.lower()).strip("_")


def _print_summary(
    sources: list[ProfessorSource],
    chunks: list[ReviewChunk],
    output_path: Path,
    sample_size: int,
) -> None:
    print()
    print(f"Fetched pages: {len(sources)}")
    print(f"Total chunks: {len(chunks)}")
    print(f"Wrote: {output_path}")
    print()
    print("Sample chunks")
    print("-------------")
    for index, chunk in enumerate(chunks[:sample_size], start=1):
        print(f"\n[{index}] {chunk.metadata['professor']} / {chunk.metadata['course']}")
        print(chunk.text)


if __name__ == "__main__":
    raise SystemExit(main())
