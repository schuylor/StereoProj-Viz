import matplotlib
matplotlib.use("MacOSX")

import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D


# 1. 定义变换公式 (Inverse Stereographic)
def inverse_stereographic_transform(u, v):
    r2 = u ** 2 + v ** 2
    denominator = r2 + 1
    x = (2 * u) / denominator
    y = (2 * v) / denominator
    z = (r2 - 1) / denominator
    return x, y, z


def calculate_jacobian_determinant(u, v):
    # 论文公式 (4) 的简化版 (n=2 for Sphere S^2)
    # det G = (2 / (u^2 + v^2 + 1))^4
    # 这代表了体积/面积的变化率
    r2 = u ** 2 + v ** 2
    return (2 / (r2 + 1)) ** 2  # 注意：面积元变化通常是平方关系，具体取决于度量定义，这里展示趋势


# 2. 准备数据
# 稍微稀疏一点，方便点击，不然点太密很难选中
grid_range = np.linspace(-3, 3, 15)
u_grid, v_grid = np.meshgrid(grid_range, grid_range)

# 展平数组方便索引
u_flat = u_grid.flatten()
v_flat = v_grid.flatten()

# 计算对应的球面坐标
x_flat, y_flat, z_flat = inverse_stereographic_transform(u_flat, v_flat)

# 3. 设置绘图
fig = plt.figure(figsize=(12, 8))
ax = fig.add_subplot(111, projection='3d')
ax.set_title('Click on a RED point on the sphere!\n(Interactive Stereographic Projection)')

# 画出参考用的单位球网格（灰色线条）
phi, theta = np.mgrid[0.0:np.pi:20j, 0.0:2.0 * np.pi:20j]
x_s = np.sin(phi) * np.cos(theta)
y_s = np.sin(phi) * np.sin(theta)
z_s = np.cos(phi)
ax.plot_wireframe(x_s, y_s, z_s, color='gray', alpha=0.1)

# 画北极点
north_pole = np.array([0, 0, 1])
ax.scatter([0], [0], [1], c='black', marker='*', s=200, label='North Pole')

# 绘制平面点 (R^2) - 蓝色，半透明
# 我们把它们画在 z=0 平面上演示
scatter_plane = ax.scatter(u_flat, v_flat, np.zeros_like(u_flat),
                           c='blue', marker='x', alpha=0.3, label='Plane Points (R^2)')

# 绘制球面点 (S^2) - 红色，开启 picker
# picker=5 意味着点击点周围 5 像素内都算选中
scatter_sphere = ax.scatter(x_flat, y_flat, z_flat,
                            c='red', marker='o', s=60, picker=5, label='Sphere Points (Click Me!)')

# 用于存储当前画出的“光线”，方便下次点击时清除旧的
current_ray = []


# 4. 定义交互逻辑
def on_pick(event):
    # 如果点击的不是球面点，忽略
    if event.artist != scatter_sphere:
        return

    # 获取被点击点的索引 (index)
    ind = event.ind[0]

    # 提取坐标
    u_val, v_val = u_flat[ind], v_flat[ind]
    x_val, y_val, z_val = x_flat[ind], y_flat[ind], z_flat[ind]

    # 计算一些有趣的统计量（Paper Question 3 相关）
    stretch_factor = calculate_jacobian_determinant(u_val, v_val)

    print(f"\n--- Point Selected: Index {ind} ---")
    print(f"Plane Coord (u,v): ({u_val:.2f}, {v_val:.2f})")
    print(f"Sphere Coord (x,y,z): ({x_val:.2f}, {y_val:.2f}, {z_val:.2f})")
    print(f"Jacobian Factor (Density Correction): {stretch_factor:.4f}")
    if abs(u_val) < 0.5:
        print(">> Note: Near South Pole/Origin. Little distortion.")
    else:
        print(">> Note: Far from center. High distortion! (Notice the ray slope)")

    # 清除上一条线
    global current_ray
    for line in current_ray:
        line.remove()
    current_ray = []

    # 画新线： 北极 -> 球面点 -> 平面点
    # 验证三点共线
    line_x = [0, u_val]
    line_y = [0, v_val]
    line_z = [1, 0]  # 从 z=1 (北极) 到 z=0 (平面)

    # 绘制射线
    line, = ax.plot(line_x, line_y, line_z, 'g-', linewidth=2, label='Projection Ray')
    current_ray.append(line)

    # 额外高亮选中的平面点
    highlight, = ax.plot([u_val], [v_val], [0], 'yo', markersize=10, markeredgecolor='black')
    current_ray.append(highlight)

    # 刷新画布
    fig.canvas.draw_idle()


if __name__ == '__main__':
    fig.canvas.mpl_connect('pick_event', on_pick)

    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')
    ax.legend()

    plt.show()