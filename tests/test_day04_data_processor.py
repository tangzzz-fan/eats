import pytest
from python_projects.data_engineering.day04_data_processor import process_and_plot_data

def test_data_processor_file_not_found(capsys):
    try:
        # 应该优雅捕获 FileNotFoundError 并打印提示，不会向外抛出异常
        process_and_plot_data("non_existent_file.csv")
        captured = capsys.readouterr()
        # 验证是否输出了友好提示
        assert "not found" in captured.out.lower() or "error" in captured.out.lower()
    except NotImplementedError:
        pytest.skip("process_and_plot_data is not implemented yet.")
