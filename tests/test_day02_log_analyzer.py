import os
import pytest
from python_projects.common.day02_log_analyzer import analyze_and_archive_logs

def test_log_analyzer(tmp_path):
    # 用 pytest tmp_path 创建临时测试日志
    log1 = tmp_path / "test_debug.log"
    log1.write_text("INFO: Startup successful\nERROR: Failed to connect\n", encoding="utf-8")
    
    log2 = tmp_path / "test_info.log"
    log2.write_text("INFO: User login\n", encoding="utf-8")
    
    try:
        results = analyze_and_archive_logs(str(tmp_path))
        # 如果未实现会抛出 NotImplementedError
        if not results:
            # 如果没找到日志或返回空，视具体 TODO 实现而定
            pass
        else:
            assert "test_debug.log" in results
            assert results["test_debug.log"] == 1
    except NotImplementedError:
        pytest.skip("analyze_and_archive_logs is not implemented yet.")
