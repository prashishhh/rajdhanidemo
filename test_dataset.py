from datasets import load_dataset

nepali_ds = load_dataset(
    "parquet",
    data_files={
        "train": "https://huggingface.co/datasets/csebuetnlp/xlsum/resolve/main/nepali/train/0000.parquet",
        "validation": "https://huggingface.co/datasets/csebuetnlp/xlsum/resolve/main/nepali/validation/0000.parquet",
        "test": "https://huggingface.co/datasets/csebuetnlp/xlsum/resolve/main/nepali/test/0000.parquet",
    }
)

print(nepali_ds)
print(nepali_ds["train"][0])
