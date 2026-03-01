# PyAutoGrid Clicker 🖱️✨

一个基于 Python 和 PyQt5 开发的**高效屏幕坐标快速选择与点击工具**。通过全屏字符网格覆盖，让用户只需输入简短的字符组合（如 "A1", "Z9"），即可精准定位并自动点击屏幕任意位置。

> **核心理念**：拒绝鼠标长途跋涉，用键盘实现“瞬移”点击。

![License](https://img.shields.io/badge/license-MIT-blue.svg)
![Python](https://img.shields.io/badge/python-3.8%2B-green.svg)
![PyQt5](https://img.shields.io/badge/PyQt5-5.15%2B-orange.svg)

---

## 📸 功能特性 (Features)

- **⚡ 极速定位**：全屏覆盖字符网格，输入 2-3 个字符即可锁定目标区域。
- **🎯 自动点击**：匹配成功后自动执行鼠标点击操作，解放双手。
- **💻 系统托盘驻留**：程序最小化至系统托盘，随时待命，不占用任务栏空间。
- **⌨️ 快捷键呼出**：支持双击 `Caps Lock` 键快速显示/隐藏操作界面。
- **🎨 可视化反馈**：输入过程中实时高亮匹配的网格标签，操作直观清晰。
- **🛑 一键退出/重置**：支持 `Esc` 键快速重置输入或隐藏窗口。
- **🐼 可爱图标**：内置熊猫图标（需准备资源文件），让工具更具亲和力。

---

## 🚀 快速开始 (Quick Start)

### 1. 环境要求

- Python 3.8 或更高版本
- 操作系统：Windows / Linux / macOS (需适配部分系统特定库)

### 2. 安装依赖

克隆项目后，安装所需的 Python 库：

```bash
pip install pyautogui PyQt5 pynput
```

> **注意**：`pynput` 在某些 Linux 发行版上可能需要额外的系统依赖（如 `xorg-dev` 等）。

### 3. 资源准备

确保项目根目录下存在 `resource` 文件夹，并包含名为 `pandaFace.ico` 的图标文件。如果没有，可以自行替换为任意 `.ico` 或 `.png` 文件，并修改代码中的路径。

```text
project_root/
├── main.py
├── resource/
│   └── pandaFace.ico
└── README.md
```

### 4. 运行程序

```bash
python main.py
```

运行后，程序将最小化至系统托盘。**双击键盘上的 `Caps Lock` 键**即可唤出全屏网格界面。

---

## 🎮 使用指南 (Usage)

1. **启动程序**：运行脚本，程序在后台运行，托盘区可见图标。
2. **唤出界面**：快速双击 `Caps Lock` 键，全屏网格出现。
3. **输入坐标**：
   - 网格由字母（行）和数字/符号（列）组成。
   - 例如：目标在 "C" 行 "5" 列，依次按下 `C` 和 `5`。
   - 随着输入，匹配的标签会高亮显示（蓝色字体）。
4. **自动点击**：当输入完全匹配某个标签时，程序会自动获取该位置坐标并执行点击，随后界面自动隐藏。
5. **重置/退出**：
   - 按 `Esc` 键：清空当前输入，恢复初始状态。
   - 再次双击 `Caps Lock` 或点击托盘菜单 "Quit" 退出程序。

---

## ⚙️ 技术栈 (Tech Stack)

- **GUI 框架**: [PyQt5](https://www.riverbankcomputing.com/software/pyqt/)
- **自动化控制**: [PyAutoGUI](https://pyautogui.readthedocs.io/)
- **键盘监听**: [Pynput](https://pynput.readthedocs.io/)
- **多线程**: `QThread` (用于非阻塞键盘监听)

---

## 🔧 自定义配置 (Configuration)

你可以根据需求修改 `main.py` 中的以下参数：

- **网格大小**: 修改 `getCharacterRange(46)` 中的数字 `46` 来调整行列数量。
- **样式美化**: 调整 `initLables` 方法中的 `setStyleSheet` 来自定义标签颜色、字体和透明度。
- **触发按键**: 修改 `KeyboardListener` 类中的 `Key.caps_lock` 为其他按键（如 `Key.f1`）。
- **点击延迟**: 在 `pyautogui.click(x, y)` 前添加 `time.sleep()` 可增加点击前的延迟。

---

## ⚠️ 注意事项 (Known Issues & Notes)

- **权限问题**: 在 macOS 或某些 Linux 环境下，可能需要赋予终端/IDE “辅助功能”或“屏幕录制”权限才能控制鼠标。
- **分辨率适配**: 当前版本基于物理像素计算坐标，在高 DPI 屏幕上可能需要调整 `devicePixelRatio()` 的相关逻辑。
- **资源文件**: 请确保 `resource/pandaFace.ico` 存在，否则程序启动时会报错。
- **冲突风险**: 避免在游戏反作弊系统或其他安全软件运行时使用，以免被误判为外挂。

---

## 🤝 贡献 (Contributing)

欢迎提交 Issue 和 Pull Request！如果你有任何改进建议、Bug 修复或新功能想法，请随时参与。

1. Fork 本仓库
2. 创建你的特性分支 (`git checkout -b feature/AmazingFeature`)
3. 提交你的更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 开启一个 Pull Request

---

## 📄 许可证 (License)

本项目采用 MIT 许可证 - 查看 [LICENSE](LICENSE) 文件了解详情。

---

## 🙏 致谢 (Acknowledgements)

- 感谢 [PyAutoGUI](https://github.com/asweigart/pyautogui) 团队提供的强大自动化库。
- 感谢 [PyQt5](https://riverbankcomputing.com/software/pyqt/intro) 社区的支持。
- 图标资源来源于网络（或请在此处注明你的图标来源）。

---

<div style="text-align: center;">

**Made with ❤️ by [GHS]**

如果这个项目对你有帮助，请给一个 ⭐ Star！

</div>