# Import các thư viện cần thiết
import pygame
import sys
import random
import heapq  
# Import thêm thư viện pygame.image để làm việc với hình ảnh
import pygame.image

# Khởi tạo Pygame
pygame.init()

# Tạo font
font = pygame.font.SysFont('comicsansms', 14)

# Kích thước cửa sổ trò chơi
window_width, window_height = 800, 600
screen = pygame.display.set_mode((window_width, window_height))
pygame.display.set_caption("Trò chơi Mê cung")
screen.fill((128, 128, 128))  # Đặt màu nền của cửa sổ là màu xám

# Load ảnh từ tập tin
image_move = "D:\\maze\\img\\arrows.png"  # Đặt đường dẫn đúng đến tập tin ảnh của bạn
image = pygame.image.load(image_move)
image = pygame.transform.scale(image, (80, 80))  # Thay đổi kích thước ảnh

# Kích thước ô trong mê cung
cell_size = 30
maze_width, maze_height = 610, 600
rows = maze_height // cell_size
cols = maze_width // cell_size

# Load ảnh mới từ tập tin
image_space = "D:\\maze\\img\\space.png"  # Thay đổi đường dẫn đến ảnh mới
image2 = pygame.image.load(image_space)
image2 = pygame.transform.scale(image2, (85, 40))

# Cài đặt đồng hồ để kiểm soát tốc độ khung hình
clock = pygame.time.Clock()

# Định nghĩa màu sắc
black = (0, 0, 0)
white = (255, 255, 255)
red = (255, 0, 0)
green = (0, 255, 0)

# Định nghĩa kích thước của ô trong mê cung
cell_size = 30

