import argparse
import asyncio
import logging
from pathlib import Path
import shutil

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Parse command-line arguments
parser = argparse.ArgumentParser(description="Sort files by extension.")
parser.add_argument("source", help="Path to the source folder")
parser.add_argument("output", help="Path to the output folder")
args = parser.parse_args()

source_dir = Path(args.source)
output_dir = Path(args.output)

# Recursively read the source folder and process files
async def read_folder(source: Path, output: Path):
    logging.info(f"Reading folder: {source}")
    try:
        for item in source.iterdir():
            if item.is_dir():
                # Recursively process subdirectories
                await read_folder(item, output)
            elif item.is_file():
                # Process a single file
                await copy_file(item, output)
    except Exception as e:
        logging.error(f"Error reading folder {source}: {e}")

# Copy a file to a subfolder named by its extension
async def copy_file(file: Path, output_dir: Path):
    try:
        ext = file.suffix.lower().strip(".") or "no_extension"
        target_folder = output_dir / ext
        target_folder.mkdir(parents=True, exist_ok=True)

        target_path = target_folder / file.name

        # Use shutil to copy the file (no async copy available)
        shutil.copy2(file, target_path)

        logging.info(f"Copied {file} to {target_path}")
    except Exception as e:
        logging.error(f"Failed to copy {file}: {e}")

# Main async entry point
async def main():
    logging.info(f"Sorting files from {source_dir} to {output_dir}...")
    await read_folder(source_dir, output_dir)

if __name__ == "__main__":
    asyncio.run(main())
