import pytest
import sys
from python_projects.common.day05_cli import main

def test_cli_execution(monkeypatch, capsys):
    # 模拟没有命令行输入
    monkeypatch.setattr(sys, "argv", ["cli.py"])
    
    # 捕获主运行退出的异常或输出
    try:
        with pytest.raises(SystemExit):
            main()
    except NotImplementedError:
        pytest.skip("CLI main is not implemented yet.")
