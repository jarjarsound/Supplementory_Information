import sys
import pandas as pd
import os

def summarize_phage_contigs(sample_id_list_path):
    summary_data = []

    # Read sample IDs from the provided text file
    with open(sample_id_list_path, 'r') as file:
        sample_ids = [line.strip() for line in file]

    for sample_id in sample_ids:
        csv_path = f"{sample_id}/out/phamer_prediction.csv"
        
        if not os.path.exists(csv_path):
            print(f"File not found: {csv_path}")
            continue

        # Read the CSV file
        df = pd.read_csv(csv_path)

        # Filter out rows marked as "filtered"
        filtered_df = df[df['Pred'] != 'filtered']

        # Calculate TotalFilteredContigs
        total_filtered_contigs = len(filtered_df)

        # Calculate Phage%
        phage_count = len(filtered_df[filtered_df['Pred'] == 'phage'])
        phage_percentage = (phage_count / total_filtered_contigs) * 100 if total_filtered_contigs > 0 else 0

        # Append to summary data
        summary_data.append([sample_id, total_filtered_contigs, phage_percentage])

    # Convert summary data to a DataFrame
    summary_df = pd.DataFrame(summary_data, columns=['SampleID', 'TotalFilteredContigs', 'Phage%'])

    # Save the summary to a CSV file
    summary_df.to_csv('summary_phage_contigs.csv', index=False)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python script.py <path_to_sample_id_list.txt>")
    else:
        summarize_phage_contigs(sys.argv[1])
