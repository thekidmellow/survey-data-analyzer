from data_manager import DataManager

def load_sample_data():
    """Load sample data function for the main application."""
    data_manager = DataManager()
    return data_manager.create_sample_data()

if __name__ == "__main__":
    # Test the sample data loading
    sample = load_sample_data()
    print(f"Sample data loaded: {len(sample)} records")
    print("Sample record:", sample[0] if sample else "No data")