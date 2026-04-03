from PyQt6.QtWidgets import QMenu, QApplication
from PyQt6.QtGui import QAction
import sys
import os
import time

# 导入功能模块
# 为了方便导入，可以在这里临时添加一下路径，或者在 main 中处理
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))
from src.function import screen_shot, open_app
from src.input import choice_dialog

class PetActions:
    def __init__(self, parent_widget, dialogue_system):
        self.parent = parent_widget
        self.dialogue = dialogue_system

    def show_context_menu(self, global_pos):
        menu = QMenu(self.parent)

        # 打开常用软件子菜单
        app_menu = menu.addMenu("打开软件")
        
        apps = ["鹰角启动！","计算器", "记事本", "终端", "网易云"]
        for app in apps:
            action = QAction(app, self.parent)
            action.triggered.connect(lambda checked, a=app: self.do_open_app(a))
            app_menu.addAction(action)

        menu.addSeparator()
        # 截图/识别屏幕
        action_screenshot = QAction('识别屏幕 (截图)', self.parent)
        action_screenshot.triggered.connect(self.do_screenshot)
        menu.addAction(action_screenshot)
        
        action_quit = QAction('退出', self.parent)
        action_quit.triggered.connect(QApplication.instance().quit)
        menu.addAction(action_quit)

        menu.exec(global_pos)

    def do_screenshot(self):
        self.parent.play_action("screenshot")
        # 1. 询问用户保存位置
        choice = choice_dialog.ask_save_location(self.parent)
        
        save_path = None
        if choice == "desktop":
            save_path = os.path.join(os.path.expanduser("~"), "Desktop")
        elif choice == "default":
            # C:\Users\{user}\Pictures\Screenshots
            save_path = os.path.join(os.path.expanduser("~"), "Pictures", "Screenshots")
        elif choice == "none":
            self.dialogue.show_message("屏幕截图", "已取消截图保存")
            return

        print(f"正在识别屏幕... 保存到: {choice}")
        
        # 2. 为了防止截图带上桌宠自己，先将桌宠隐藏并刷新页面缓冲
        self.parent.hide()
        QApplication.processEvents()
        
        # 可选等待一小下，确保窗口完全从屏幕清除了视觉残留
        time.sleep(0.2)
        
        # 执行截图
        result = screen_shot.capture_screen_content(save_dir=save_path)
        
        # 截完图重新显示回来并置顶
        if hasattr(self.parent, "force_on_top"):
            self.parent.force_on_top()
        else:
            self.parent.show()
            self.parent.raise_()
        
        print(result)
        self.dialogue.show_message("屏幕截图", result)

    def do_open_app(self, app_name):
        self.parent.play_action("open_app")
        print(f"正在打开 {app_name}...")
        result = open_app.open_application(app_name)
        print(result)
        self.dialogue.show_message("打开软件", result)
