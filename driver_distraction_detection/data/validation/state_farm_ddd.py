from queue import PriorityQueue

import pandas as pd
from pathlib import Path

from config.paths.state_farm_ddd import TRAIN_PROCESSED_CSV, EVAL_PROCESSED_CSV, TEST_PROCESSED_CSV, TRAIN_DIR, TEST_DIR


def validate_csv(
    csv_path: Path,
    images_dir: Path,
    require_subject: bool = True,
) -> bool:
    print(f"\nValidating: {csv_path}")

    if not csv_path.is_file():
        raise FileNotFoundError(f"CSV not found: {csv_path}")

    df = pd.read_csv(csv_path)

    # Check required columns
    missing_columns = {"subject", "classname", "img"} - set(df.columns)

    if missing_columns:
        raise ValueError(
            f"Missing columns in {csv_path}: {missing_columns}"
        )

    if df.empty:
        raise ValueError(f"CSV is empty: {csv_path}")

    # Check required values
    for column in ("classname", "img"):
        if df[column].isna().any() or df[column].astype(str).str.strip().eq("").any():
            raise ValueError(
                f"Empty values found in column '{column}'"
            )

    if require_subject:
        if df["subject"].isna().any() or df["subject"].astype(str).str.strip().eq("").any():
            raise ValueError(
                f"Empty subjects found in {csv_path}"
            )

    # Check valid classes
    invalid_classes = set(df["classname"].unique()) - set(range(10))

    if invalid_classes:
        raise ValueError(
            f"Invalid classes found: {invalid_classes}"
        )

    # Check image files
    image_paths = images_dir / df["img"]

    missing_images = [
        str(path)
        for path in image_paths
        if not path.is_file()
    ]

    if missing_images:
        raise FileNotFoundError(
            f"{len(missing_images)} images not found. "
            f"{missing_images}"
        )

    print(f"Rows: {len(df)}")
    print(f"Classes: {sorted(df['classname'].unique().tolist())}")
    print("All referenced images exist.")

    return True


def validate_subject_split(
    train_csv: Path,
    eval_csv: Path,
) -> bool:
    train_df = pd.read_csv(train_csv)
    eval_df = pd.read_csv(eval_csv)

    train_subjects = set(
        train_df["subject"].dropna().unique()
    )
    eval_subjects = set(
        eval_df["subject"].dropna().unique()
    )

    overlapping_subjects = train_subjects & eval_subjects

    if overlapping_subjects:
        raise ValueError(
            f"Subjects overlap between train and eval: "
            f"{overlapping_subjects}"
        )

    print("\nTrain/eval subject split is valid.")
    print(f"Train subjects: {len(train_subjects)}")
    print(f"Eval subjects: {len(eval_subjects)}")

    return True


def validate_all() -> None:
    print("=== VALIDATING ===")

    validate_csv(
        TRAIN_PROCESSED_CSV,
        TRAIN_DIR,
        require_subject=True,
    )

    validate_csv(
        EVAL_PROCESSED_CSV,
        TRAIN_DIR,
        require_subject=True,
    )

    validate_csv(
        TEST_PROCESSED_CSV,
        TEST_DIR,
        require_subject=False,
    )

    validate_subject_split(TRAIN_PROCESSED_CSV, EVAL_PROCESSED_CSV)

    print("\nAll validations completed successfully.")
