# 共性技术询价推荐的离线比较与再验证

仓库维护企业技术需求、展示机会、试询与反馈资料。展示和回函使用服务窗口的相对日编号。字段 minute 和 cutoff 是历史系统字段名，单位仍为日。

资料为合成输入。各来源文件的单位、标识及关联见 [资料字典](资料字典.md)。

## 检查资料

使用 Python 3.11。NumPy 与 SciPy 版本在依赖清单中固定。已有环境可直接执行资料检查。首次在本地使用时可以建立虚拟环境并安装依赖。

```sh
python3 -m venv .venv
. .venv/bin/activate
python3 -m pip install -r requirements.txt
python3 -m unittest discover -s tests -v
```

检查只读原始 JSON，报告编号、记录引用、相互关联的原始资料及运行环境是否可用。
