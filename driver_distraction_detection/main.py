from data.processing.state_farm_ddd import generate_processed_test, generate_processed_train_eval
from data.validation.state_farm_ddd import validate_all

if __name__ == "__main__":
    generate_processed_train_eval()
    generate_processed_test()
    validate_all()
