import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random
import string

class PatternedPathGenerator:
    def __init__(self, num_ids, num_patterns=10, min_hops=3, max_hops=10, 
                 start_date=datetime(2024, 1, 1)):
        self.num_ids = num_ids
        self.num_patterns = num_patterns
        self.min_hops = min_hops
        self.max_hops = max_hops
        self.start_date = start_date
        self.events = list(string.ascii_uppercase[:7])  # A through G
        self.data = []
        self.patterns = self.generate_base_patterns()

    def generate_base_patterns(self):
        """Generate base patterns that will be used as templates."""
        patterns = []
        for _ in range(self.num_patterns):
            pattern_length = random.randint(self.min_hops, self.max_hops)
            
            # Create a more structured pattern
            pattern = []
            # Always start with 'A'
            pattern.append('A')
            
            # Middle events follow some rules
            for i in range(pattern_length - 2):
                if i % 2 == 0:
                    # Even positions tend to progress forward in alphabet
                    prev = pattern[-1]
                    next_choices = [c for c in self.events if c > prev]
                    if next_choices:
                        pattern.append(random.choice(next_choices))
                    else:
                        pattern.append(random.choice(self.events))
                else:
                    # Odd positions are more random
                    pattern.append(random.choice(self.events))
            
            # Last event tends to be towards end of alphabet
            pattern.append(random.choice(self.events[3:]))  # Choose from D-G
            
            patterns.append(pattern)
        return patterns

    def apply_pattern_variation(self, base_pattern):
        """Apply small variations to a base pattern."""
        pattern = base_pattern.copy()
        
        # Possibly add an extra event (20% chance)
        if random.random() < 0.2 and len(pattern) < self.max_hops:
            insert_pos = random.randint(1, len(pattern)-1)
            pattern.insert(insert_pos, random.choice(self.events))
            
        # Possibly modify one event (30% chance)
        if random.random() < 0.3 and len(pattern) > 3:
            modify_pos = random.randint(1, len(pattern)-2)  # Don't modify first or last
            pattern[modify_pos] = random.choice(self.events)
        
        return pattern

    def generate_random_dates(self, num_dates, start_date):
        """Generate sorted random dates within 6 months of start_date."""
        date_range = pd.date_range(
            start=start_date,
            end=start_date + timedelta(days=180),
            periods=num_dates
        )
        return sorted(pd.to_datetime(np.random.choice(date_range, num_dates, replace=False)))

    def generate_path(self, id_num):
        """Generate a path based on one of the patterns."""
        # Select a base pattern
        base_pattern = random.choice(self.patterns)
        
        # Apply variations to create unique but similar path
        events = self.apply_pattern_variation(base_pattern)
        
        # Random start date for this ID
        id_start_date = self.start_date + timedelta(
            days=random.randint(0, 30)
        )
        
        # Generate dates
        dates = self.generate_random_dates(len(events), id_start_date)
        
        # Create path entries
        for date, event in zip(dates, events):
            self.data.append({
                'id': id_num,
                'event': event,
                'date': pd.Timestamp(date).strftime('%Y-%m-%d'),
                'pattern_base': ''.join(base_pattern)  # Store original pattern for analysis
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
        
        print("\nBase Patterns Used:")
        for i, pattern in enumerate(self.patterns, 1):
            print(f"Pattern {i}: {' → '.join(pattern)}")
        
        print("\nSample of Generated Sequences:")
        sample_ids = sorted(df['id'].unique())[:5]  # Show first 5 IDs
        for id_val in sample_ids:
            id_events = df[df['id'] == id_val]
            print(f"\nID {id_val} ({len(id_events)} events):")
            sequence = " → ".join(id_events['event'])
            print(f"Sequence: {sequence}")
            print(f"Based on pattern: {id_events.iloc[0]['pattern_base']}")

def main():
    # Configuration
    NUM_IDS = 1000  # Number of IDs to generate paths for
    NUM_PATTERNS = 1  # Number of base patterns to use
    MIN_HOPS = 3
    MAX_HOPS = 10
    START_DATE = datetime(2024, 1, 1)
    
    # Create generator
    generator = PatternedPathGenerator(
        num_ids=NUM_IDS,
        num_patterns=NUM_PATTERNS,
        min_hops=MIN_HOPS,
        max_hops=MAX_HOPS,
        start_date=START_DATE
    )
    
    # Generate paths
    df = generator.generate_all_paths()
    
    # Save to CSV
    generator.save_to_csv(df, filename='patterned_events.csv')
    
    # Display summary
    generator.display_summary(df)

if __name__ == "__main__":
    main()
