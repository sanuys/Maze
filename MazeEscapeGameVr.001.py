import tkinter as tk
import keyboard

class MazeGame:
    def __init__(self, root):
        self.root = root
        self.root.title("Maze Game - Control with Keyboard")
        self.canvas = tk.Canvas(root, width=350, height=350)
        self.canvas.pack()

        self.cell_size = 50  # ขนาดของช่อง
        self.maze = [
            ["X", "X", "X", "X", "X", "X", "X"],
            ["X", " ", " ", " ", " ", " ", "X"],
            ["X", "X", "X", " ", "X", " ", "E"],
            ["X", " ", "X", " ", "X", " ", "X"],
            ["X", " ", " ", " ", "X", "X", "X"],
            ["X", " ", "X", " ", " ", " ", "X"],
            ["X", "O", "X", "X", "X", "X", "X"]
        ]

        self.player_pos = [6, 1]  # ตำแหน่งเริ่มต้นของ "O"
        self.end_pos = (2, 6)  # ตำแหน่ง "E"
        self.draw_maze()

        # ตั้งค่าการควบคุม
        keyboard.on_press_key("w", lambda _: self.move(-1, 0))  # ขึ้น
        keyboard.on_press_key("s", lambda _: self.move(1, 0))   # ลง
        keyboard.on_press_key("a", lambda _: self.move(0, -1))  # ซ้าย
        keyboard.on_press_key("d", lambda _: self.move(0, 1))   # ขวา

    def draw_maze(self):
        """ วาดเขาวงกตลงบน Canvas """
        self.canvas.delete("all")  # เคลียร์หน้าจอเก่า
        colors = {"X": "black", " ": "white", "O": "green", "E": "red"}

        for y, row in enumerate(self.maze):
            for x, cell in enumerate(row):
                color = colors.get(cell, "white")
                self.canvas.create_rectangle(
                    x * self.cell_size, y * self.cell_size,
                    (x + 1) * self.cell_size, (y + 1) * self.cell_size,
                    fill=color, outline="black"
                )

    def move(self, dy, dx):
        """ เคลื่อนที่ตามปุ่มที่กด """
        new_y = self.player_pos[0] + dy
        new_x = self.player_pos[1] + dx

        if self.maze[new_y][new_x] not in ["X"]:  # ห้ามเดินชนกำแพง
            # เปลี่ยนตำแหน่งเดิมเป็นช่องว่าง
            self.maze[self.player_pos[0]][self.player_pos[1]] = " "

            # อัปเดตตำแหน่งใหม่
            self.player_pos = [new_y, new_x]
            self.maze[new_y][new_x] = "O"

            # รีเฟรชหน้าจอ
            self.draw_maze()

            # ถ้าถึง "E" แสดงข้อความชนะ
            if (new_y, new_x) == self.end_pos:
                print(">>>>> Congratulations!!! <<<<<")

if __name__ == '__main__':
    root = tk.Tk()
    app = MazeGame(root)
    root.mainloop()
