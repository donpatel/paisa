import pandas as pd
import os

filename = "NQ_1_Minute_1month.txt"

def import_nq_futures_data(file_path):
    """
    Import 1-minute /NQ futures data from a text file with specific format:
    Date,Time,Open,High,Low,Close,Volume,9SMA,21SMA,200SMA
    
    Args:
        file_path (str): Path to the text file containing the NQ futures data
        
    Returns:
        pandas.DataFrame: DataFrame containing the parsed futures data
    """
    # Check if file exists
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"The file {file_path} does not exist.")
    
    try:
        # Read CSV with expected format
        df = pd.read_csv(file_path)
        
        # Combine Date and Time columns to create DateTime
        df['DateTime'] = pd.to_datetime(df['Date'] + ' ' + df['Time'])
        
        # Drop original Date and Time columns
        df.drop(['Date', 'Time'], axis=1, inplace=True)
        
        # Set the DateTime column as the index
        df.set_index('DateTime', inplace=True)
        
        # Convert numeric columns to appropriate data types
        numeric_columns = ['Open', 'High', 'Low', 'Close', 'Volume', '9SMA', '21SMA', '200SMA']
        for col in numeric_columns:
            if col in df.columns:
                df[col] = pd.to_numeric(df[col], errors='coerce')
        
        return df
    
    except Exception as e:
        print(f"Error importing data: {e}")
        print("Please ensure the file is in the expected format:")
        print("Date,Time,Open,High,Low,Close,Volume,9SMA,21SMA,200SMA")
        return None

def main():
    # Hardcoded file path to be in the same folder as the script
    file_path = os.path.join(os.path.dirname(__file__), filename)
    
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

if __name__ == "__main__":
    main()