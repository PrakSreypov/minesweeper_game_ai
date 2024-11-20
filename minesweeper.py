import random

class Minesweeper():
    """
    Represents the Minesweeper game board and mine positions
    
    """

    def __init__(self, height=8, width=8, mines=8):

        # Set initial width, height, and number of mines
        self.height = height
        self.width = width
        self.mines = set()

        # Initialize an empty field with no mines
        self.board = []
        for i in range(self.height):
            row = []
            for j in range(self.width):
                row.append(False)
            self.board.append(row)

        # Add mines randomly
        while len(self.mines) != mines:
            i = random.randrange(height)
            j = random.randrange(width)
            if not self.board[i][j]:
                self.mines.add((i, j))
                self.board[i][j] = True

        # At first, player has found no mines
        self.mines_found = set()

    def print(self):
        """
        Prints a text-based representation
        of where mines are located.
        """
        for i in range(self.height):
            print("--" * self.width + "-")
            for j in range(self.width):
                if self.board[i][j]:
                    print("|X", end="")
                else:
                    print("| ", end="")
            print("|")
        print("--" * self.width + "-")

    # Checks if a specific cell contains a mine.
    def is_mine(self, cell):
        i, j = cell
        return self.board[i][j]

    def nearby_mines(self, cell):
        """
        Counts the number of mines around a specific cell.
        """

        # Keep count of nearby mines
        count = 0

        # Loop over all cells within one row and column
        for i in range(cell[0] - 1, cell[0] + 2):
            for j in range(cell[1] - 1, cell[1] + 2):

                # Ignore the cell itself
                if (i, j) == cell:
                    continue

                # Update count if cell in bounds and is mine
                if 0 <= i < self.height and 0 <= j < self.width:
                    if self.board[i][j]:
                        count += 1

        return count

    def won(self):
        """
        Checks if all mines have been flagged.
        """
        return self.mines_found == self.mines


class Sentence():
    """
    >>>>> Solver: Represents a logical statement about Minesweeper cells (e.g., "these cells contain X mines").
    """

    def __init__(self, cells, count):
        self.cells = set(cells)
        self.count = count

    def __eq__(self, other):
        return self.cells == other.cells and self.count == other.count

    def __str__(self):
        return f"{self.cells} = {self.count}"

    def known_mines(self):
        """
        >>>>> Solver: Returns cells that are definitely mines based on this sentence.
        Used to mark mines in the AI's knowledge base.

        """
        if len(self.cells) == self.count:
            return self.cells
        return None

    def known_safes(self):
        """
        >>>>> Solver: Returns cells that are definitely safe based on this sentence.
        Used to mark safes in the AI's knowledge base.
        """
        if self.count == 0:
            return self.cells
        return None

    def mark_mine(self, cell):
        """
        >>>>> Solver: Updates the sentence to account for a known mine, reducing the count.
        Critical for reasoning about remaining unknown cells.
        """

        newCells = set()
        for item in self.cells:
            if item != cell:
                newCells.add(item)
            else:
                self.count -= 1
        self.cells = newCells

    def mark_safe(self, cell):
        """
        >>>>> Solver: Updates the sentence to account for a known safe cell.
        Helps refine logical deductions about other cells.
        """
        newCells = set()
        for item in self.cells:
            if item != cell:
                newCells.add(item)
        self.cells = newCells
        