# Hàm tạo mê cung
def create_maze():
    maze = [[1 for _ in range(cols)] for _ in range(rows)]

    # Hàm đệ quy để tạo đường đi trong mê cung
    def create_path(x, y):
        directions = [(0, 2), (2, 0), (0, -2), (-2, 0)]
        random.shuffle(directions)
        for dx, dy in directions:
            nx, ny = x + dx, y + dy
            if 0 <= nx < rows and 0 <= ny < cols and maze[nx][ny] == 1:
                maze[x + dx // 2][y + dy // 2] = 0
                maze[nx][ny] = 0
                create_path(nx, ny)

    # Bắt đầu tạo đường đi từ góc trên bên trái
    create_path(0, 0)

    # Đặt điểm đích
    maze[rows - 2][cols - 1] = 0

    return maze

# Tạo mê cung
maze = create_maze()

# Vị trí ban đầu của người chơi và điểm đích
player_pos = [0, 0]
goal_pos = [rows - 2, cols - 1] 

# Cờ chỉ định xem chế độ tự động có được kích hoạt không
auto_mode = False

# Hàm vẽ thông báo lên màn hình
def draw_message(message):
    font = pygame.font.SysFont('comicsansms', 48)  # Sử dụng font 'comicsansms' với kích thước 48
    text = font.render(message, True, (255, 255, 255), (128, 128, 128))  # Chữ trắng, nền màu xám
    text_rect = text.get_rect(center=(window_width // 2, window_height // 2))  # Căn giữa văn bản trên màn hình
    screen.fill((128, 128, 128))  # Đổ màu xám lên toàn bộ màn hình
    screen.blit(text, text_rect)
    pygame.display.flip()
    pygame.time.delay(2000)  # Chờ 2 giây trước khi khởi động lại trò chơi

# Hàm để tính khoảng cách (heuristic cho A*)
def heuristic(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])

# Hàm thực hiện thuật toán A* để tìm đường
def astar(maze, start, end):
    # open_set chứa các nút có thể xem xét tiếp theo và được sắp xếp theo f_score
    open_set = []
    # closed_set chứa các nút đã được xem xét
    closed_set = set()
    # Đưa điểm xuất phát vào open_set với f_score là 0
    heapq.heappush(open_set, (0, start))
    # came_from lưu trữ đỉnh trước đỉnh hiện tại trong đường đi tốt nhất từ điểm xuất phát đến đỉnh hiện tại
    came_from = {}

    # g_score là chi phí tốt nhất để đi từ điểm xuất phát đến mỗi điểm
    g_score = {start: 0}
    # f_score là tổng chi phí ước lượng từ điểm xuất phát đến mỗi điểm thông qua đỉnh hiện tại
    f_score = {start: heuristic(start, end)}

    while open_set:
        # Lấy điểm hiện tại có f_score thấp nhất từ open_set
        current = heapq.heappop(open_set)[1]

        # Nếu đến được điểm đích, xây dựng đường đi và trả về
        if current == end:
            path = []
            while current in came_from:
                path.append(current)
                current = came_from[current]
            return path[::-1]

        # Đưa điểm hiện tại vào closed_set vì đã xem xét
        closed_set.add(current)

        # Duyệt qua các hướng xung quanh (lên, xuống, trái, phải)
        for i, j in [(0, -1), (0, 1), (-1, 0), (1, 0)]:
            # Tính toán tọa độ của điểm kế tiếp
            neighbor = current[0] + i, current[1] + j

            # Kiểm tra xem điểm kế tiếp có nằm trong biên và không phải là điểm cản trở
            if 0 <= neighbor[0] < rows and 0 <= neighbor[1] < cols and maze[neighbor[0]][neighbor[1]] == 0:
                # Tính toán chi phí tạm thời để đi từ điểm xuất phát đến điểm kế tiếp
                tentative_g_score = g_score[current] + 1

                # Nếu điểm kế tiếp chưa được xem xét hoặc chi phí tạm thời nhỏ hơn chi phí đã biết
                if neighbor not in closed_set or tentative_g_score < g_score.get(neighbor, 0):
                    # Cập nhật thông tin cho điểm kế tiếp
                    came_from[neighbor] = current
                    g_score[neighbor] = tentative_g_score
                    f_score[neighbor] = tentative_g_score + heuristic(neighbor, end)
                    # Đưa điểm kế tiếp vào open_set để xem xét trong các bước tiếp theo
                    heapq.heappush(open_set, (f_score[neighbor], neighbor))

    # Nếu không tìm thấy đường đi, trả về danh sách rỗng
    return []


# Hàm tạo nút mới
def create_button(x, y, width, height, color, text, action=None):
    font = pygame.font.SysFont('comicsansms', 14)
    text_surface = font.render(text, True, black)
    text_rect = text_surface.get_rect(center=(x + width // 2, y + height // 2))

    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()

    button_color = color
    border_color = (0, 0, 0)

    if x < mouse[0] < x + width and y < mouse[1] < y + height:
        button_color = (200, 200, 200)  # Màu nền khi hover
        border_color = (255, 255, 255)  # Màu viền khi hover

        if click[0] == 1 and action is not None:
            action()

    pygame.draw.rect(screen, button_color, (x, y, width, height))
    pygame.draw.rect(screen, border_color, (x, y, width, height), 2)  # Viền nút
    screen.blit(text_surface, text_rect)

# Hàm thay đổi mê cung ngẫu nhiên
def change_maze():
    global maze, player_pos
    maze = create_maze()
    player_pos = [0, 0]

# Vòng lặp chính của trò chơi
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and not auto_mode and player_pos[0] > 0 and maze[player_pos[0] - 1][player_pos[1]] == 0:
                player_pos[0] -= 1
            elif event.key == pygame.K_DOWN and not auto_mode and player_pos[0] < rows - 1 and maze[player_pos[0] + 1][player_pos[1]] == 0:
                player_pos[0] += 1
            elif event.key == pygame.K_LEFT and not auto_mode and player_pos[1] > 0 and maze[player_pos[0]][player_pos[1] - 1] == 0:
                player_pos[1] -= 1
            elif event.key == pygame.K_RIGHT and not auto_mode and player_pos[1] < cols - 1 and maze[player_pos[0]][player_pos[1] + 1] == 0:
                player_pos[1] += 1
            elif event.key == pygame.K_SPACE:
                # Chuyển đổi chế độ tự động
                auto_mode = not auto_mode
            elif event.type == pygame.MOUSEBUTTONDOWN:
                # Kiểm tra xem người chơi đã nhấp vào nút chưa
                if 150 < event.pos[0] < 250 and 10 < event.pos[1] < 40:
                    change_maze()

    # Vẽ nút thay đổi mê cung
    create_button(window_width - 160, 10, 100, 30, (255, 255, 255), "Change Maze", action=change_maze)

    # Vẽ ảnh lên màn hình
    screen.blit(image, (window_width - 150, 50))  # Đặt vị trí của ảnh

    # Vẽ văn bản dưới ảnh
    text_surface = font.render("Move", True, (255, 255, 255))
    text_rect = text_surface.get_rect(center=(window_width - 110, 130))
    screen.blit(text_surface, text_rect)

    # Vẽ ảnh 2
    screen.blit(image2, (window_width - 150, 150))

    # Vẽ văn bản dưới ảnh 2
    text_surface2 = font.render("On/Off Auto", True, (255, 255, 255))  # Thay đổi nội dung văn bản
    text_rect2 = text_surface2.get_rect(center=(window_width - 110, 210))
    screen.blit(text_surface2, text_rect2)

    # Logic tự động sử dụng thuật toán A*
    if auto_mode and player_pos != goal_pos:
        path = astar(maze, tuple(player_pos), tuple(goal_pos))
        if path:
            player_pos = list(path[0])

    # Kiểm tra xem người chơi đã đến đích hay chưa
    if player_pos == goal_pos:
        draw_message("Goal!!!Restarting...")
        auto_mode = not auto_mode
        # Khởi tạo lại mê cung và vị trí người chơi
        maze = create_maze()
        player_pos = [0, 0]

    # Vẽ mê cung
    for row in range(rows):
        for col in range(cols):
            color = white if maze[row][col] == 0 else black
            pygame.draw.rect(screen, color, (col * cell_size, row * cell_size, cell_size, cell_size))

    # Vẽ người chơi
    pygame.draw.rect(screen, red, (player_pos[1] * cell_size, player_pos[0] * cell_size, cell_size, cell_size))

    # Vẽ điểm đích
    pygame.draw.rect(screen, green, (goal_pos[1] * cell_size, goal_pos[0] * cell_size, cell_size, cell_size))

    # Cập nhật màn hình
    pygame.display.flip()

    # Giữ tốc độ khung hình ở mức 10 khung hình mỗi giây
    clock.tick(10)
