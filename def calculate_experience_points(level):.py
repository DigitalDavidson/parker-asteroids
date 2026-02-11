def calculate_experience_points(level):
    """Calculate the experience points required for a given level.

    Args:
        level (int): The level for which to calculate experience points.
    Returns:
        int: The experience points required for the given level.
    """
    if level < 1:
        raise ValueError("Level must be at least 1.")
    return level ** 3 + 50 * level + 100
# Example usage:
if __name__ == "__main__":
    level = 5
    xp = calculate_experience_points(level)
    print(f"Experience points required for level {level}: {xp}")
def calculate_experience_points(level):
    """Calculate the experience points required for a given level.

    Args:
        level (int): The level for which to calculate experience points.
    Returns:
        int: The experience points required for the given level.
    """
    if level < 1:
        raise ValueError("Level must be at least 1.")
    return level ** 3 + 50 * level + 100
