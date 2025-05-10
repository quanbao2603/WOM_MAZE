# 🧭 WOM_MAZE: Mô phỏng Robot Tìm Đường bằng Python

Dự án này là một hệ thống mô phỏng trực quan quá trình robot tìm đường trong mê cung, ứng dụng các thuật toán cổ điển như BFS, DFS, Dijkstra và A*. Giao diện người dùng được phát triển bằng CustomTkinter nhằm mang lại trải nghiệm trực quan, dễ thao tác và thân thiện với người học.

---

## 🧠 Thuật toán hỗ trợ

- **BFS** (Breadth-First Search)
- **DFS** (Depth-First Search)
- **Dijkstra**
- **A\*** (A Star Search) – hỗ trợ nhiều loại heuristic:
  - Manhattan
  - Euclidean
  - Chebyshev
  - Octile
  - Tie-breaking

---

## 🧱 Các thành phần chính

| Tên tệp | Chức năng |
|--------|-----------|
| `WOM_MAZE_LOGIC.py` | Chứa toàn bộ thuật toán tìm đường và sinh mê cung |
| `WOM_MAZE-UI.py` | Giao diện mô phỏng cơ bản |
| `WOM_MAZE_COMPARE_UI.py` | Giao diện so sánh hai thuật toán chạy song song |
| `WOM_MAZE_ECOBOT_UI.py` | Mô phỏng môi trường có địa hình và nhiên liệu (EcoBot) |
| `WOM_MAZE_MUD_UI.py` | Mô phỏng mê cung động, tường có thể thay đổi trong quá trình tìm đường |

---

## 🖼️ Tính năng nổi bật

- Sinh mê cung bằng nhiều thuật toán: Recursive Backtracking, Prim, Kruskal, Eller
- Tùy chỉnh điểm bắt đầu/kết thúc, chọn thuật toán, tốc độ chạy
- Hiển thị trực quan từng bước thuật toán với hiệu ứng animation
- So sánh hiệu suất thuật toán: số ô đã duyệt, độ dài đường đi, thời gian
- Hỗ trợ mô phỏng môi trường thực tế:
  - **EcoBot:** địa hình tiêu hao năng lượng
  - **Mud Maze:** mê cung có thể thay đổi khi robot đang tìm đường

---

## 🚀 Cách chạy

### ⚙️ Cài đặt thư viện cần thiết
```bash
pip install customtkinter pillow
