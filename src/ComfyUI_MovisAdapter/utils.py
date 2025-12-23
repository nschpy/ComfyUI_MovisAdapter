"""
Utility functions for ComfyUI MovisAdapter.
"""

import hashlib
import os


def strip_path(path: str) -> str:
    """
    Strip subfolder prefix from path if present.

    Args:
        path: File path potentially with subfolder prefix

    Returns:
        Cleaned path string
    """
    # Remove any [subfolder] prefix that ComfyUI might add
    if path.startswith("[") and "]" in path:
        return path.split("]", 1)[1].strip()
    return path


def calculate_file_hash(filepath: str, hash_every_n: int = 1) -> str:
    """
    Calculate hash of a file for cache invalidation.

    Args:
        filepath: Path to file to hash
        hash_every_n: Read every nth byte (1 = full file)

    Returns:
        Hash string combining file stats and content hash
    """
    if not os.path.exists(filepath):
        return "0"

    # Get file stats
    stats = os.stat(filepath)
    file_size = stats.st_size
    file_mtime = stats.st_mtime

    # For small files or hash_every_n=1, hash the entire file
    # For large files, sample bytes for performance
    hash_md5 = hashlib.md5()

    try:
        with open(filepath, "rb") as f:
            if hash_every_n == 1 or file_size < 1024 * 1024:  # < 1MB
                # Hash entire file
                for chunk in iter(lambda: f.read(4096), b""):
                    hash_md5.update(chunk)
            else:
                # Sample bytes for large files
                bytes_read = 0
                while bytes_read < file_size:
                    chunk = f.read(4096)
                    if not chunk:
                        break
                    hash_md5.update(chunk)
                    bytes_read += 4096 * hash_every_n
                    f.seek(bytes_read)
    except Exception:
        # If we can't read the file, just use file stats
        pass

    # Combine file metadata with content hash
    return f"{file_size}_{file_mtime}_{hash_md5.hexdigest()}"
