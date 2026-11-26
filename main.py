"""Write the one-line roast entry for the Make.fun bounty.

Deterministic, stdlib only. Reads $MAKEFUN_OUTPUT_DIR, validates the
entry against the contest gate (1-160 chars, single line, non-empty)
and writes it as exact UTF-8 bytes with no trailing newline. After
writing, the file is re-read and verified byte-for-byte.
"""

import os

ENTRY = (
    "My smart fridge defrosts itself every night: the one appliance "
    "whose entire job is staying cold, and it still takes a warm break."
)

MAX_LENGTH = 160


class BlankError(ValueError):
    """Entry is empty or whitespace-only."""


class MultiLineError(ValueError):
    """Entry contains a newline or carriage return."""


class LengthError(ValueError):
    """Entry length is outside the 1-160 character gate."""


class VerificationError(RuntimeError):
    """Written file does not match the bytes we intended to write."""


def validate(text: str) -> None:
    """Check text against the contest gate, in order.

    Blank -> multi-line -> length, so a failing entry reports its
    first gate violation only.
    """
    if not text or not text.strip():
        raise BlankError("entry must not be empty or whitespace-only")
    if "\n" in text or "\r" in text:
        raise MultiLineError("entry must be a single line")
    if not 1 <= len(text) <= MAX_LENGTH:
        raise LengthError(
            f"entry must be 1-{MAX_LENGTH} characters, got {len(text)}"
        )


def verify_written(path: str, expected: bytes) -> None:
    """Re-read the file and confirm its bytes match what we wrote."""
    with open(path, "rb") as fh:
        actual = fh.read()
    if actual != expected:
        raise VerificationError(
            f"{path}: written bytes differ from expected "
            f"({len(actual)} bytes on disk vs {len(expected)} expected)"
        )


def main() -> None:
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR")
    if not out_dir:
        raise RuntimeError("MAKEFUN_OUTPUT_DIR is not set")

    validate(ENTRY)

    path = os.path.join(out_dir, "entry.txt")
    payload = ENTRY.encode("utf-8")
    with open(path, "wb") as fh:
        fh.write(payload)
    verify_written(path, payload)


if __name__ == "__main__":
    main()
