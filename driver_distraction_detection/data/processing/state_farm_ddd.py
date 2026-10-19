import pandas as pd
from sklearn.model_selection import train_test_split

from config.paths.state_farm_ddd import (
    TRAIN_RAW_CSV, TRAIN_PROCESSED_CSV, EVAL_PROCESSED_CSV,
    TEST_RAW_CSV, TEST_PROCESSED_CSV
)


def generate_processed_train_eval() -> None:
    print("=== TRAIN AND EVAL DATASET SPLIT AND PROCESSING ===")

    # Read source CSV
    df = pd.read_csv(TRAIN_RAW_CSV)

    # Remove the 'c' prefix from classname
    df["classname"] = df["classname"].str.replace(r"^c", "", regex=True)

    # Get unique subjects
    subjects = df["subject"].dropna().unique()

    # Split subjects into train and eval
    train_subjects, eval_subjects = train_test_split(
        subjects,
        train_size=0.8,
        random_state=42,
        shuffle=True
    )

    # Generate datasets based on subjects
    df_train = df[df["subject"].isin(train_subjects)].copy()
    df_eval = df[df["subject"].isin(eval_subjects)].copy()

    # Save CSV files
    df_train.to_csv(TRAIN_PROCESSED_CSV, index=False)
    df_eval.to_csv(EVAL_PROCESSED_CSV, index=False)

    # Display statistics
    print(f"Original images: {len(df)}")
    print(f"Train images: {len(df_train)} ({len(df_train) / len(df) * 100:.2f}%)")
    print(f"Eval images: {len(df_eval)} ({len(df_eval) / len(df) * 100:.2f}%)")
    print(f"Train CSV generated at: {TRAIN_PROCESSED_CSV}")
    print(f"Eval CSV generated at: {EVAL_PROCESSED_CSV}")
    print()


def generate_processed_test() -> None:
    print("=== PROCESSING TEST DATASET ===")

    # Read source CSV
    df = pd.read_csv(TEST_RAW_CSV)

    # Generate the new CSV
    df_output = pd.DataFrame({
        "subject": "",
        "classname": df["classname"].str.replace(r"^c", "", regex=True),
        "img": df["image"].str.extract(r"(img_.*)", expand=False)
    })

    # Save the CSV to the predefined path
    df_output.to_csv(TEST_PROCESSED_CSV, index=False)

    print(f"Test CSV generated at: {TEST_PROCESSED_CSV}")
    print()