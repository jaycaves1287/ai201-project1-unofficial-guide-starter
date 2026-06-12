import argparse
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from unofficial_guide.embeddings import SentenceTransformerEmbedder
from unofficial_guide.vector_store import ChromaReviewStore, load_chunks_jsonl


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Embed review chunks and store them in ChromaDB."
    )
    parser.add_argument(
        "--chunks",
        type=Path,
        default=ROOT / "data" / "chunks" / "rmp_chunks.jsonl",
        help="JSONL chunks created by scripts/build_chunks.py.",
    )
    parser.add_argument(
        "--db-path",
        type=Path,
        default=ROOT / "chroma_db",
        help="Persistent ChromaDB directory.",
    )
    parser.add_argument(
        "--collection",
        default="ucsc_cse_reviews",
        help="ChromaDB collection name.",
    )
    args = parser.parse_args()

    chunks = load_chunks_jsonl(args.chunks)
    embedder = SentenceTransformerEmbedder()
    store = ChromaReviewStore.persistent(args.db_path, args.collection, embedder)
    store.rebuild(chunks)
    print(f"Loaded chunks: {len(chunks)}")
    print(f"Stored records: {store.count()}")
    print(f"Collection: {args.collection}")
    print(f"DB path: {args.db_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
