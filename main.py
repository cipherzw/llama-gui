import sys
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QMenuBar, QStatusBar,
    QSplitter, QTabWidget, QWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QLineEdit, QPlainTextEdit, QPushButton, QFrame, QFileDialog
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

        # ---- 中栏：上下两部分布局 ----
        # 使用垂直布局将中间栏分为上下两部分
        center_widget = QWidget()
        center_layout = QVBoxLayout(center_widget)
        
        # --- 上半部分：导入文件路径和按钮 ---
        top_widget = QWidget()
        top_layout = QVBoxLayout(top_widget)
        top_layout.setContentsMargins(10, 10, 10, 10)
        
        # llama-server.exe 文件导入部分（新增行）
        server_row_layout = QHBoxLayout()
        server_row_layout.addWidget(QLabel("llama-server.exe:"))
        self.server_path_edit = QLineEdit()
        self.server_path_edit.setPlaceholderText("llama-server.exe")
        self.server_path_edit.setText("llama-server.exe")
        server_row_layout.addWidget(self.server_path_edit)
        self.server_import_btn = QPushButton("导入")
        self.server_import_btn.clicked.connect(self.import_server_file)
        server_row_layout.addWidget(self.server_import_btn)
        top_layout.addLayout(server_row_layout)
        
        # 模型文件导入部分（单行）
        model_row_layout = QHBoxLayout()
        model_row_layout.addWidget(QLabel("模型文件:"))
        self.model_path_edit = QLineEdit()
        self.model_path_edit.setPlaceholderText("D:/models/llama")
        model_row_layout.addWidget(self.model_path_edit)
        self.model_import_btn = QPushButton("导入")
        self.model_import_btn.clicked.connect(self.import_model_file)
        model_row_layout.addWidget(self.model_import_btn)
        top_layout.addLayout(model_row_layout)
        
        # 多模态文件导入部分（单行）
        multimodal_row_layout = QHBoxLayout()
        multimodal_row_layout.addWidget(QLabel("视觉文件:"))
        self.multimodal_path_edit = QLineEdit()
        self.multimodal_path_edit.setPlaceholderText("D:/multimodal")
        multimodal_row_layout.addWidget(self.multimodal_path_edit)
        self.multimodal_import_btn = QPushButton("导入")
        self.multimodal_import_btn.clicked.connect(self.import_multimodal_file)
        multimodal_row_layout.addWidget(self.multimodal_import_btn)
        top_layout.addLayout(multimodal_row_layout)
        
        center_layout.addWidget(top_widget)
        
        # --- 下半部分：参数设置标签页 ---
        self.tab_widget = QTabWidget()
        # 添加四个参数分类页（占位）
        self.add_parameter_tab("基础参数")
        self.add_parameter_tab("模型参数")
        self.add_parameter_tab("高级参数")
        self.add_parameter_tab("视觉模型")
        center_layout.addWidget(self.tab_widget)
        
        splitter.addWidget(center_widget)

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

        # 设置三栏初始宽度比例（左：中：右 = 2:3:2）
        splitter.setSizes([250, 450, 250])

        self.setCentralWidget(splitter)

    def import_server_file(self):
        """导入 llama-server.exe 文件路径"""
        path, _ = QFileDialog.getOpenFileName(
            self,
            "选择 llama-server.exe 文件",
            "",
            "可执行文件 (*.exe);;所有文件 (*.*)"
        )
        if path:
            self.server_path_edit.setText(path)

    def import_model_file(self):
        """导入模型文件路径"""
        path, _ = QFileDialog.getOpenFileName(
            self,
            "选择模型文件",
            "",
            "GGUF 模型文件 (*.gguf);;模型文件 (*.bin);;所有文件 (*.*)"
        )
        if path:
            self.model_path_edit.setText(path)

    def import_multimodal_file(self):
        """导入多模态文件路径"""
        path, _ = QFileDialog.getOpenFileName(
            self,
            "选择多模态文件",
            "",
            "GGUF 模型文件 (*.gguf);;模型文件 (*.bin);;所有文件 (*.*)"
        )
        if path:
            self.multimodal_path_edit.setText(path)

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
