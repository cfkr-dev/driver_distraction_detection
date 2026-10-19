from .global_paths import STATE_FARM_DDD_DIR

# --- DATA ---
DATA_DIR = STATE_FARM_DDD_DIR / "data"
TRAIN_DIR = DATA_DIR / "train"
TEST_DIR = DATA_DIR / "test"

# --- METADATA ---
METADATA_DIR = STATE_FARM_DDD_DIR / "metadata"
RAW_DIR = METADATA_DIR / "raw"
PROCESSED_DIR = METADATA_DIR / "processed"

TRAIN_RAW_CSV = RAW_DIR / "train.csv"
TEST_RAW_CSV = RAW_DIR / "test.csv"
LABELS_CSV = RAW_DIR / "labels.csv"

TRAIN_PROCESSED_CSV = PROCESSED_DIR / "train.csv"
EVAL_PROCESSED_CSV = PROCESSED_DIR / "eval.csv"
TEST_PROCESSED_CSV = PROCESSED_DIR / "test.csv"
