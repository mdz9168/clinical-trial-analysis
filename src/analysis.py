import pandas as pd
import os

DATA_PATH = "data/alzheimers_trials_clean.csv"
OUTPUT_TABLE = "reports/summary_tables.csv"

def load_data(path):
    if not os.path.exists(path):
        raise FileNotFoundError(f"Can't find file at: {path}")
    df = pd.read_csv(path)
    print(f"✅ Loaded {len(df)} rows from {path}")
    return df

def run_analysis(df):
    # the trial count per sponsor
    sponsor_counts = df['sponsor'].value_counts().reset_index()
    sponsor_counts.columns = ['sponsor', 'trial_count']

    # Study type count
    study_types = df['study_type'].value_counts().reset_index()
    study_types.columns = ['study_type', 'count']

    # the enrollment stats if column exists
    enrollment_summary = pd.DataFrame()
    if 'enrollment' in df.columns:
        try:
            df['enrollment'] = pd.to_numeric(df['enrollment'], errors='coerce')
            enrollment_summary = df['enrollment'].describe().to_frame().T
        except Exception as e:
            print(f"⚠️ Enrollment column could not be processed: {e}")

    return sponsor_counts, study_types, enrollment_summary

def save_summaries(sponsor_df, study_df, enrollment_df):
    with pd.ExcelWriter(OUTPUT_TABLE.replace('.csv', '.xlsx')) as writer:
        sponsor_df.to_excel(writer, sheet_name='Sponsors', index=False)
        study_df.to_excel(writer, sheet_name='StudyTypes', index=False)
        if not enrollment_df.empty:
            enrollment_df.to_excel(writer, sheet_name='EnrollmentSummary', index=False)
    print(f"✅ Saved summary tables to {OUTPUT_TABLE.replace('.csv', '.xlsx')}")

def main():
    df = load_data(DATA_PATH)
    sponsors, studies, enrollments = run_analysis(df)
    save_summaries(sponsors, studies, enrollments)

if __name__ == "__main__":
    main()
