from IPython.core.magic import register_line_magic


@register_line_magic
def pathsetup(line):
    """Custom line magic for adding the git repository root and
    a space-delimited list of subdirectories to the system path
    """
    # Doing these imports inside the function so that they don't
    # end up in the interactive notebook environment
    import os
    import sys
    import git

    repo_root = git.Repo(".", search_parent_directories=True).working_tree_dir
    if repo_root not in sys.path:
        sys.path.append(repo_root)

    subdirs = line.split(" ")
    for subdir in subdirs:
        new_item = os.path.join(repo_root, subdir)
        if new_item not in sys.path:
            sys.path.append(new_item)

    return (
        f"Updated sys path to include repository root and as well as subdirs {subdirs}"
    )


# In an interactive session, we need to delete these to avoid
# name conflicts for automagic to work on line magics.
del pathsetup
