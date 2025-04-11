import pandas as pd
from pathlib import Path
import sys
from tabulate import tabulate

class EventProcessor:
    def __init__(self, input_file='src/data/source/events.csv', output_file='src/data/features/feature_sequence.csv'):
        self.input_file = Path(input_file)
        self.output_file = Path(output_file)
        self.data = []
        
    def read_events(self):
        """Read events from CSV file and generate pattern_base."""
        try:
            if not self.input_file.exists():
                print(f"Error: {self.input_file} not found.")
                sys.exit(1)
                
            # Read CSV into DataFrame
            df = pd.read_csv(self.input_file)
            
            # Verify required columns exist
            required_columns = ['id', 'event', 'date']
            if not all(col in df.columns for col in required_columns):
                print(f"Error: CSV must contain columns: {', '.join(required_columns)}")
                sys.exit(1)
                
            # Convert date to datetime
            df['date'] = pd.to_datetime(df['date'])
            
            # Sort by date, then by event (ascending) for same-day events
            df = df.sort_values(['id', 'date', 'event'])
            
            # Generate pattern_base for each ID
            pattern_bases = {}
            for id_val in df['id'].unique():
                id_events = df[df['id'] == id_val]
                # Convert events to strings and join with commas
                pattern_base = ','.join(id_events['event'].astype(str))
                pattern_bases[id_val] = pattern_base
            
            # Add pattern_base to DataFrame
            df['pattern_base'] = df['id'].map(pattern_bases)
            
            return df
            
        except pd.errors.EmptyDataError:
            print("Error: The CSV file is empty.")
            sys.exit(1)
        except Exception as e:
            print(f"Error reading CSV file: {e}")
            sys.exit(1)

    def display_summary(self, df):
        """Display summary of events."""
        print("\nEvents Summary:")
        print("-" * 50)
        print(f"Total events: {len(df)}")
        print(f"Number of unique IDs: {df['id'].nunique()}")
        print(f"Date range: {df['date'].min().strftime('%Y-%m-%d')} to {df['date'].max().strftime('%Y-%m-%d')}")
        
        print("\nEvents by ID:")
        for id_val in sorted(df['id'].unique()):
            id_events = df[df['id'] == id_val]
            print(f"\nID {id_val} ({len(id_events)} events):")
            sequence = " → ".join(id_events['event'].astype(str))
            print(f"Sequence: {sequence}")
            print(f"Pattern Base: {id_events.iloc[0]['pattern_base']}")

    def save_to_csv(self, df):
        """Save the events to a CSV file."""
        # Create output directory if it doesn't exist
        self.output_file.parent.mkdir(parents=True, exist_ok=True)
        
        # Select and reorder columns
        output_df = df[['id', 'date', 'event', 'pattern_base']]
        output_df.to_csv(self.output_file, index=False)
        print(f"\nData saved to {self.output_file}")

def main():
    # Create processor with specific file paths
    processor = EventProcessor(
        input_file='src/data/source/events.csv',
        output_file='src/data/features/feature_sequence.csv'
    )
    
    # Read events
    df = processor.read_events()
    
    # Display summary
    processor.display_summary(df)
    
    # Save to CSV
    processor.save_to_csv(df)

if __name__ == "__main__":
    main() 