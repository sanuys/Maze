import tkinter as tk
import time
import keyboard
from Stack import Stack

class MazeApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Maze Solver")
        self.canvas = tk.Canvas(root, width=350, height=350)
        self.canvas.pack()
        
        self.cell_size = 50  # ขนาดของแต่ละช่อง
        self.maze = [
            ["X", "X", "X", "X", "X", "X", "X"],
            ["X", " ", " ", " ", " ", " ", "X"],
            ["X", "X", "X", " ", "X", " ", "E"],
            ["X", " ", "X", " ", "X", " ", "X"],
            ["X", " ", " ", " ", "X", "X", "X"],
            ["X", " ", "X", " ", " ", " ", "X"],
            ["X", "O", "X", "X", "X", "X", "X"]
        ]
        self.start = (6, 1)
        self.end = (2, 6)
        self.directions = {1: (-1, 0), 2: (1, 0), 3: (0, -1), 4: (0, 1)}
        
        self.visited = set()
        self.dead_end = set()
        self.path = []
        self.stack = Stack()
        self.stack.push(self.start)

        self.draw_maze()
        self.root.after(500, self.solve_maze)  # เริ่มแก้ Maze

    def draw_maze(self):
        """ วาดเขาวงกตลงบน Canvas """
        self.canvas.delete("all")  # ล้างหน้าจอทุกครั้งที่อัปเดต
        colors = {"X": "black", " ": "white", "O": "green", "E": "red", ".": "gray", "I": "yellow"}
        
        for y, row in enumerate(self.maze):
            for x, cell in enumerate(row):
                color = colors.get(cell, "white")
                self.canvas.create_rectangle(
                    x * self.cell_size, y * self.cell_size,
                    (x + 1) * self.cell_size, (y + 1) * self.cell_size,
                    fill=color, outline="black"
                )

    def solve_maze(self):
        """ ใช้ DFS + Backtracking แก้ปัญหา Maze """
        if self.stack.isEmpty():
            print("No path to the exit.")
            return
        
        current_y, current_x = self.stack.pop()
        self.maze[current_y][current_x] = "O"  # อัปเดตตำแหน่ง
        self.visited.add((current_y, current_x))
        self.draw_maze()
        self.root.update()
        time.sleep(0.2)  # ทำให้ดูเหมือนเคลื่อนที่

        if (current_y, current_x) == self.end:
            print(">>>>> Congratulations!!! <<<<<")
            return

        possible_moves = []

        for direction in [1, 2, 3, 4]:
            dy, dx = self.directions[direction]
            next_y, next_x = current_y + dy, current_x + dx

            if (0 <= next_y < len(self.maze) and 0 <= next_x < len(self.maze[0]) and
                    (next_y, next_x) not in self.visited and
                    (next_y, next_x) not in self.dead_end and
                    self.maze[next_y][next_x] in [" ", "E"]):
                possible_moves.append((next_y, next_x))

        if possible_moves:
            for move in possible_moves:
                self.stack.push(move)
            if self.path:
                prev_y, prev_x = self.path[-1]
                self.maze[prev_y][prev_x] = "."
            self.path.append((current_y, current_x))
        else:
            self.dead_end.add((current_y, current_x))
            self.maze[current_y][current_x] = "I"
            self.draw_maze()
            self.root.update()
            time.sleep(0.1)

            while self.path:
                back_y, back_x = self.path.pop()
                if any(
                    (back_y + dy, back_x + dx) in self.visited and
                    self.maze[back_y + dy][back_x + dx] in [" ", "E"]
                    for dy, dx in self.directions.values()
                ):
                    break

        self.root.after(100, self.solve_maze)  # เรียกตัวเองซ้ำทุก 100 มิลลิวินาที


if __name__ == '__main__':
    root = tk.Tk()
    app = MazeApp(root)
    root.mainloop()
