def shuffle_unmatched_cards(memoryPictures, hiddenImages, nemPics, nemPicsRect, rows, cols):
    # Get the indices of all unmatched (hidden) and non-bomb cards
    unmatched_indices = [
        i for i, (pic, hidden) in enumerate(zip(memoryPictures, hiddenImages)) 
        if not hidden and pic != "bomb"  # Only shuffle cards that are not bombs
    ]
    unmatched_pictures = [memoryPictures[idx] for idx in unmatched_indices]
    random.shuffle(unmatched_pictures)  # Shuffle the unmatched cards

    # Update the memoryPictures array with the shuffled unmatched cards
    for i, idx in enumerate(unmatched_indices):
        memoryPictures[idx] = unmatched_pictures[i]
        if unmatched_pictures[i] != "bomb":
            nemPics[idx] = pygame.image.load(f"images/{unmatched_pictures[i]}.png")
            nemPics[idx] = pygame.transform.scale(nemPics[idx], (picSize, picSize))

    # Update the card positions in nemPicsRect (no need to shuffle positions)
    for idx, rect in enumerate(nemPicsRect):
        rect.update(
            leftMargin + (idx % cols) * (picSize + padding),
            topMargin + (idx // cols) * (picSize + padding),
            picSize, picSize,
        )