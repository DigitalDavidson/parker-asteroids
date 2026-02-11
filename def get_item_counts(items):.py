def get_item_counts(items):
    potion_count = 0
    bread_count = 0
    shortsword_count = 0

    # don't touch above this line

    for item in items:
        if item == "Potion":
            potion_count += 1
        elif item == "Bread":
            bread_count += 1
        elif item == "Shortsword":
            shortsword_count += 1

    # don't touch below this line

    return potion_count, bread_count, shortsword_count
