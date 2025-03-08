import argparse
import yaml
from process_data import process_data
from process_data_all import process_data_all

def load_config(config_path):
    """Loads configuration from a YAML file."""
    with open(config_path, "r") as file:
        return yaml.safe_load(file)

def main():
    parser = argparse.ArgumentParser(description="News Data Processing Pipeline")
    parser.add_argument("command", choices=["process_data", "process_data_all"], help="Command to execute")
    parser.add_argument("-cfg", "--config", required=True, help="Path to the configuration YAML file")
    parser.add_argument("-dataset", required=True, help="Dataset")
    parser.add_argument("-dirout", required=True, help="Output directory for processed files")

    args = parser.parse_args()

    # Load configuration
    config = load_config(args.config)

    if args.command == "process_data":
        print(f"📌 Running data processing for dataset: {args.dataset}")
        target_words = config.get("target_words", [])
        process_data(target_words, args.dirout)

    elif args.command == "process_data_all":
        print(f"📌 Running data processing for all words in dataset: {args.dataset}")
        process_data_all(args.dirout)

if __name__ == "__main__":
    main()
