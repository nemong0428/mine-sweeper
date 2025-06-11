import random
from js import document, window
from pyodide.ffi import create_proxy

class Minesweeper:
    def __init__(self):
        # 게임 설정
        self.SIZE = 6          # 게임판 크기 (8x8)
        self.MINES = 7        # 지뢰 개수
        self.CELL_SIZE = 25    # 각 칸의 픽셀 크기
        
        # 색상 상수
        self.COLOR_BACKGROUND = "#f0f0f0"    # 전체 배경색
        self.COLOR_MINE = "#ff4444"          # 지뢰 칸 색상 (빨간색)
        self.COLOR_REVEALED = "#ffffff"       # 열린 칸 색상 (흰색)
        self.COLOR_HIDDEN = "#cccccc"         # 닫힌 칸 색상 (회색)
        self.COLOR_BORDER = "#999999"         # 테두리 색상
        self.COLOR_TEXT = "#000000"           # 텍스트 색상 (검정색)
        
        # 캔버스 설정
        self.canvas = document.getElementById("game")
        self.canvas.width = self.canvas.height = self.SIZE * self.CELL_SIZE
        self.ctx = self.canvas.getContext("2d")
        
        # 게임 시작
        self.start_new_game()
        
        # 마우스 이벤트 연결
        self.canvas.addEventListener("click", create_proxy(self.handle_left_click))
        self.canvas.addEventListener("contextmenu", create_proxy(self.handle_right_click))
        
        # 첫 화면 그리기
        self.draw_board()
    
    def start_new_game(self):
        # 게임판 초기화 (0으로 채워진 8x8 배열)
        self.board = [[0 for _ in range(self.SIZE)] for _ in range(self.SIZE)]
        
        # 열린 칸 표시 (모두 False로 시작)
        self.revealed = [[False for _ in range(self.SIZE)] for _ in range(self.SIZE)]
        
        # 깃발 표시 (모두 False로 시작)
        self.flagged = [[False for _ in range(self.SIZE)] for _ in range(self.SIZE)]
        
        # 게임 상태
        self.game_over = False
        self.game_won = False
        self.revealed_count = 0
        
        # 랜덤하게 지뢰 배치
        mines_placed = 0
        while mines_placed < self.MINES:
            x = random.randint(0, self.SIZE-1)
            y = random.randint(0, self.SIZE-1)
            
            # 이미 지뢰가 있는 곳이 아니면 지뢰 배치
            if self.board[y][x] != -1:  # -1은 지뢰를 의미
                self.board[y][x] = -1
                mines_placed += 1
        
        # 각 칸의 주변 지뢰 개수 계산
        for y in range(self.SIZE):
            for x in range(self.SIZE):
                if self.board[y][x] != -1:  # 지뢰가 아닌 칸만
                    count = 0
                    # 주변 8칸 확인
                    for dy in [-1, 0, 1]:
                        for dx in [-1, 0, 1]:
                            if dy == 0 and dx == 0:  # 자기 자신은 제외
                                continue
                            ny, nx = y + dy, x + dx
                            # 게임판 범위 내에서 지뢰가 있으면 카운트
                            if 0 <= ny < self.SIZE and 0 <= nx < self.SIZE:
                                if self.board[ny][nx] == -1:
                                    count += 1
                    self.board[y][x] = count
    
    def get_cell_position(self, event):
        # 마우스 클릭 위치를 게임판 좌표로 변환
        rect = self.canvas.getBoundingClientRect()
        x = int((event.clientX - rect.left) / self.CELL_SIZE)
        y = int((event.clientY - rect.top) / self.CELL_SIZE)
        
        # 게임판 범위 내인지 확인
        if 0 <= x < self.SIZE and 0 <= y < self.SIZE:
            return (x, y)
        return (None, None)
    
    def handle_left_click(self, event):
        # 게임이 끝났으면 새 게임 시작
        if self.game_over or self.game_won:
            self.start_new_game()
            self.draw_board()
            return
        
        x, y = self.get_cell_position(event)
        if x is None or self.flagged[y][x]:  # 깃발이 있으면 클릭 무시
            return
        
        # 지뢰를 클릭한 경우
        if self.board[y][x] == -1:
            self.game_over = True
            # 모든 지뢰 표시
            for yy in range(self.SIZE):
                for xx in range(self.SIZE):
                    if self.board[yy][xx] == -1:
                        self.revealed[yy][xx] = True
        else:
            # 안전한 칸을 클릭한 경우
            self.reveal_cell(x, y)
            
            # 승리 조건 확인 (지뢰가 아닌 모든 칸을 열었을 때)
            if self.revealed_count == self.SIZE * self.SIZE - self.MINES:
                self.game_won = True
        
        self.draw_board()
    
    def handle_right_click(self, event):
        event.preventDefault()  # 기본 우클릭 메뉴 방지
        
        if self.game_over or self.game_won:
            return
        
        x, y = self.get_cell_position(event)
        if x is None or self.revealed[y][x]:  # 이미 열린 칸은 깃발 불가
            return
        
        # 깃발 토글 (있으면 제거, 없으면 추가)
        self.flagged[y][x] = not self.flagged[y][x]
        self.draw_board()
    
    def reveal_cell(self, x, y):
        """
        DFS(깊이 우선 탐색) 알고리즘을 사용하여 칸을 여는 함수
        빈 칸(0)을 클릭하면 재귀적으로 주변 칸들을 모두 엽니다.
        """
        # 이미 열렸거나 깃발이 있으면 무시
        if self.revealed[y][x] or self.flagged[y][x]:
            return
        
        # 칸 열기
        self.revealed[y][x] = True
        self.revealed_count += 1
        
        # 빈 칸(0)이면 주변 칸도 자동으로 열기 (DFS 재귀 호출)
        if self.board[y][x] == 0:
            for dy in [-1, 0, 1]:
                for dx in [-1, 0, 1]:
                    if dy == 0 and dx == 0:
                        continue
                    nx, ny = x + dx, y + dy
                    if 0 <= nx < self.SIZE and 0 <= ny < self.SIZE:
                        self.reveal_cell(nx, ny)  # 재귀 호출 (DFS)
    
    def draw_board(self):
        # 전체 배경 그리기
        self.ctx.fillStyle = self.COLOR_BACKGROUND
        self.ctx.fillRect(0, 0, self.SIZE * self.CELL_SIZE, self.SIZE * self.CELL_SIZE)
        
        # 각 칸 그리기
        for y in range(self.SIZE):
            for x in range(self.SIZE):
                screen_x = x * self.CELL_SIZE
                screen_y = y * self.CELL_SIZE
                
                # 칸의 배경색 결정
                if self.revealed[y][x]:
                    if self.board[y][x] == -1:
                        color = self.COLOR_MINE      # 지뢰는 빨간색
                    else:
                        color = self.COLOR_REVEALED  # 열린 칸은 흰색
                else:
                    color = self.COLOR_HIDDEN        # 닫힌 칸은 회색
                
                # 칸 그리기
                self.ctx.fillStyle = color
                self.ctx.fillRect(screen_x, screen_y, self.CELL_SIZE, self.CELL_SIZE)
                
                # 테두리 그리기
                self.ctx.strokeStyle = self.COLOR_BORDER
                self.ctx.strokeRect(screen_x, screen_y, self.CELL_SIZE, self.CELL_SIZE)
                
                # 칸의 내용 그리기
                self.ctx.fillStyle = self.COLOR_TEXT
                self.ctx.font = "12px Arial"
                self.ctx.textAlign = "center"
                text_x = screen_x + self.CELL_SIZE // 2
                text_y = screen_y + self.CELL_SIZE // 2 + 4
                
                if self.flagged[y][x]:
                    # 깃발 표시
                    self.ctx.fillText("F", text_x, text_y)
                elif self.revealed[y][x]:
                    if self.board[y][x] == -1:
                        # 지뢰 표시
                        self.ctx.fillText("X", text_x, text_y)
                    elif self.board[y][x] > 0:
                        # 주변 지뢰 개수 표시
                        self.ctx.fillText(str(self.board[y][x]), text_x, text_y)

# 게임 시작
game = Minesweeper()