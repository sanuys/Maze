#อันนี้ไม่ไช่ final จริงนะครับมันวาป
import os
import time
from Stack import Stack

class maze:
    def __init__(self) -> None:
        self.maze = [
            ["X", "X", "X", "X", "X", "X", "X"],
            ["X", " ", " ", " ", " ", " ", "X"],
            ["X", "X", "X", " ", "X", " ", " "],
            ["X", " ", "X", " ", "X", " ", "X"],
            ["X", " ", " ", " ", "X", "X", "X"],
            ["X", " ", "X", " ", " ", " ", "X"],
            ["X", " ", "X", "X", "X", "X", "X"]
        ]
        self.ply = pos(6, 1)  # จุดเริ่มต้น
        self.end = pos(2, 6)  # จุดสิ้นสุด
        self.maze[self.ply.y][self.ply.x] = "O"
        self.maze[self.end.y][self.end.x] = "E"
        self.directions = {1: (-1, 0), 2: (1, 0), 3: (0, -1), 4: (0, 1)}

    def isInBound(self, y, x):
        return 0 <= y < len(self.maze) and 0 <= x < len(self.maze[0])

    def print(self):
        os.system("cls" if os.name == "nt" else "clear")
        print("\n\n\n")
        for row in self.maze:
            print(" ".join(row))
        print("\n\n\n")

    def printEND(self):
        os.system("cls" if os.name == "nt" else "clear")
        print("\n\n\n")
        print(">>>>> Congratulations!!! <<<<<")
        print("\n\n\n")

    def Visited(self):
        stack = Stack()
        stack.push((self.ply.y, self.ply.x))  # เพิ่มตำแหน่งเริ่มต้นลงใน Stack
        visited = set()  # ใช้เก็บตำแหน่งที่เคยไปมาแล้ว

        while not stack.isEmpty():
            current_y, current_x = stack.pop()
            self.ply.y, self.ply.x = current_y, current_x  # อัปเดตตำแหน่ง "O"
            self.maze[current_y][current_x] = "O"  # วาง "O" ที่ตำแหน่งปัจจุบัน
            self.print()  # แสดงเขาวงกต
            time.sleep(0.25)  # ดีเลย์เพื่อแสดงการเคลื่อนไหว

            # ถ้าถึงตำแหน่งเป้าหมาย
            if (current_y, current_x) == (self.end.y, self.end.x):
                self.printEND()
                return True

            # ทำเครื่องหมายตำแหน่งนี้ว่าเยี่ยมชมแล้ว
            visited.add((current_y, current_x))

            # ตรวจสอบตำแหน่งรอบ ๆ (บน, ล่าง, ซ้าย, ขวา)
            for direction in [1, 2, 3, 4]:
                dy, dx = self.directions[direction]
                next_y, next_x = current_y + dy, current_x + dx

                # ถ้าตำแหน่งถัดไปอยู่ในเขตและยังไม่ได้เยี่ยมชม
                if self.isInBound(next_y, next_x) and (next_y, next_x) not in visited:
                    if self.maze[next_y][next_x] in [" ", "E"]:  # ถ้าตำแหน่งถัดไปว่างหรือเป็นเป้าหมาย
                        stack.push((next_y, next_x))  # เพิ่มลงใน Stack

            # คืนตำแหน่งเดิมเป็น " " ถ้าไม่ใช่เป้าหมาย
            if (current_y, current_x) != (self.end.y, self.end.x):
                self.maze[current_y][current_x] = "."

        print("No path to the exit.")
        return False


class pos:
    def __init__(self, y, x) -> None:
        self.y = y
        self.x = x


if __name__ == '__main__':
    m = maze()
    m.print()
    m.Visited()  # เรียกใช้ฟังก์ชันเพื่อให้ "O" เดินออกจากเขาวงกต
