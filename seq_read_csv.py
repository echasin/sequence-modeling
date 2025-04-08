import pandas as pd
from pathlib import Path
import sys

def read_events_csv():
    """
    Read events.csv into a pandas DataFrame.
    Returns DataFrame with events data sorted by id and date.
    """
    try:
        # Define the file path
        file_path = Path('events.csv')
        
        # Check if file exists
        if not file_path.exists():
            print(f"Error: {file_path} not found.")
            sys.exit(1)
            
        # Read CSV into DataFrame
        df = pd.read_csv(file_path)
        
        # Verify required columns exist
        required_columns = ['id', 'event', 'date']
        if not all(col in df.columns for col in required_columns):
            print(f"Error: CSV must contain columns: {', '.join(required_columns)}")
            sys.exit(1)
            
        # Convert date to datetime
        df['date'] = pd.to_datetime(df['date'])
        
        # Sort by id and date
        df = df.sort_values(['id', 'date'])
        
        # Display DataFrame info
        print("\nDataFrame Summary:")
        print("-" * 50)
        print(f"Total rows: {len(df)}")
        print(f"Unique IDs: {df['id'].nunique()}")
        print(f"Date range: {df['date'].min().date()} to {df['date'].max().date()}")
        
        # Display first few rows
        print("\nFirst few rows of the DataFrame:")
        print(df.head())
        
        return df
        
    except pd.errors.EmptyDataError:
        print("Error: The CSV file is empty.")
        sys.exit(1)
    except Exception as e:
        print(f"Error reading CSV file: {e}")
        sys.exit(1)

def main():
    # Read the CSV file
    df = read_events_csv()
    
    # Example: Display events grouped by ID
    print("\nEvents grouped by ID:")
    print("-" * 50)
    for id_val in df['id'].unique():
        events = df[df['id'] == id_val]
        print(f"\nID: {id_val}")
        for _, row in events.iterrows():
            print(f"  {row['date'].strftime('%Y-%m-%d')}: {row['event']}")

if __name__ == "__main__":
    main()
