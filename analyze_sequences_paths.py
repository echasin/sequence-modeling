# analyze_path_timing.py
import pandas as pd
import numpy as np
from pathlib import Path
from tabulate import tabulate
from datetime import datetime

class PathTimingAnalyzer:
    def __init__(self, file_path='patterned_events.csv'):
        self.file_path = Path(file_path)
        self.df = None
        self.path_timings = None
        
    def read_data(self):
        """Read and prepare the event data."""
        try:
            if not self.file_path.exists():
                print(f"Error: {self.file_path} not found.")
                return False
                
            # Read CSV and convert date to datetime
            self.df = pd.read_csv(self.file_path)
            self.df['date'] = pd.to_datetime(self.df['date'])
            return True
            
        except Exception as e:
            print(f"Error reading CSV file: {e}")
            return False
    
    def calculate_path_timings(self):
        """Calculate timing statistics for each unique path segment."""
        path_timings = []
        
        # Process each ID separately
        for id_val in self.df['id'].unique():
            id_events = self.df[self.df['id'] == id_val].sort_values('date')
            
            # Look at each consecutive pair of events
            for i in range(len(id_events) - 1):
                current = id_events.iloc[i]
                next_event = id_events.iloc[i + 1]
                
                # Calculate time difference in hours
                time_diff = (next_event['date'] - current['date']).total_seconds() / 3600
                
                path_segment = f"{current['event']}-{next_event['event']}"
                
                path_timings.append({
                    'path_segment': path_segment,
                    'time_hours': time_diff,
                    'id': id_val,
                    'start_date': current['date'],
                    'end_date': next_event['date']
                })
        
        # Convert to DataFrame
        self.path_timings = pd.DataFrame(path_timings)
    
    def analyze_path_segments(self):
        """Create summary statistics for each unique path segment."""
        # Group by path segment and calculate statistics
        stats = self.path_timings.groupby('path_segment').agg({
            'time_hours': ['count', 'mean', 'min', 'max', 'std'],
            'id': 'nunique'
        }).round(2)
        
        # Flatten column names
        stats.columns = ['frequency', 'avg_hours', 'min_hours', 'max_hours', 'std_hours', 'unique_ids']
        stats = stats.reset_index()
        
        # Sort by path_segment alphabetically
        stats = stats.sort_values('path_segment', ascending=True)
        
        return stats
    
    def save_results(self, stats):
        """Save analysis results to CSV file."""
        output_file = 'sequence_analysis_paths.csv'
        
        # Rename columns for clarity
        stats_output = stats.copy()
        stats_output.columns = [
            'Path_Segment',
            'Frequency',
            'Average_Hours',
            'Minimum_Hours',
            'Maximum_Hours',
            'Std_Dev_Hours',
            'Unique_IDs'
        ]
        
        # Save to CSV
        stats_output.to_csv(output_file, index=False)
        print(f"\nAnalysis results saved to: {output_file}")
        
        # Display sample of results
        print("\nFirst few rows of the output file:")
        print(tabulate(
            stats_output.head(),
            headers='keys',
            tablefmt='grid',
            showindex=False,
            floatfmt=".2f"
        ))
    
    def display_summary(self, stats):
        """Display summary statistics."""
        print("\nPath Segment Analysis Summary")
        print("=" * 50)
        print(f"Total unique path segments: {len(stats)}")
        print(f"Total transitions analyzed: {stats['frequency'].sum()}")
        print(f"Average transition time: {stats['avg_hours'].mean():.2f} hours")
        print(f"Overall time range: {stats['min_hours'].min():.2f} to {stats['max_hours'].max():.2f} hours")

def main():
    # Initialize analyzer
    analyzer = PathTimingAnalyzer()
    
    # Read and process data
    if analyzer.read_data():
        # Calculate path timings
        analyzer.calculate_path_timings()
        
        # Analyze path segments
        stats = analyzer.analyze_path_segments()
        
        # Display summary
        analyzer.display_summary(stats)
        
        # Save results
        analyzer.save_results(stats)

if __name__ == "__main__":
    main()