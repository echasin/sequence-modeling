# Feature_count_seq.py
import pandas as pd
from pathlib import Path
import sys
from tabulate import tabulate
from collections import Counter

class SequenceAnalyzer:
    def __init__(self, file_path='results_id_seq.csv'):
        self.file_path = Path(file_path)
        self.df = None
        self.unique_sequences = None
        
    def read_sequences(self):
        """Read and validate the sequence CSV file."""
        try:
            if not self.file_path.exists():
                print(f"Error: {self.file_path} not found.")
                sys.exit(1)
                
            self.df = pd.read_csv(self.file_path)
            
            # Verify required columns exist
            if 'sequence' not in self.df.columns:
                print("Error: CSV must contain 'sequence' column")
                sys.exit(1)
                
            return True
            
        except Exception as e:
            print(f"Error reading CSV file: {e}")
            sys.exit(1)
    
    def analyze_sequences(self):
        """Analyze sequences and count unique patterns."""
        # Count unique sequences
        sequence_counts = Counter(self.df['sequence'])
        
        # Create analysis results
        analysis_results = []
        for sequence, count in sequence_counts.items():
            # Get IDs that share this sequence
            ids_with_sequence = self.df[self.df['sequence'] == sequence]['id'].tolist()
            
            analysis_results.append({
                'sequence': sequence,
                'count': count,
                'ids': sorted(ids_with_sequence),
                'length': len(sequence.split('→')),
            })
            
        # Convert to DataFrame for easy handling
        self.unique_sequences = pd.DataFrame(analysis_results)
        self.unique_sequences = self.unique_sequences.sort_values('count', ascending=False)
        
    def display_results(self):
        """Display analysis results."""
        print("\nSequence Analysis Summary:")
        print("-" * 50)
        print(f"Total number of sequences: {len(self.df)}")
        print(f"Number of unique sequences: {len(self.unique_sequences)}")
        
        print("\nUnique Sequences (sorted by frequency):")
        print(tabulate(
            self.unique_sequences,
            headers={
                'sequence': 'Sequence',
                'count': 'Frequency',
                'ids': 'IDs',
                'length': 'Length'
            },
            tablefmt='grid',
            showindex=False
        ))
        
        # Display sequence length distribution
        length_dist = self.unique_sequences.groupby('length')['count'].sum()
        print("\nSequence Length Distribution:")
        print(tabulate(
            [[length, count] for length, count in length_dist.items()],
            headers=['Length', 'Count'],
            tablefmt='grid'
        ))
    
    def save_analysis(self, output_file='sequence_analysis.csv'):
        """Save analysis results to CSV."""
        # Convert IDs list to string for CSV storage
        self.unique_sequences['ids'] = self.unique_sequences['ids'].apply(lambda x: ', '.join(map(str, x)))
        self.unique_sequences.to_csv(output_file, index=False)
        print(f"\nAnalysis results saved to '{output_file}'")

def main():
    # Initialize analyzer
    analyzer = SequenceAnalyzer()
    
    # Read and analyze sequences
    analyzer.read_sequences()
    analyzer.analyze_sequences()
    
    # Display results
    analyzer.display_results()
    
    # Save analysis results
    analyzer.save_analysis()

if __name__ == "__main__":
    main()