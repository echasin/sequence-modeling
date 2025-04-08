import pandas as pd
from pathlib import Path
import sys
from tabulate import tabulate

def read_events_csv():
    """
    Read events.csv into a pandas DataFrame.
    Returns DataFrame with events data sorted by id and date.
    """
    try:
        # Define the file path
        file_path = Path('random_events.csv')
        
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
        
        # Sort by date and id
        df = df.sort_values(['date', 'id'])
        
        return df
        
    except pd.errors.EmptyDataError:
        print("Error: The CSV file is empty.")
        sys.exit(1)
    except Exception as e:
        print(f"Error reading CSV file: {e}")
        sys.exit(1)

def create_sequence_results(df):
    """
    Create a DataFrame with sequence results for each ID.
    """
    results = []
    for id_val in sorted(df['id'].unique()):
        events = df[df['id'] == id_val].sort_values('date')
        sequence = " → ".join(events['event'])
        start_date = events['date'].min().strftime('%Y-%m-%d')
        end_date = events['date'].max().strftime('%Y-%m-%d')
        
        results.append({
            'id': id_val,
            'sequence': sequence,
            'num_events': len(events),
            'start_date': start_date,
            'end_date': end_date
        })
    
    return pd.DataFrame(results)

def display_event_sequence(df):
    """
    Display events in a formatted table, ordered by date.
    """
    # Create a summary section
    print("\nEvent Sequence Summary:")
    print("-" * 50)
    print(f"Total events: {len(df)}")
    print(f"Date range: {df['date'].min().strftime('%Y-%m-%d')} to {df['date'].max().strftime('%Y-%m-%d')}")
    print(f"Number of unique IDs: {df['id'].nunique()}")
    
    # Prepare data for tabulate
    # Format date column to be more readable
    df_display = df.copy()
    df_display['date'] = df_display['date'].dt.strftime('%Y-%m-%d')
    
    # Create the table
    print("\nEvent Sequence (ordered by date):")
    print(tabulate(
        df_display,
        headers=['ID', 'Event', 'Date'],
        tablefmt='grid',
        showindex=False
    ))
    
    # Display sequence by ID
    print("\nEvent Sequences by ID:")
    print("-" * 50)
    for id_val in sorted(df['id'].unique()):
        events = df[df['id'] == id_val].sort_values('date')
        print(f"\nID: {id_val}")
        sequence = " → ".join(events['event'])
        print(f"Sequence: {sequence}")

def main():
    # Read the CSV file
    df = read_events_csv()
    
    # Display formatted event sequence
    display_event_sequence(df)
    
    # Create and save sequence results
    results_df = create_sequence_results(df)
    results_df.to_csv('results_id_seq.csv', index=False)
    print("\nSequence results saved to 'results_id_seq.csv'")
    
    # Display the contents of the results file
    print("\nContents of results_id_seq.csv:")
    print(tabulate(
        results_df,
        headers='keys',
        tablefmt='grid',
        showindex=False
    ))

if __name__ == "__main__":
    main()
