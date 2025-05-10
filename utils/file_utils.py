import os
def walk_files(path, file_types=[]):
    """
    Walk through the directory and yield file paths.

    Args:
        path (str): The directory path to walk through.
        file_types (list, optional): List of file extensions to filter by. Defaults to None.

    Yields:
        str: File paths that match the specified file types.
    """
    return_files = []
    for root, _, files in os.walk(path):
        for file in files:
            if file_types is None or any(file.endswith(ext) for ext in file_types):
                # yield os.path.join(root, file)
                return_files.append(os.path.join(root, file))
    return return_files