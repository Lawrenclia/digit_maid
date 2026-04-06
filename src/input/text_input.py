from PyQt6.QtWidgets import (
    QInputDialog,
    QLineEdit,
    QDialog,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QDoubleSpinBox,
)
from PyQt6.QtCore import Qt

def get_text_input(parent_widget, title="输入", label="请输入内容:"):
    """
    弹出一个简单的文本输入对话框，获取用户输入。
    
    Args:
        parent_widget: 父窗口部件
        title (str): 对话框标题
        label (str): 输入框标签文字
        
    Returns:
        str: 用户输入的文本。如果用户取消，则返回 None。
    """
    text, ok = QInputDialog.getText(parent_widget, title, label, QLineEdit.EchoMode.Normal, "")
    
    if ok and text:
        return text.strip()
    return None


def get_double_input(
    parent_widget,
    title="输入数值",
    label="请输入数值:",
    value=1.0,
    min_value=0.0,
    max_value=10.0,
    decimals=1,
    step=0.1,
):
    """弹出一个自定义数值输入框，返回 float；取消时返回 None。"""
    dialog = QDialog(parent_widget)
    dialog.setWindowTitle(title)
    dialog.setModal(True)
    dialog.setMinimumWidth(360)
    dialog.setStyleSheet(
        """
        QDialog {
            background-color: rgba(255, 248, 245, 245);
            border: 2px solid #ff3b30;
            border-radius: 12px;
        }
        QLabel {
            color: #4a2b2b;
            font-size: 14px;
            font-weight: 700;
        }
        QDoubleSpinBox {
            background: white;
            border: 2px solid #ffb3ad;
            border-radius: 10px;
            padding: 8px 10px;
            font-size: 16px;
            font-weight: 700;
            color: #2b2b2b;
        }
        QPushButton {
            min-width: 96px;
            padding: 8px 14px;
            border-radius: 10px;
            font-size: 13px;
            font-weight: 700;
        }
        QPushButton#ok_btn {
            background-color: #ff3b30;
            color: white;
            border: none;
        }
        QPushButton#ok_btn:hover {
            background-color: #ff5a52;
        }
        QPushButton#cancel_btn {
            background-color: #f2e7e5;
            color: #6a4a4a;
            border: 1px solid #d7c2bf;
        }
        QPushButton#cancel_btn:hover {
            background-color: #eadedb;
        }
        """
    )

    layout = QVBoxLayout(dialog)
    layout.setContentsMargins(16, 16, 16, 14)
    layout.setSpacing(12)

    label_widget = QLabel(label, dialog)
    layout.addWidget(label_widget)

    spin = QDoubleSpinBox(dialog)
    spin.setDecimals(max(0, int(decimals)))
    spin.setRange(float(min_value), float(max_value))
    spin.setSingleStep(float(step))
    clamped_value = max(float(min_value), min(float(max_value), float(value)))
    spin.setValue(clamped_value)
    spin.setAlignment(Qt.AlignmentFlag.AlignCenter)
    spin.selectAll()
    layout.addWidget(spin)

    btn_row = QHBoxLayout()
    btn_row.addStretch(1)

    cancel_btn = QPushButton("取消", dialog)
    cancel_btn.setObjectName("cancel_btn")
    cancel_btn.clicked.connect(dialog.reject)
    btn_row.addWidget(cancel_btn)

    ok_btn = QPushButton("确定", dialog)
    ok_btn.setObjectName("ok_btn")
    ok_btn.clicked.connect(dialog.accept)
    btn_row.addWidget(ok_btn)

    layout.addLayout(btn_row)

    if dialog.exec() == QDialog.DialogCode.Accepted:
        value = spin.value()
        return round(value, max(0, int(decimals)))
    return None
