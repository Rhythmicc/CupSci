import os
import json
from QuickProject import user_root, user_lang, QproDefaultConsole, QproInfoString, _ask

enable_config = True
config_path = os.path.join(user_root, ".CupSci_config")

questions = {
    "work_path": {
        "type": "input",
        "message": "Please enter the work path of sci-hub: "
        if user_lang != "zh"
        else "请输入cup-sci的工作路径: ",
    },
    "username": {"type": "input", "message": "Please enter your webvpn username: "},
    "password": {"type": "password", "message": "Please enter your webvpn password: "},
}


def init_config():
    with open(config_path, "w") as f:
        json.dump(
            {i: _ask(questions[i]) for i in questions}, f, indent=4, ensure_ascii=False
        )
    QproDefaultConsole.print(
        QproInfoString,
        f'Config file has been created at: "{config_path}"'
        if user_lang != "zh"
        else f'配置文件已创建于: "{config_path}"',
    )


class CupSciConfig:
    def __init__(self):
        if not os.path.exists(config_path):
            init_config()
        with open(config_path, "r") as f:
            self.config = json.load(f)

    def select(self, key):
        if key not in self.config and key in questions:
            self.update(key, _ask(questions[key]))
        return self.config[key]

    def update(self, key, value):
        self.config[key] = value
        with open(config_path, "w") as f:
            json.dump(self.config, f, indent=4, ensure_ascii=False)
