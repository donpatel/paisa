import pandas as pd
import os

def import_nq_futures_data(file_path):
    """
    Import 1-minute /NQ futures data from a text file.
    
    Args:
        file_path (str): Path to the text file containing the NQ futures data
        
    Returns:
        pandas.DataFrame: DataFrame containing the parsed futures data
    """
    # Check if file exists
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"The file {file_path} does not exist.")
    
    try:
        # Attempt to read the file - common formats for futures data
        # Assuming standard format: DateTime, Open, High, Low, Close, Volume
        # First try a comma-separated format
        df = pd.read_csv(file_path, parse_dates=True)
        
        # If the file doesn't have headers, try with explicit column names
        if len(df.columns) <= 2 or 'Open' not in df.columns:
            df = pd.read_csv(file_path, 
                             names=['DateTime', 'Open', 'High', 'Low', 'Close', 'Volume'],
                             parse_dates=['DateTime'])
        
        # If the file is tab-delimited, try this format
        if len(df.columns) == 1:
            df = pd.read_csv(file_path, sep='\t', parse_dates=True)
            
            # And if needed, try with explicit column names
            if len(df.columns) <= 2 or 'Open' not in df.columns:
                df = pd.read_csv(file_path, 
                                 sep='\t',
                                 names=['DateTime', 'Open', 'High', 'Low', 'Close', 'Volume'],
                                 parse_dates=['DateTime'])
        
        # If we still don't have proper data, try a space-delimited format
        if len(df.columns) <= 2 or 'Open' not in df.columns:
            df = pd.read_csv(file_path, sep='\s+', parse_dates=True)
            
            # And with explicit column names if needed
            if len(df.columns) <= 2 or 'Open' not in df.columns:
                df = pd.read_csv(file_path,
                                 sep='\s+',
                                 names=['DateTime', 'Open', 'High', 'Low', 'Close', 'Volume'],
                                 parse_dates=['DateTime'])
        
        # Set the DateTime column as the index if it exists
        if 'DateTime' in df.columns:
            df.set_index('DateTime', inplace=True)
            
        # Convert numeric columns to appropriate data types
        numeric_columns = ['Open', 'High', 'Low', 'Close', 'Volume']
        for col in numeric_columns:
            if col in df.columns:
                df[col] = pd.to_numeric(df[col], errors='coerce')
        
        return df
    
    except Exception as e:
        print(f"Error importing data: {e}")
        print("If the format is non-standard, you may need to modify the script.")
        return None

def main():
    # Example usage
    file_path = input("Enter the path to your NQ futures data file: ")
    df = import_nq_futures_data(file_path)
    
    if df is not None:
        print("\nData imported successfully!")
        print("\nData summary:")
        print(f"Total records: {len(df)}")
        print(f"Date range: {df.index.min()} to {df.index.max()}")
        print("\nFirst 5 rows:")
        print(df.head())
        
        # Sample analysis
        print("\nDaily statistics:")
        daily_stats = df.resample('D').agg({
            'Open': 'first',
            'High': 'max',
            'Low': 'min',
            'Close': 'last',
            'Volume': 'sum'
        })
        print(daily_stats.head())
        
        # Save to CSV option
        save_option = input("\nDo you want to save the processed data to a CSV file? (y/n): ")
        if save_option.lower() == 'y':
            output_path = input("Enter the output file path (or press Enter for 'processed_nq_data.csv'): ")
            if not output_path:
                output_path = 'processed_nq_data.csv'
            df.to_csv(output_path)
            print(f"Data saved to {output_path}")

if __name__ == "__main__":
    main()