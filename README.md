# 🎮 PyScript로 지뢰찾기 게임 만들기

## 📚 학습 목표
- Canvas를 이용한 그래픽 프로그래밍
- 2차원 배열을 활용한 게임판 구현
- 마우스 이벤트 처리
- DFS(깊이 우선 탐색)를 이용한 자동 확장 기능

---

## 🚀 1. HTML 파일 만들기

### index.html
```html
<!DOCTYPE html>
<html>
    <head>
        <script type="module" src="https://pyscript.net/releases/2025.3.1/core.js"></script>
    </head>
    <body>
        <canvas id="game"></canvas>
        <py-script src="game.py"></py-script>
    </body>
</html>
```

### 📖 PyScript란?
PyScript는 웹 브라우저에서 Python 코드를 실행할 수 있게 해주는 기술임
- HTML 파일 안에 `<py-script>` 태그를 사용
- Python 파일을 `src` 속성으로 연결
- 브라우저가 Python 코드를 JavaScript로 변환하여 실행

---

## 🎨 2. Canvas 이해하기

### Canvas란?
Canvas는 웹 페이지에서 그림을 그릴 수 있는 HTML 요소임

### 좌표 시스템
Canvas의 좌표는 **왼쪽 위가 (0, 0)**

```
(0,0) ────────→ X축 (오른쪽으로 갈수록 증가)
  │
  │   예시: 
  │   • (50, 30) = 오른쪽으로 50px, 아래로 30px
  │   • (100, 100) = 오른쪽으로 100px, 아래로 100px
  │
  ↓
 Y축 (아래로 갈수록 증가)
```

### 📖 js 모듈

```python
from js import document
```
- `from js`: PyScript에서 제공하는 JavaScript 모듈에서
- `import document`: document 객체를 가져오기
- `document`는 웹 페이지의 HTML 요소들을 제어할 수 있는 객체

### 예제 코드
```python
from js import document

# Canvas 가져오기
canvas = document.getElementById("game")
ctx = canvas.getContext("2d")

# Canvas 크기 설정
canvas.width = 200
canvas.height = 200

# 배경 사각형 그리기
ctx.fillStyle = "#cccccc"  # 회색
ctx.fillRect(0, 0, 200, 200)  # (x, y, 너비, 높이)
```

### 📖 Canvas 코드 설명
- `document.getElementById("game")`: HTML에서 id가 "game"인 요소를 가져오기
- `canvas.getContext("2d")`: 2D 그리기 도구를 가져오기
- `canvas.fillStyle`: 채우기 색상을 설정
- `canvas.fillRect(x, y, width, height)`: 색이 채워진 직사각형을 그리기

---

## 🏗️ 3. 기본 클래스 구조 만들기

### 클래스 설계 (game.py)
```python
import random
from js import document, window
from pyodide.ffi import create_proxy

class Minesweeper:
    def __init__(self):
        # 게임 설정
        self.SIZE = 8          # 8×8 게임판
        self.MINES = 10        # 지뢰 10개
        self.CELL_SIZE = 25    # 각 칸의 크기
        
        # 색상 상수
        self.COLOR_BACKGROUND = "#f0f0f0"    # 전체 배경색
        self.COLOR_MINE = "#ff4444"          # 지뢰 칸 색상 (빨간색)
        self.COLOR_REVEALED = "#ffffff"       # 열린 칸 색상 (흰색)
        self.COLOR_HIDDEN = "#cccccc"         # 닫힌 칸 색상 (회색)
        self.COLOR_BORDER = "#999999"         # 테두리 색상
        self.COLOR_TEXT = "#000000"           # 텍스트 색상 (검정색)
        
        # Canvas 설정
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
```

### 📖 모듈 상세 설명

**1. random 모듈**
```python
import random
```
- Python 기본 제공 모듈
- 랜덤한 숫자를 생성하는 기능 제공
- 지뢰를 무작위 위치에 배치할 때 사용

