"""
E2E tests for gemma2
"""

from pathlib import Path

import pytest

from axolotl.common.datasets import load_datasets
from axolotl.train import train
from axolotl.utils.config import normalize_config, validate_config
from axolotl.utils.dict import DictDefault


class TestGemma2:
    """
    Test case for Gemma2 models
    """

    @pytest.mark.parametrize(
        "sample_packing",
        [True, False],
    )
    def test_lora_gemma2(self, temp_dir, sample_packing):
        # pylint: disable=duplicate-code
        cfg = DictDefault(
            {
                "base_model": "axolotl-ai-co/gemma-2-33M",
                "trust_remote_code": True,
                "sample_packing": sample_packing,
                "flash_attention": True,
                "sequence_len": 2048,
                "adapter": "lora",
                "lora_r": 8,
                "lora_alpha": 16,
                "lora_dropout": 0.05,
                "lora_target_linear": True,
                "val_set_size": 0,
                "datasets": [
                    {
                        "path": "mlabonne/FineTome-100k",
                        "type": "chat_template",
                        "field_messages": "conversations",
                        "message_property_mappings": {
                            "role": "from",
                            "content": "value",
                        },
                        "drop_system_message": True,
                        "split": "train[:1%]",
                    },
                ],
                "special_tokens": {
                    "bos_token": "<bos>",
                    "eos_token": "<eos>",
                },
                "chat_template": "gemma",  # gemma2's template is same as gemma
                "num_epochs": 1,
                "micro_batch_size": 1,
                "gradient_accumulation_steps": 2,
                "output_dir": temp_dir,
                "learning_rate": 0.00001,
                "optimizer": "adamw_bnb_8bit",
                "lr_scheduler": "cosine",
                "max_steps": 5,
                "save_safetensors": True,
                "bf16": True,
            }
        )
        cfg = validate_config(cfg)
        normalize_config(cfg)
        dataset_meta = load_datasets(cfg=cfg)

        train(cfg=cfg, dataset_meta=dataset_meta)
        assert (Path(temp_dir) / "adapter_model.safetensors").exists()

    @pytest.mark.parametrize(
        "sample_packing",
        [True, False],
    )
    def test_fft_gemma2(self, temp_dir, sample_packing):
        # pylint: disable=duplicate-code
        cfg = DictDefault(
            {
                "base_model": "axolotl-ai-co/gemma-2-33M",
                "trust_remote_code": True,
                "sample_packing": sample_packing,
                "flash_attention": True,
                "sequence_len": 2048,
                "val_set_size": 0,
                "datasets": [
                    {
                        "path": "mlabonne/FineTome-100k",
                        "type": "chat_template",
                        "field_messages": "conversations",
                        "message_property_mappings": {
                            "role": "from",
                            "content": "value",
                        },
                        "split": "train[:1%]",
                        "drop_system_message": True,
                    },
                ],
                "chat_template": "gemma",  # gemma2's template is same as gemma
                "special_tokens": {
                    "bos_token": "<bos>",
                    "eos_token": "<eos>",
                },
                "num_epochs": 1,
                "micro_batch_size": 1,
                "gradient_accumulation_steps": 2,
                "output_dir": temp_dir,
                "learning_rate": 0.00001,
                "optimizer": "adamw_bnb_8bit",
                "lr_scheduler": "cosine",
                "max_steps": 5,
                "save_safetensors": True,
                "bf16": True,
            }
        )
        cfg = validate_config(cfg)
        normalize_config(cfg)
        dataset_meta = load_datasets(cfg=cfg)

        train(cfg=cfg, dataset_meta=dataset_meta)
        assert (Path(temp_dir) / "model.safetensors").exists()
