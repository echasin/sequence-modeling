import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random
import string

class RandomPathGenerator:
    def __init__(self, num_ids, min_hops=3, max_hops=10, 
                 start_date=datetime(2024, 1, 1)):
        self.num_ids = num_ids
        self.min_hops = min_hops
        self.max_hops = max_hops
        self.start_date = start_date
        self.events = list(string.ascii_uppercase[:7])  # A through G
        self.data = []

    def generate_random_dates(self, num_dates, start_date):
        """Generate sorted random dates within 6 months of start_date."""
        date_range = pd.date_range(
            start=start_date,
            end=start_date + timedelta(days=180),  # 6 months
            periods=num_dates
        )
        # Convert numpy datetime64 to pandas Timestamp
        return sorted(pd.to_datetime(np.random.choice(date_range, num_dates, replace=False)))

    def generate_path(self, id_num):
        """Generate a random path for a single ID."""
        # Random number of hops for this path
        num_hops = random.randint(self.min_hops, self.max_hops)
        
        # Random start date for this ID
        id_start_date = self.start_date + timedelta(
            days=random.randint(0, 30)  # Randomize start within first month
        )
        
        # Generate random dates for this path
        dates = self.generate_random_dates(num_hops, id_start_date)
        
        # Generate random events (can repeat)
        events = random.choices(self.events, k=num_hops)
        
        # Create path entries
        for date, event in zip(dates, events):
            self.data.append({
                'id': id_num,
                'event': event,
                'date': pd.Timestamp(date).strftime('%Y-%m-%d')  # Convert to Timestamp before strftime
            })

    def generate_all_paths(self):
        """Generate paths for all IDs."""
        for id_num in range(1, self.num_ids + 1):
            self.generate_path(id_num)
        
        # Convert to DataFrame and sort
        df = pd.DataFrame(self.data)
        df = df.sort_values(['id', 'date'])
        return df

    def save_to_csv(self, df, filename='random_events.csv'):
        """Save the generated paths to a CSV file."""
        df.to_csv(filename, index=False)
        print(f"\nData saved to {filename}")

    def display_summary(self, df):
        """Display summary of generated paths."""
        print("\nGenerated Paths Summary:")
        print("-" * 50)
        print(f"Total events generated: {len(df)}")
        print(f"Number of unique IDs: {df['id'].nunique()}")
        print(f"Date range: {df['date'].min()} to {df['date'].max()}")
        
        print("\nEvents per ID:")
        print(df.groupby('id').size().to_string())
        
        print("\nPath Sequences by ID:")
        for id_val in sorted(df['id'].unique()):
            id_events = df[df['id'] == id_val]
            print(f"\nID {id_val} ({len(id_events)} events):")
            sequence = " → ".join(id_events['event'])
            print(f"Sequence: {sequence}")
            print(f"Dates: {', '.join(id_events['date'])}")

def main():
    # Configuration
    NUM_IDS = 1000  # Number of IDs to generate paths for
    MIN_HOPS = 3
    MAX_HOPS = 10
    START_DATE = datetime(2024, 1, 1)
    
    # Create generator
    generator = RandomPathGenerator(
        num_ids=NUM_IDS,
        min_hops=MIN_HOPS,
        max_hops=MAX_HOPS,
        start_date=START_DATE
    )
    
    # Generate paths
    df = generator.generate_all_paths()
    
    # Save to CSV
    generator.save_to_csv(df, filename='random_events.csv')
    
    # Display summary
    generator.display_summary(df)

if __name__ == "__main__":
    main()
