import random
import pygame

class Shuffle:
    def __init__(self, memory_pictures, hidden_images, nem_pics, nem_pics_rect, rows, cols, left_margin, top_margin, pic_size, padding):
        self.memory_pictures = memory_pictures
        self.hidden_images = hidden_images
        self.nem_pics = nem_pics
        self.nem_pics_rect = nem_pics_rect
        self.rows = rows
        self.cols = cols
        self.left_margin = left_margin
        self.top_margin = top_margin
        self.pic_size = pic_size
        self.padding = padding

    def shuffle_unmatched_cards(self):
        # Get the indices of all unmatched (hidden) and non-bomb cards
        unmatched_indices = [
            i for i, (pic, hidden) in enumerate(zip(self.memory_pictures, self.hidden_images)) 
            if not hidden and pic != "bomb"  # Only shuffle cards that are not bombs
        ]
        unmatched_pictures = [self.memory_pictures[idx] for idx in unmatched_indices]
        random.shuffle(unmatched_pictures)  # Shuffle the unmatched cards

        # Update the memoryPictures array with the shuffled unmatched cards
        for i, idx in enumerate(unmatched_indices):
            self.memory_pictures[idx] = unmatched_pictures[i]
            self.nem_pics[idx] = pygame.image.load(f"images/{unmatched_pictures[i]}.png")
            self.nem_pics[idx] = pygame.transform.scale(self.nem_pics[idx], (self.pic_size, self.pic_size))

        # Update the card positions in nemPicsRect (no need to shuffle positions)
        for idx, rect in enumerate(self.nem_pics_rect):
            rect.update(
                self.left_margin + (idx % self.cols) * (self.pic_size + self.padding),
                self.top_margin + (idx // self.cols) * (self.pic_size + self.padding),
                self.pic_size, self.pic_size,
            )