class MinesweeperAI():
    """
    >>>>> Solver: AI logic to deduce safe moves and mines using knowledge-based reasoning.

    """

    def __init__(self, height=8, width=8):

        # Set initial height and width
        self.height = height
        self.width = width

        # Keep track of which cells have been clicked on
        self.moves_made = set()

        # Keep track of cells known to be safe or mines
        self.mines = set()
        self.safes = set()

        # List of sentences about the game known to be true
        self.knowledge = []

    def mark_mine(self, cell):

        """
        >>>>> Solver: Marks a cell as a mine and updates the knowledge base to reflect this information.
              Ensures the AI avoids choosing this cell in future moves.
        """
        self.mines.add(cell)
        for sentence in self.knowledge:
            sentence.mark_mine(cell)

    def mark_safe(self, cell):
        """
        >>>>> Solver: Marks a cell as safe and updates the knowledge base.
              This allows the AI to confidently choose this cell in future moves.
        """

        self.safes.add(cell)
        for sentence in self.knowledge:
            sentence.mark_safe(cell)

    def add_knowledge(self, cell, count):
        """
        >>>>> Solver: Updates AI's knowledge when a safe cell and its nearby mine count are revealed.

        Steps:
        1) Mark the revealed cell as safe.
        2) Add a new logical sentence to the knowledge base, based on the cell's neighbors.
        3) Deduce new safes and mines from existing knowledge.
        4) Infer additional sentences by comparing current sentences in the knowledge base.
        """

        # Mark cell as safe and add to moves_made
        self.mark_safe(cell)
        self.moves_made.add(cell)

        # Create and Add sentence to knowledge
        neighbors, count = self.get_cell_neighbors(cell, count)
        sentence = Sentence(neighbors, count)
        self.knowledge.append(sentence)

        # Conclusion
        new_inferences = []
        for s in self.knowledge:
            if s == sentence:
                continue
            elif s.cells.issuperset(sentence.cells):
                setDiff = s.cells-sentence.cells
                # Known safes
                if s.count == sentence.count:
                    for safeFound in setDiff:
                        self.mark_safe(safeFound)
                # Known mines
                elif len(setDiff) == s.count - sentence.count:
                    for mineFound in setDiff:
                        self.mark_mine(mineFound)
                # Known inference
                else:
                    new_inferences.append(
                        Sentence(setDiff, s.count - sentence.count)
                    )
            elif sentence.cells.issuperset(s.cells):
                setDiff = sentence.cells-s.cells
                # Known safes
                if s.count == sentence.count:
                    for safeFound in setDiff:
                        self.mark_safe(safeFound)
                # Known mines
                elif len(setDiff) == sentence.count - s.count:
                    for mineFound in setDiff:
                        self.mark_mine(mineFound)
                # Known inference
                else:
                    new_inferences.append(
                        Sentence(setDiff, sentence.count - s.count)
                    )

        self.knowledge.extend(new_inferences)
        self.remove_dups()
        self.remove_sures()

    def make_safe_move(self):
        """
        >>>>> Solver: Chooses a cell that is known to be safe based on the knowledge base.
        This ensures the AI avoids triggering a mine.

        """
        safeCells = self.safes - self.moves_made
        if not safeCells:
            return None
        # print(f"Pool: {safeCells}")
        move = safeCells.pop()
        return move

    def make_random_move(self):
        """
        >>>>> Solver: Selects a random move from unexplored cells that are not known to be mines.
              Used as a fallback when no logical safe moves are available.

        """
        all_moves = set()
        for i in range(self.height):
            for j in range(self.width):
                if (i,j) not in self.mines and (i,j) not in self.moves_made:
                    all_moves.add((i,j))
        # No moves left
        if len(all_moves) == 0:
            return None
        # Return available
        move = random.choice(tuple(all_moves))
        return move

    # ---------------- Helper function ----------------        
    def get_cell_neighbors(self, cell, count):

        """
        >>>>> Solver: Identifies all neighboring cells of a given cell that are not already known to be safe or mines.
              Adjusts the count of nearby mines based on known mines.
              This is crucial for constructing new logical sentences.

        """

        i, j = cell
        neighbors = []

        for row in range(i-1, i+2):
            for col in range(j-1, j+2):
                if (row >= 0 and row < self.height) \
                and (col >= 0 and col < self.width) \
                and (row, col) != cell \
                and (row, col) not in self.safes \
                and (row, col) not in self.mines:
                    neighbors.append((row, col))
                if (row, col) in self.mines:
                    count -= 1

        return neighbors, count

    def remove_dups(self):
        """
        >>>>> Solver: Removes duplicate sentences from the knowledge base.
              Keeps the reasoning process efficient and avoids redundant checks.
        """
        unique_knowledge = []
        for s in self.knowledge:
            if s not in unique_knowledge:
                unique_knowledge.append(s)
        self.knowledge = unique_knowledge

    def remove_sures(self):
        """
        >>>> Solver: Processes sentences in the knowledge base to identify and handle fully solved sentences:
        - Marks all cells as safe if the sentence contains no mines.
        - Marks all cells as mines if the sentence's count equals its size.
        
        """
        final_knowledge = []
        for s in self.knowledge:
            final_knowledge.append(s)
            if s.known_mines():
                for mineFound in s.known_mines():
                    self.mark_mine(mineFound)
                final_knowledge.pop(-1)
            elif s.known_safes():
                for safeFound in s.known_safes():
                    self.mark_safe(safeFound)
                final_knowledge.pop(-1)
        self.knowledge = final_knowledge
