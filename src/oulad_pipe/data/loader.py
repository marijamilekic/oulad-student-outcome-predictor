from pathlib import Path
import pandas as pd

DATA_RAW_DIR = Path("data/raw")


def load_student_info() -> pd.DataFrame:
    return pd.read_csv("data/rawstudentInfo.csv")


def load_student_registration() -> pd.DataFrame:
    return pd.read_csv(DATA_RAW_DIR / "studentRegistration.csv")


def load_courses() -> pd.DataFrame:
    return pd.read_csv(DATA_RAW_DIR / "courses.csv")


def load_vle() -> pd.DataFrame:
    return pd.read_csv(DATA_RAW_DIR / "vle.csv")


def load_student_vle() -> pd.DataFrame:
    return pd.read_csv(DATA_RAW_DIR / "studentVle.csv")


def load_assessments() -> pd.DataFrame:
    return pd.read_csv(DATA_RAW_DIR / "assessments.csv")


def load_student_assessment() -> pd.DataFrame:
    return pd.read_csv(DATA_RAW_DIR / "studentAssessment.csv")