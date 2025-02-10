import turtle

PART_OF_PATH = 'O'
TRIED = '.'
OBSTACLE = '+'
DEAD_END = '-'

class Maze:
    def __init__(self, maze_file_name):
        self.maze_list = []
        rows_in_maze = 0
        with open(maze_file_name, 'r') as maze_file:
            for line in maze_file:
                row_list = []
                for col, ch in enumerate(line.strip()):
                    row_list.append(ch)
                    if ch == 'S':
                        self.start_row = rows_in_maze
                        self.start_col = col
                self.maze_list.append(row_list)
                rows_in_maze += 1

        self.rows_in_maze = rows_in_maze
        self.columns_in_maze = len(self.maze_list[0]) if self.maze_list else 0
        self.x_translate = -self.columns_in_maze / 2
        self.y_translate = self.rows_in_maze / 2

        self.t = turtle.Turtle()
        self.t.shape('turtle')
        self.wn = turtle.Screen()
        self.wn.setworldcoordinates(
            - (self.columns_in_maze - 1) / 2 - 0.5,
            - (self.rows_in_maze - 1) / 2 - 0.5,
            (self.columns_in_maze - 1) / 2 + 0.5,
            (self.rows_in_maze - 1) / 2 + 0.5
        )
        self.wn.bgcolor('lightblue') 

    def draw_maze(self):
        self.t.speed(0)  # ตั้งค่าให้วาดเร็วขึ้น
        for y in range(self.rows_in_maze):
            for x in range(self.columns_in_maze):
                if self.maze_list[y] [x] == OBSTACLE:
                    self.draw_centered_box(x + self.x_translate, -y + self.y_translate, 'orange')  # เปลี่ยนเป็นสีน้ำตาล
        self.t.color('black')
        self.t.fillcolor('blue')
    def draw_centered_box(self, x, y, color):
        self.t.up()
        self.t.goto(x - 0.5, y - 0.5)
        self.t.color(color)
        self.t.fillcolor(color)
        self.t.setheading(90)
        self.t.down()
        self.t.begin_fill()
        for _ in range(4):
            self.t.forward(1)
            self.t.right(90)
        self.t.end_fill()

    def move_turtle(self, x, y):
        self.t.up()
        self.t.setheading(self.t.towards(x + self.x_translate, -y + self.y_translate))
        self.t.goto(x + self.x_translate, -y + self.y_translate)

    def drop_bread_crumb(self, color):
        self.t.dot(10, color)

    def update_position(self, row, col, val=None):
        if val:
            self.maze_list[row][col] = val
        self.move_turtle(col, row)
        color_map = {
            PART_OF_PATH: 'green',  # เส้นทางที่เดินผ่าน (จุดสีเขียว)
            OBSTACLE: 'saddlebrown',  # กำแพง (น้ำตาล)
            TRIED: 'yellow',  # ทางที่ลองแล้ว (จุดสีเขียว)
            DEAD_END: 'red'  # ทางตัน (จุดสีแดง)
        }
        if val in color_map:
            self.drop_bread_crumb(color_map[val])

    def is_exit(self, row, col):
        return row == 0 or row == self.rows_in_maze - 1 or col == 0 or col == self.columns_in_maze - 1

    def __getitem__(self, idx):
        return self.maze_list[idx]


def search_from(maze, start_row, start_column):
    if maze[start_row][start_column] in (OBSTACLE, TRIED, DEAD_END):
        return False

    if maze.is_exit(start_row, start_column):
        maze.update_position(start_row, start_column, PART_OF_PATH)
        return True

    maze.update_position(start_row, start_column, TRIED)

    found = (
        search_from(maze, start_row - 1, start_column) or
        search_from(maze, start_row + 1, start_column) or
        search_from(maze, start_row, start_column - 1) or
        search_from(maze, start_row, start_column + 1)
    )

    if found:
        maze.update_position(start_row, start_column, PART_OF_PATH)
    else:
        maze.update_position(start_row, start_column, DEAD_END)

    return found


# โหลดเขาวงกตและเริ่มค้นหาเส้นทาง
my_maze = Maze('maze1.txt')
my_maze.draw_maze()
my_maze.update_position(my_maze.start_row, my_maze.start_col)
search_from(my_maze, my_maze.start_row, my_maze.start_col)

turtle.done()