**2. js 모듈에서 가져오기**
```python
from js import document, window
```
- `document`: HTML 문서의 요소들을 제어
- `window`: 브라우저 창 객체

**3. PyScript 전용 모듈**
```python
from pyodide.ffi import create_proxy
```
- `pyodide.ffi`: PyScript의 Python-JavaScript 연결 모듈
- `create_proxy`: Python 함수를 JavaScript에서 사용할 수 있게 변환
- 마우스 클릭 이벤트를 Python 함수와 연결할 때 필수

**import 방식의 차이:**
```python
# 방식 1: 모듈 전체 가져오기
import random
random.randint(0, 10)  # 모듈명.함수명

# 방식 2: 특정 객체만 가져오기
from js import document
document.getElementById("game")  # 바로 사용
```

### 📖 주요 개념 설명

**클래스와 생성자**
- `class Minesweeper`: 게임 전체를 관리하는 클래스
- `__init__`: 객체가 생성될 때 자동으로 실행되는 초기화 함수
- `self`: 클래스 내에서 자기 자신을 가리키는 변수

**색상 코드 이해**
색상은 16진수 코드로 표현됨 (#RRGGBB):
- RR: 빨간색 강도 (00~FF)
- GG: 초록색 강도 (00~FF)  
- BB: 파란색 강도 (00~FF)

예시:
- `#ff0000`: 빨간색 (R=255, G=0, B=0)
- `#00ff00`: 초록색 (R=0, G=255, B=0)
- `#cccccc`: 회색 (R=204, G=204, B=204)

**Canvas 크기 계산**
```
전체 Canvas 크기 = SIZE × CELL_SIZE
                 = 8칸 × 25픽셀
                 = 200픽셀
```

**create_proxy가 필요한 이유**
Python과 JavaScript는 서로 다른 언어임. 브라우저의 이벤트(클릭 등)는 JavaScript로 처리되는데, 우리는 Python 함수로 처리하고 싶기 때문에 `create_proxy`가 이 둘을 연결해주는 다리 역할을 함.

```python
# create_proxy 없이 (작동 안 함)
canvas.addEventListener("click", self.handle_click)  # ❌

# create_proxy 사용 (정상 작동)
canvas.addEventListener("click", create_proxy(self.handle_click))  # ✅
```

---

## 🎲 4. 게임판 초기화

### 2차원 배열 이해하기
게임판은 2차원 배열(리스트 안의 리스트)로 표현함

```
board[y][x] 형식으로 접근 (y가 행, x가 열)

     x: 0   1   2   3   4   5   6   7
y: 0   [0] [0] [0] [0] [0] [0] [0] [0]
   1   [0] [0] [0] [0] [0] [0] [0] [0]
   2   [0] [0] [0] [0] [0] [0] [0] [0]
   3   [0] [0] [0] [0] [0] [0] [0] [0]
   4   [0] [0] [0] [0] [0] [0] [0] [0]
   5   [0] [0] [0] [0] [0] [0] [0] [0]
   6   [0] [0] [0] [0] [0] [0] [0] [0]
   7   [0] [0] [0] [0] [0] [0] [0] [0]

예: board[2][3] = 2행 3열의 값
```

### 게임 초기화 함수
```python
def start_new_game(self):
    # 게임판 초기화 (0으로 채워진 8×8 배열)
    self.board = [[0 for _ in range(self.SIZE)] for _ in range(self.SIZE)]
    
    # 열린 칸 표시 (모두 False로 시작)
    self.revealed = [[False for _ in range(self.SIZE)] for _ in range(self.SIZE)]
    
    # 깃발 표시 (모두 False로 시작)
    self.flagged = [[False for _ in range(self.SIZE)] for _ in range(self.SIZE)]
    
    # 게임 상태
    self.game_over = False
    self.game_won = False
    self.revealed_count = 0
    
    # 지뢰 배치
    self.place_mines()
    # 숫자 계산
    self.calculate_numbers()
```

### 📖 리스트 컴프리헨션문
```python
# 일반적인 방법
n = []
for _ in range(5):
    n.append(0)
# n = [0, 1, 2, 3, 4]

#컴프리헨션문 사용
n = [0 for _ in range(5)]
# n = [0, 1, 2, 3, 4]
```
파이썬 리스트 컴프리헨션문은 위와 같이 사용 가능함

아래는 2차원 배열 초기화 방법
```python
# 일반적인 방법
board = []
for y in range(8):
    row = []
    for x in range(8):
        row.append(0)
    board.append(row)

# 리스트 컴프리헨션 (같은 결과, 더 간결)
board = [[0 for x in range(8)] for y in range(8)]
```

### 세 가지 배열의 역할
1. **board**: 각 칸의 내용
   - -1: 지뢰
   - 0: 빈 칸 (주변에 지뢰 없음)
   - 1~8: 주변 지뢰 개수
   
2. **revealed**: 각 칸이 열렸는지 여부
   - True: 열린 칸
   - False: 닫힌 칸
   
3. **flagged**: 각 칸에 깃발이 있는지 여부
   - True: 깃발 있음
   - False: 깃발 없음

---

## 💣 5. 지뢰 배치하기

### 랜덤 함수 이해하기
```python
import random

# random.randint(a, b): a부터 b까지의 정수 중 하나를 랜덤하게 선택
x = random.randint(0, 7)  # 0, 1, 2, 3, 4, 5, 6, 7 중 하나
```

### 지뢰 배치 함수
```python
def place_mines(self):
    """랜덤하게 지뢰 배치"""
    mines_placed = 0
    
    while mines_placed < self.MINES:
        # 랜덤한 좌표 생성
        x = random.randint(0, self.SIZE-1)
        y = random.randint(0, self.SIZE-1)
        
        # 이미 지뢰가 있는 곳이 아니면 지뢰 배치
        if self.board[y][x] != -1:  # -1은 지뢰를 의미
            self.board[y][x] = -1
            mines_placed += 1
```

### 📖 알고리즘 설명
1. `mines_placed = 0`: 현재까지 배치한 지뢰 개수
2. `while mines_placed < self.MINES`: 10개를 모두 배치할 때까지 반복
3. 랜덤한 좌표 (x, y) 선택
4. 그 위치에 지뢰가 없으면 지뢰 배치
5. 이미 지뢰가 있으면 다시 다른 좌표 선택

**예시 진행 과정:**
```
1번째: (3,5)에 지뢰 배치 → mines_placed = 1
2번째: (1,2)에 지뢰 배치 → mines_placed = 2
3번째: (3,5) 선택됨 → 이미 지뢰 있음, 다시 선택
4번째: (7,1)에 지뢰 배치 → mines_placed = 3
... 10개가 될 때까지 반복
```

---

## 🔢 6. 주변 지뢰 개수 계산

### 주변 8칸 확인하기
각 칸 주변의 8개 칸을 확인해야 함

```
현재 칸을 중심으로 주변 8칸의 상대 좌표:

[-1,-1] [-1,0] [-1,1]
[ 0,-1] [중심] [ 0,1]
[ 1,-1] [ 1,0] [ 1,1]

예시: 중심이 (3,3)일 때
(2,2) (2,3) (2,4)
(3,2) (3,3) (3,4)
(4,2) (4,3) (4,4)
```

### 숫자 계산 함수
```python
def calculate_numbers(self):
    """각 칸의 주변 지뢰 개수 계산"""
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
```

### 📖 중첩 반복문 이해하기
```python
# dy, dx의 모든 조합 (9가지):
dy=-1, dx=-1 → 왼쪽 위
dy=-1, dx=0  → 위
dy=-1, dx=1  → 오른쪽 위
dy=0,  dx=-1 → 왼쪽
dy=0,  dx=0  → 중심 (continue로 건너뜀)
dy=0,  dx=1  → 오른쪽
dy=1,  dx=-1 → 왼쪽 아래
dy=1,  dx=0  → 아래
dy=1,  dx=1  → 오른쪽 아래
```

### 경계 검사의 중요성
```python
if 0 <= ny < self.SIZE and 0 <= nx < self.SIZE:
```

이 조건은 좌표가 게임판을 벗어나지 않는지 확인함
- `0 <= ny`: Y좌표가 0 이상 (위쪽 경계)
- `ny < self.SIZE`: Y좌표가 8 미만 (아래쪽 경계)
- `0 <= nx`: X좌표가 0 이상 (왼쪽 경계)
- `nx < self.SIZE`: X좌표가 8 미만 (오른쪽 경계)

**경계 검사가 없으면:**
```
(0,0)의 주변을 확인할 때
(-1,-1) → 게임판 밖! (오류 발생)
(-1,0)  → 게임판 밖! (오류 발생)
...
```

---

## 🖼️ 7. 게임판 그리기

### 전체 게임판 그리기
```python
def draw_board(self):
    # 전체 배경 그리기
    self.ctx.fillStyle = self.COLOR_BACKGROUND
    self.ctx.fillRect(0, 0, self.SIZE * self.CELL_SIZE, self.SIZE * self.CELL_SIZE)
    
    # 각 칸 그리기
    for y in range(self.SIZE):
        for x in range(self.SIZE):
            self.draw_cell(x, y)
```

### 개별 칸 그리기
```python
def draw_cell(self, x, y):
    # 화면상 픽셀 좌표 계산
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
    
    # 텍스트 위치 (칸의 중앙)
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
```

### 📖 좌표 변환 이해하기
게임판 좌표를 화면 픽셀 좌표로 변환:

```
게임판 좌표 (3, 2) → 화면 좌표:
screen_x = 3 × 25 = 75px
screen_y = 2 × 25 = 50px

즉, Canvas의 왼쪽에서 75픽셀, 위에서 50픽셀 위치
```

**텍스트 중앙 정렬:**
- `textAlign = "center"`: 텍스트를 가로 중앙 정렬
- `text_x = screen_x + CELL_SIZE // 2`: 칸의 가로 중앙
- `text_y = screen_y + CELL_SIZE // 2 + 4`: 칸의 세로 중앙 (약간 아래로)

---

## 🖱️ 8. 마우스 클릭 처리

### 마우스 좌표를 게임판 좌표로 변환
```python
def get_cell_position(self, event):
    # 마우스 클릭 위치를 게임판 좌표로 변환
    rect = self.canvas.getBoundingClientRect()
    x = int((event.clientX - rect.left) / self.CELL_SIZE)
    y = int((event.clientY - rect.top) / self.CELL_SIZE)
    
    # 게임판 범위 내인지 확인
    if 0 <= x < self.SIZE and 0 <= y < self.SIZE:
        return (x, y)
    return (None, None)
```

### 📖 좌표 변환 과정 상세 설명

1. **마우스 좌표 얻기**
   - `event.clientX`: 화면 전체에서의 마우스 X좌표
   - `event.clientY`: 화면 전체에서의 마우스 Y좌표

2. **Canvas 위치 얻기**
   - `getBoundingClientRect()`: Canvas의 화면상 위치와 크기
   - `rect.left`: Canvas의 왼쪽 경계
   - `rect.top`: Canvas의 위쪽 경계

3. **상대 좌표 계산**
   ```
   Canvas 내부 좌표 = 마우스 좌표 - Canvas 시작 좌표
   ```

4. **게임판 좌표로 변환**
   ```
   게임판 좌표 = Canvas 내부 좌표 ÷ 칸 크기
   ```

**예시:**
```
마우스 클릭: 화면상 (285, 160)
Canvas 위치: (200, 100)
Canvas 내부: (285-200, 160-100) = (85, 60)
칸 크기: 25
게임판 좌표: (85÷25, 60÷25) = (3, 2)
```

### 좌클릭 처리
```python
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
        
        # 승리 조건 확인
        if self.revealed_count == self.SIZE * self.SIZE - self.MINES:
            self.game_won = True
            window.alert("Victory!")
    
    self.draw_board()
```

### 우클릭 처리 (깃발)
```python
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
```

### 📖 preventDefault()의 역할
브라우저에서 우클릭하면 기본적으로 컨텍스트 메뉴가 나타남
`preventDefault()`는 이런 기본 동작을 막아줌

**not 연산자로 토글하기:**
```python
# 깃발 토글 예시
flagged = False
flagged = not flagged  # True가 됨
flagged = not flagged  # 다시 False가 됨
```

---

## ✨ 9단계: 빈 칸 자동 확장 (재귀 함수와 DFS)

### 재귀 함수란?
재귀 함수는 자기 자신을 호출하는 함수

**간단한 예시: 카운트다운**
```python
def countdown(n):
    print(n)
    if n > 0:
        countdown(n - 1)  # 자기 자신을 호출 (재귀 호츌)
    else:
        print("히히 오줌 발싸!")

countdown(5)
```
**출력결과**
```
5
4
3
2
1
히히 오줌 발싸!
```

### DFS(깊이 우선 탐색)란?
DFS(Depth-First Search)는 한 방향으로 끝까지 탐색한 후 돌아와서 다른 방향을 탐색하는 알고리즘임

**일상생활 예시: 미로 찾기**
```
미로에서 출구를 찾을 때:
1. 갈림길에서 한 방향 선택
2. 막다른 길이 나올 때까지 계속 직진
3. 막히면 되돌아와서 다른 길 선택
4. 모든 길을 탐색할 때까지 반복
```

### DFS vs BFS 비교
```
DFS (깊이 우선):          BFS (너비 우선):
    1                        1
   / \                      / \
  2   5                    2   3
 / \                      / \
3   4                    4   5

탐색 순서: 1→2→3→4→5     탐색 순서: 1→2→3→4→5
(한 가지를 끝까지)        (층별로 탐색)
```

### 지뢰찾기에서의 DFS 시각화
```
게임판 상태 (0은 빈 칸, 숫자는 주변 지뢰 개수):
[1][1][0][0]
[1][X][1][0]
[1][1][1][0]
[0][0][0][0]

(2,0) 클릭 시 DFS 진행 과정:
1단계: (2,0) 열기 → 빈 칸이므로 주변 탐색
2단계: (1,0) 확인 → 숫자 1이므로 열기만
3단계: (3,0) 확인 → 빈 칸이므로 재귀 호출
4단계: (3,0)의 주변 탐색...
...이런 식으로 연쇄적으로 확장
```

### DFS 구현 코드
```python
def reveal_cell(self, x, y):
    """
    DFS(깊이 우선 탐색) 알고리즘을 사용하여 칸을 여는 함수
    빈 칸(0)을 클릭하면 재귀적으로 주변 칸들을 모두 연다
    """
    # 종료 조건 1: 이미 열린 칸
    if self.revealed[y][x]:
        return
    
    # 종료 조건 2: 깃발이 있는 칸
    if self.flagged[y][x]:
        return
    
    # 현재 칸 열기
    self.revealed[y][x] = True
    self.revealed_count += 1
    
    # 빈 칸(0)이면 주변 8칸 탐색 (DFS의 핵심)
    if self.board[y][x] == 0:
        # 주변 8방향
        for dy in [-1, 0, 1]:
            for dx in [-1, 0, 1]:
                if dy == 0 and dx == 0:
                    continue  # 자기 자신 제외
                
                nx, ny = x + dx, y + dy
                
                # 경계 확인
                if 0 <= nx < self.SIZE and 0 <= ny < self.SIZE:
                    # 재귀 호출 (DFS의 "깊이" 부분)
                    self.reveal_cell(nx, ny)
```

### 📖 DFS 동작 과정 상세 분석
```
예시: (2, 2) 클릭 (빈 칸)

호출 스택:
1. reveal_cell(2, 2) 시작
   - (2,2) 열기
   - 빈 칸이므로 주변 탐색
   
2. reveal_cell(1, 1) 호출
   - (1,1) 열기
   - 숫자이므로 종료
   
3. reveal_cell(1, 2) 호출
   - (1,2) 열기
   - 빈 칸이므로 또 주변 탐색
   
4. reveal_cell(0, 1) 호출
   - (0,1) 열기
   - 숫자이므로 종료
   
... 이런 식으로 계속
```

### DFS의 장점과 특징
1. **메모리 효율적**: 현재 경로만 기억
2. **구현이 간단**: 재귀로 쉽게 구현
3. **깊이 제한 없음**: 연결된 모든 빈 칸 탐색

### 종료 조건의 중요성
재귀 함수에서 종료 조건이 없으면 무한 루프에 빠짐
```python
# 잘못된 예시 (무한 루프)
def bad_reveal(x, y):
    self.revealed[y][x] = True
    # 종료 조건 없이 계속 호출
    for dy in [-1, 0, 1]:
        for dx in [-1, 0, 1]:
            bad_reveal(x+dx, y+dy)  # 영원히 반복!

# 올바른 예시 (종료 조건 있음)
def good_reveal(x, y):
    if self.revealed[y][x]:  # 종료 조건
        return
    self.revealed[y][x] = True
    # ... 나머지 코드
```

---

## 🎮 10. 전체 코드 완성

### 최종 코드
```python
import random
from js import document, window
from pyodide.ffi import create_proxy

class Minesweeper:
    def __init__(self):
        # 게임 설정
        self.SIZE = 8          # 게임판 크기 (8x8)
        self.MINES = 10        # 지뢰 개수
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
                window.alert("Victory!")
        
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
```

---

## 🚀 확장 아이디어

### 1. 난이도 조절
```python
# 초급
self.SIZE = 8
self.MINES = 10

# 중급
self.SIZE = 16
self.MINES = 40

# 고급
self.SIZE = 24
self.MINES = 99
```

### 2. 색상 테마 변경
```python
# 다크 모드
self.COLOR_BACKGROUND = "#2b2b2b"
self.COLOR_HIDDEN = "#444444"
self.COLOR_REVEALED = "#666666"

# 파스텔 톤
self.COLOR_MINE = "#ffb3ba"
self.COLOR_HIDDEN = "#bae1ff"
```

### 3. 이모지 사용
```python
# 텍스트 대신 이모지
self.ctx.font = "16px Arial"  # 크기 조정
self.ctx.fillText("💣", text_x, text_y)  # 지뢰
self.ctx.fillText("🚩", text_x, text_y)  # 깃발
```

### 4. 숫자별 색상
```python
# 숫자별로 다른 색상 적용
number_colors = {
    1: "#0000ff",  # 파란색
    2: "#008000",  # 초록색
    3: "#ff0000",  # 빨간색
    4: "#000080",  # 남색
    5: "#800000",  # 갈색
    6: "#008080",  # 청록색
    7: "#000000",  # 검정색
    8: "#808080"   # 회색
}

if self.board[y][x] > 0:
    self.ctx.fillStyle = number_colors.get(self.board[y][x], "#000000")
```

---

## 📝 학습 정리

### 배운 개념들

1. **Canvas API**
   - 웹에서 그래픽을 그리는 방법
   - 좌표 시스템과 도형 그리기
   - 텍스트 렌더링

2. **2차원 배열**
   - 게임판 데이터 구조
   - 인덱스를 통한 접근
   - 리스트 컴프리헨션

3. **이벤트 처리**
   - 마우스 클릭 이벤트
   - 좌표 변환 (화면 → 게임판)
   - preventDefault()

4. **알고리즘**
   - 랜덤 배치 알고리즘
   - 주변 탐색 알고리즘
   - DFS(깊이 우선 탐색)

5. **재귀 함수**
   - 자기 호출의 개념
   - 종료 조건의 중요성
   - 실제 활용 사례

### 프로그래밍 사고력
- 문제를 작은 단위로 나누기
- 데이터 구조 설계하기
- 알고리즘을 코드로 구현하기
- 사용자 인터페이스 만들기