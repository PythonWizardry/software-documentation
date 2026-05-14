import os

from src.reader.dataset_reader import DatasetReader
from src.strategy.strategy_factory import create_strategy
from src.utils.config_loader import load_config


def main() -> None:
    base_dir = os.path.dirname(__file__)
    config_path = os.path.join(base_dir, "..", "config", "config.yaml")
    config = load_config(config_path)

    dataset_cfg = config.get("dataset", {})
    reader = DatasetReader(
        api_url=dataset_cfg.get("url"),
        local_path=dataset_cfg.get("local_path", "data/dataset.csv"),
        limit=dataset_cfg.get("limit", 200),
    )

    force_download = dataset_cfg.get("force_download", False)
    if force_download:
        reader.fetch_and_save()

    records = reader.read()
    if not records:
        print("No data loaded. Exiting.")
        return

    strategy = create_strategy(config)
    try:
        strategy.write_batch(records)
    finally:
        strategy.close()


if __name__ == "__main__":
    main()
