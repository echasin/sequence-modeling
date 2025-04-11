import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

def read_events_csv(file_path):
    """Read and display events from CSV file."""
    try:
        # Read the CSV file
        df = pd.read_csv(file_path)
        
        # Convert date to datetime
        df['date'] = pd.to_datetime(df['date'])
        
        # Sort by ID and date
        df = df.sort_values(['id', 'date'])
        
        # Display basic information
        print("\n=== Events Data Summary ===")
        print(f"Total events: {len(df)}")
        print(f"Unique IDs: {df['id'].nunique()}")
        print("\n=== First 5 Events ===")
        print(df.head())
        
        # Display events by ID
        print("\n=== Events by ID ===")
        for id_val in df['id'].unique():
            print(f"\nID: {id_val}")
            id_events = df[df['id'] == id_val]
            for _, row in id_events.iterrows():
                print(f"  {row['date'].strftime('%Y-%m-%d')}: {row['event']}")
        
        return df
    
    except FileNotFoundError:
        print(f"Error: File '{file_path}' not found.")
        return None
    except Exception as e:
        print(f"Error reading file: {e}")
        return None

def plot_events_timeline(df):
    """Create a simple timeline plot of events."""
    plt.figure(figsize=(12, 6))
    
    # Plot events for each ID
    for id_val in df['id'].unique():
        id_events = df[df['id'] == id_val]
        plt.plot(id_events['date'], [id_val] * len(id_events), 'o', 
                label=f'ID {id_val}', markersize=10)
        
        # Add event labels
        for _, row in id_events.iterrows():
            plt.annotate(row['event'], 
                        (row['date'], id_val),
                        xytext=(10, 5), 
                        textcoords='offset points',
                        fontsize=8,
                        rotation=45)
    
    plt.yticks(df['id'].unique())
    plt.title('Events Timeline')
    plt.xlabel('Date')
    plt.ylabel('ID')
    plt.grid(True)
    plt.legend()
    
    # Adjust layout to prevent label cutoff
    plt.tight_layout()
    plt.show()

def main():
    # Use the current directory
    file_path = Path('events.csv')
    
    # Read and display events
    df = read_events_csv(file_path)
    
    if df is not None:
        # Create timeline visualization
        plot_events_timeline(df)

if __name__ == "__main__":
    main()
