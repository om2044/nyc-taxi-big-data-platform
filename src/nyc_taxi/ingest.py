
from pathlib import Path
from urllib.request import urlopen
from urllib.error import HTTPError, URLError
from datetime import datetime, timezone
import hashlib
import json


# ============================================================
# 1. CONFIGURATION
# ============================================================

YEAR = 2025
MONTH = 1

FILENAME = f"yellow_tripdata_{YEAR}-{MONTH:02d}.parquet"

SOURCE_URL = (
    "https://d37ci6vzurychx.cloudfront.net/"
    f"trip-data/{FILENAME}"
)

PROJECT_ROOT = Path(__file__).resolve().parents[2]

RAW_DIR = PROJECT_ROOT / "data" / "raw"

OUTPUT_PATH = RAW_DIR / FILENAME

MANIFEST_PATH = RAW_DIR / f"{FILENAME}.manifest.json"

CHUNK_SIZE = 1024 * 1024  # 1 MiB


# ============================================================
# 2. SHA-256 CHECKSUM
# ============================================================

def calculate_sha256(file_path: Path) -> str:
    """Calculate the SHA-256 checksum of a file."""

    sha256 = hashlib.sha256()

    with file_path.open("rb") as file:
        while True:
            chunk = file.read(CHUNK_SIZE)

            if not chunk:
                break

            sha256.update(chunk)

    return sha256.hexdigest()


# ============================================================
# 3. PARQUET FILE VALIDATION
# ============================================================

def validate_parquet_file(file_path: Path) -> None:
    """Perform basic Parquet file validation."""

    if not file_path.is_file():
        raise FileNotFoundError(f"File not found: {file_path}")

    if file_path.stat().st_size < 8:
        raise ValueError("File is empty or too small.")

    with file_path.open("rb") as file:
        header = file.read(4)

        file.seek(-4, 2)
        footer = file.read(4)

    if header != b"PAR1" or footer != b"PAR1":
        raise ValueError("Invalid Parquet file signature.")

    print("Parquet validation: SUCCESS")


# ============================================================
# 4. FILE DOWNLOAD
# ============================================================

def download_file(source_url: str, output_path: Path) -> None:
    """Download a file in chunks with basic integrity checks."""

    temp_path = output_path.with_name(
        output_path.name + ".part"
    )

    downloaded_bytes = 0

    try:
        with urlopen(source_url, timeout=60) as response:

            if response.status != 200:
                raise ValueError(
                    f"Unexpected HTTP status: {response.status}"
                )

            expected_size = response.headers.get("Content-Length")

            with temp_path.open("wb") as file:

                while True:
                    chunk = response.read(CHUNK_SIZE)

                    if not chunk:
                        break

                    file.write(chunk)
                    downloaded_bytes += len(chunk)

        if downloaded_bytes == 0:
            raise ValueError("Downloaded file is empty.")

        if expected_size is not None:
            if downloaded_bytes != int(expected_size):
                raise ValueError("Incomplete download detected.")

        validate_parquet_file(temp_path)

        temp_path.replace(output_path)

        print("Download: SUCCESS")

    except (HTTPError, URLError, TimeoutError, OSError, ValueError):
        temp_path.unlink(missing_ok=True)
        raise


# ============================================================
# 5. MANIFEST GENERATION
# ============================================================

def generate_manifest(
    file_path: Path,
    checksum: str
) -> dict:
    """Build the ingestion manifest metadata."""

    manifest = {
        "batch_id": f"yellow_{YEAR}_{MONTH:02d}",
        "source_url": SOURCE_URL,
        "file_name": file_path.name,
        "year": YEAR,
        "month": MONTH,
        "file_size_bytes": file_path.stat().st_size,
        "sha256": checksum,
        "ingestion_ts_utc": datetime.now(
            timezone.utc
        ).isoformat(),
        "status": "SUCCESS"
    }

    return manifest


# ============================================================
# 6. SAVE MANIFEST AS JSON
# ============================================================

def save_manifest(manifest: dict, manifest_path: Path) -> None:
    """Save the manifest as a formatted JSON file."""

    with manifest_path.open("w", encoding="utf-8") as file:
        json.dump(
            manifest,
            file,
            indent=4,
            ensure_ascii=False
        )

    print("Manifest created:", manifest_path)


# ============================================================
# 7. MAIN INGESTION PIPELINE
# ============================================================

def main() -> None:

    print("\n========== NYC TAXI BATCH INGESTION ==========\n")

    # Create RAW directory
    RAW_DIR.mkdir(parents=True, exist_ok=True)

    print("Source:", SOURCE_URL)
    print("Destination:", OUTPUT_PATH)

    # Step 1: Download if necessary
    if OUTPUT_PATH.exists():
        print("\nFile already exists. Skipping download.")
    else:
        print("\nStarting download...")
        download_file(SOURCE_URL, OUTPUT_PATH)

    # Step 2: Validate the Parquet file
    print("\nValidating Parquet file...")
    validate_parquet_file(OUTPUT_PATH)

    # Step 3: Calculate SHA-256
    print("\nCalculating SHA-256...")
    checksum = calculate_sha256(OUTPUT_PATH)

    # Step 4: Generate manifest
    print("\nGenerating manifest...")
    manifest = generate_manifest(
        OUTPUT_PATH,
        checksum
    )

    # Step 5: Save manifest
    save_manifest(manifest, MANIFEST_PATH)

    # Step 6: Display summary
    print("\n========== INGESTION SUMMARY ==========")
    print("File:", FILENAME)
    print("Size:", OUTPUT_PATH.stat().st_size, "bytes")
    print("SHA-256:", checksum)
    print("Manifest:", MANIFEST_PATH)
    print("Status: SUCCESS")
    print("=======================================\n")


# ============================================================
# 8. PROGRAM ENTRY POINT
# ============================================================

if __name__ == "__main__":
    main()
