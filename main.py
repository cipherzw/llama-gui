import sys
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QMenuBar, QStatusBar,
    QSplitter, QTabWidget, QWidget, QVBoxLayout, QLabel,
    QPlainTextEdit, QPushButton, QFrame
)
from PySide6.QtCore import Qt

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("LLaMA GUI")
        self.resize(1200, 700)  # 加宽以容纳三栏

        # ---------- 菜单栏 ----------
        menubar = self.menuBar()
        file_menu = menubar.addMenu("文件")
        help_menu = menubar.addMenu("帮助")

        # ---------- 状态栏 ----------
        self.statusBar().showMessage("就绪")

        # ---------- 中央区域：三栏布局 ----------
        splitter = QSplitter(Qt.Horizontal)

        # ---- 左栏：参数预览 ----
        self.preview_edit = QPlainTextEdit()
        self.preview_edit.setReadOnly(True)
        self.preview_edit.setPlaceholderText("参数预览将在此显示...")
        # 等宽字体便于阅读
        self.preview_edit.setStyleSheet("font-family: Consolas, monospace;")
        splitter.addWidget(self.preview_edit)

        # ---- 中栏：参数设置标签页 ----
        self.tab_widget = QTabWidget()
        # 添加四个参数分类页（占位）
        self.add_parameter_tab("基础参数")
        self.add_parameter_tab("模型参数")
        self.add_parameter_tab("高级参数")
        self.add_parameter_tab("视觉模型")
        splitter.addWidget(self.tab_widget)

        # ---- 右栏：启动与监控 ----
        right_widget = QWidget()
        right_layout = QVBoxLayout(right_widget)
        right_layout.setContentsMargins(5, 5, 5, 5)

        self.launch_btn = QPushButton("启动 llama-server")
        right_layout.addWidget(self.launch_btn)

        # 资源监控占位区（后续替换为图表）
        self.monitor_placeholder = QFrame()
        self.monitor_placeholder.setFrameStyle(QFrame.StyledPanel)
        self.monitor_placeholder.setMinimumHeight(200)
        monitor_label = QLabel("CPU/GPU 实时监控（开发中）")
        monitor_label.setAlignment(Qt.AlignCenter)
        monitor_placeholder_layout = QVBoxLayout(self.monitor_placeholder)
        monitor_placeholder_layout.addWidget(monitor_label)
        right_layout.addWidget(self.monitor_placeholder)

        right_layout.addStretch()  # 将控件推到顶部
        splitter.addWidget(right_widget)

        # 设置三栏初始宽度比例（左:中:右 = 2:3:2）
        splitter.setSizes([250, 450, 250])

        self.setCentralWidget(splitter)

    def add_parameter_tab(self, title: str):
        """添加一个参数分类页面"""
        page = QWidget()
        layout = QVBoxLayout(page)
        layout.addWidget(QLabel(f"这里将放置 {title} 相关设置"))
        self.tab_widget.addTab(page, title)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())