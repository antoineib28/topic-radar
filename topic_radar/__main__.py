import sys
import tomllib

from dotenv import load_dotenv

from .collect import collect
from .report import write_report


def main() -> None:
    load_dotenv()
    with open("config.toml", "rb") as f:
        cfg = tomllib.load(f)

    cmd = sys.argv[1] if len(sys.argv) > 1 else ""
    if cmd == "collect":
        print("Saved", collect(cfg))
    elif cmd == "report":
        print("Wrote", write_report(cfg))
    else:
        print("Usage: python -m topic_radar [collect|report]")
        sys.exit(1)


if __name__ == "__main__":
    main()
