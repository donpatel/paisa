import pandas as pd
import os

if __name__ == "__main__":
    folder = "C:\\Users\\Don\\OneDrive\\Documents\\Code\\paisa\\paisa\\data"  # Replace with your folder path
    filename = "NQ_1_Minute_1month.txt"  # Replace with your file name
    
    # Create full file path
    filepath = os.path.join(folder, filename)
    
    try:
        df = pd.read_csv(filepath)
        print(f"Imported DataFrame with shape: {df.shape}")
        print("\nFirst few rows:")
        print(df.head())
        print("\nColumn names:")
        print(df.columns.tolist())
        print("\nData types:")
        print(df.dtypes)
        
    except FileNotFoundError:
        print(f"File '{filename}' not found in folder '{folder}'.")
    except Exception as e:
        print(f"Error reading file: {e}")