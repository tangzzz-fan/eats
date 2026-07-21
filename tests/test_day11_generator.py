import pytest
import torch
from python_projects.modeling.day11_generator import (
    LanguageModel,
    top_k_sampling,
    generate_sequence
)

def test_language_model_shapes():
    vocab_size = 10
    d_model = 8
    nhead = 2
    
    try:
        model = LanguageModel(vocab_size=vocab_size, d_model=d_model, nhead=nhead)
        x = torch.randint(0, vocab_size, (2, 5))  # batch=2, seq=5
        logits = model(x)
        assert logits.shape == (2, 5, vocab_size)
    except NotImplementedError:
        pytest.skip("LanguageModel is not implemented yet.")

def test_top_k_sampling():
    vocab_size = 5
    logits = torch.tensor([1.0, 10.0, 2.0, 0.5, 0.1])
    try:
        idx = top_k_sampling(logits, k=2)
        assert isinstance(idx, int)
        # top 2 indices are 1 and 2
        assert idx in [1, 2]
    except NotImplementedError:
        pytest.skip("top_k_sampling is not implemented yet.")

def test_generate_sequence():
    vocab_size = 10
    d_model = 8
    nhead = 2
    try:
        model = LanguageModel(vocab_size=vocab_size, d_model=d_model, nhead=nhead)
        start_tokens = [1, 2, 3]
        
        # 强制前向不报错（若 model 未实现则跳过）
        # 我们 mock 采样
        res = generate_sequence(model, start_tokens, max_len=5, k=3)
        assert len(res) <= 8
        assert res[:3] == [1, 2, 3]
    except NotImplementedError:
        pytest.skip("generate_sequence or LanguageModel is not implemented yet.")
