import pytest
import torch
from python_projects.modeling.day10_attention import (
    MultiHeadAttention,
    FeedForwardNetwork
)

def test_multi_head_attention_shapes():
    batch_size = 2
    seq_len = 3
    d_model = 8
    num_heads = 2
    
    try:
        mha = MultiHeadAttention(d_model=d_model, num_heads=num_heads)
        x = torch.randn(batch_size, seq_len, d_model)
        out = mha(x, x, x)
        assert out.shape == (batch_size, seq_len, d_model)
    except NotImplementedError:
        pytest.skip("MultiHeadAttention is not implemented yet.")

def test_multi_head_attention_divisibility():
    with pytest.raises(ValueError):
        MultiHeadAttention(d_model=7, num_heads=2)

def test_feed_forward_network_shapes():
    batch_size = 2
    seq_len = 3
    d_model = 8
    d_ff = 16
    
    try:
        ffn = FeedForwardNetwork(d_model=d_model, d_ff=d_ff)
        x = torch.randn(batch_size, seq_len, d_model)
        out = ffn(x)
        assert out.shape == (batch_size, seq_len, d_model)
    except NotImplementedError:
        pytest.skip("FeedForwardNetwork is not implemented yet.")
