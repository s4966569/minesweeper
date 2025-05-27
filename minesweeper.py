import random
import os

class Minesweeper:
    def __init__(self, rows=10, cols=10, mines=10):
        self.rows = rows
        self.cols = cols
        self.mines = mines
        self.board = [[0 for _ in range(cols)] for _ in range(rows)]
        self.revealed = [[False for _ in range(cols)] for _ in range(rows)]
        self.flagged = [[False for _ in range(cols)] for _ in range(rows)]
        self.game_over = False
        self.won = False
        self.first_move = True
        
    def place_mines(self, first_row, first_col):
        """在棋盘上随机放置地雷，避开第一次点击的位置"""
        mines_placed = 0
        while mines_placed < self.mines:
            row = random.randint(0, self.rows - 1)
            col = random.randint(0, self.cols - 1)
            
            # 避开第一次点击的位置和已经有地雷的位置
            if (row != first_row or col != first_col) and self.board[row][col] != -1:
                self.board[row][col] = -1  # -1 表示地雷
                mines_placed += 1
                
        # 计算每个非地雷格子周围的地雷数量
        self.calculate_numbers()
    
    def calculate_numbers(self):
        """计算每个非地雷格子周围的地雷数量"""
        directions = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]
        
        for row in range(self.rows):
            for col in range(self.cols):
                if self.board[row][col] != -1:  # 如果不是地雷
                    count = 0
                    for dr, dc in directions:
                        new_row, new_col = row + dr, col + dc
                        if (0 <= new_row < self.rows and 0 <= new_col < self.cols 
                            and self.board[new_row][new_col] == -1):
                            count += 1
                    self.board[row][col] = count
    
    def reveal_cell(self, row, col):
        """揭开一个格子"""
        if (row < 0 or row >= self.rows or col < 0 or col >= self.cols 
            or self.revealed[row][col] or self.flagged[row][col]):
            return
        
        # 如果是第一次移动，先放置地雷
        if self.first_move:
            self.place_mines(row, col)
            self.first_move = False
        
        self.revealed[row][col] = True
        
        # 如果踩到地雷
        if self.board[row][col] == -1:
            self.game_over = True
            return
        
        # 如果是空格子（周围没有地雷），自动揭开周围的格子
        if self.board[row][col] == 0:
            directions = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]
            for dr, dc in directions:
                self.reveal_cell(row + dr, col + dc)
    
    def toggle_flag(self, row, col):
        """切换标记状态"""
        if (0 <= row < self.rows and 0 <= col < self.cols 
            and not self.revealed[row][col]):
            self.flagged[row][col] = not self.flagged[row][col]
    
    def check_win(self):
        """检查是否获胜"""
        for row in range(self.rows):
            for col in range(self.cols):
                # 如果有非地雷格子没有被揭开，游戏还没结束
                if self.board[row][col] != -1 and not self.revealed[row][col]:
                    return False
        self.won = True
        return True
    
    def display_board(self, show_mines=False):
        """显示棋盘"""
        os.system('cls' if os.name == 'nt' else 'clear')  # 清屏
        
        print("   ", end="")
        for col in range(self.cols):
            print(f"{col:2}", end=" ")
        print()
        
        for row in range(self.rows):
            print(f"{row:2} ", end="")
            for col in range(self.cols):
                if self.flagged[row][col] and not show_mines:
                    print(" F", end=" ")
                elif self.revealed[row][col] or show_mines:
                    if self.board[row][col] == -1:
                        print(" *", end=" ")
                    elif self.board[row][col] == 0:
                        print("  ", end=" ")
                    else:
                        print(f" {self.board[row][col]}", end=" ")
                else:
                    print(" ■", end=" ")
            print()
        print()
    
    def get_user_input(self):
        """获取用户输入"""
        while True:
            try:
                action = input("输入操作 (r:揭开, f:标记, q:退出): ").lower().strip()
                if action == 'q':
                    return 'quit', 0, 0
                elif action in ['r', 'f']:
                    coords = input("输入坐标 (行 列): ").strip().split()
                    if len(coords) == 2:
                        row, col = int(coords[0]), int(coords[1])
                        if 0 <= row < self.rows and 0 <= col < self.cols:
                            return action, row, col
                        else:
                            print(f"坐标超出范围！请输入 0-{self.rows-1} 和 0-{self.cols-1} 之间的数字。")
                    else:
                        print("请输入两个数字，用空格分隔。")
                else:
                    print("无效操作！请输入 r（揭开）、f（标记）或 q（退出）。")
            except ValueError:
                print("请输入有效的数字！")
    
    def play(self):
        """主游戏循环"""
        print("=" * 50)
        print("欢迎来到扫雷游戏！")
        print(f"棋盘大小: {self.rows}x{self.cols}")
        print(f"地雷数量: {self.mines}")
        print("=" * 50)
        print("操作说明:")
        print("r - 揭开格子")
        print("f - 标记/取消标记地雷")
        print("q - 退出游戏")
        print("■ - 未揭开的格子")
        print("F - 标记的格子")
        print("* - 地雷")
        print("数字 - 周围地雷的数量")
        print("=" * 50)
        
        while not self.game_over and not self.won:
            self.display_board()
            
            # 显示游戏状态
            revealed_count = sum(sum(row) for row in self.revealed)
            total_safe = self.rows * self.cols - self.mines
            print(f"已揭开: {revealed_count}/{total_safe}")
            
            action, row, col = self.get_user_input()
            
            if action == 'quit':
                print("游戏退出。")
                return
            elif action == 'r':
                self.reveal_cell(row, col)
            elif action == 'f':
                self.toggle_flag(row, col)
            
            # 检查游戏状态
            if not self.game_over:
                self.check_win()
        
        # 游戏结束，显示最终棋盘
        self.display_board(show_mines=True)
        
        if self.game_over:
            print("💥 Game Over! 你踩到地雷了！")
        elif self.won:
            print("🎉 Congratulations! You Win! 恭喜你成功扫雷！")

def main():
    """主函数"""
    print("扫雷游戏设置")
    
    # 获取游戏设置
    while True:
        try:
            difficulty = input("选择难度 (1:简单 9x9/10雷, 2:中等 16x16/40雷, 3:困难 16x30/99雷, 4:自定义): ").strip()
            
            if difficulty == '1':
                rows, cols, mines = 9, 9, 10
                break
            elif difficulty == '2':
                rows, cols, mines = 16, 16, 40
                break
            elif difficulty == '3':
                rows, cols, mines = 16, 30, 99
                break
            elif difficulty == '4':
                rows = int(input("输入行数: "))
                cols = int(input("输入列数: "))
                max_mines = rows * cols - 1
                mines = int(input(f"输入地雷数量 (最多 {max_mines}): "))
                
                if rows < 1 or cols < 1 or mines < 1 or mines >= rows * cols:
                    print("无效的设置！请重新输入。")
                    continue
                break
            else:
                print("请输入 1、2、3 或 4。")
        except ValueError:
            print("请输入有效的数字！")
    
    # 开始游戏
    game = Minesweeper(rows, cols, mines)
    game.play()
    
    # 询问是否再玩一局
    while True:
        play_again = input("\n是否再玩一局？(y/n): ").lower().strip()
        if play_again in ['y', 'yes', '是']:
            main()
            break
        elif play_again in ['n', 'no', '否']:
            print("谢谢游玩！")
            break
        else:
            print("请输入 y 或 n。")

if __name__ == "__main__":
    main() 