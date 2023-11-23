import sys
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

def convert_distance(distance_str):
    try:
        a, b = map(int, distance_str.split('/'))
        return a / b
    except (ValueError, ZeroDivisionError):
        # Handle cases where the conversion or division fails
        return np.nan

def create_heatmap_from_csv(csv_file, output_file):
    # Read the CSV file into a DataFrame without headers
    df = pd.read_csv(csv_file, header=None, names=['seq1', 'seq2', 'distance', 'pval', 'hashes'], delimiter='\t')

    # Convert the "distance" column to numeric values
    df['hashes'] = df['hashes'].apply(convert_distance)

    # Create a set of unique sequences
    unique_seqs = set(df['seq1'].unique()) | set(df['seq2'].unique())

    # Create a mapping from sequence labels to integer indices
    seq_to_index = {seq: i for i, seq in enumerate(unique_seqs)}

    # Set the matrix size based on the number of unique sequences
    matrix_size = len(unique_seqs)

    # Create a matrix of distances
    similarity_matrix = np.zeros((matrix_size, matrix_size))
    for row in df.itertuples(index=False):
        index_seq1 = seq_to_index[row.seq1]
        index_seq2 = seq_to_index[row.seq2]
        similarity_matrix[index_seq1, index_seq2] = row.hashes
        similarity_matrix[index_seq2, index_seq1] = row.hashes  # Since it's a pairwise edge list

    # Set diagonal elements to 1.0
    np.fill_diagonal(similarity_matrix, 1.0)

    # Create a heatmap using Matplotlib
    plt.figure(figsize=(10, 8))
    plt.imshow(similarity_matrix, cmap='viridis', interpolation='nearest')
    plt.xticks(range(matrix_size), unique_seqs, rotation=45, ha='right')
    plt.yticks(range(matrix_size), unique_seqs)
    plt.colorbar(label='Similarity')
    plt.title('k-mer Jaccard index heatmap')
    plt.xlabel('Chromosome accession')
    plt.ylabel('Chromosome accession')

    # Save or display the heatmap
    if output_file:
        plt.savefig(output_file)
    else:
        plt.show()

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python script.py edgelist.tsv")
        sys.exit(1)

    input_file = sys.argv[1]

    # Output file name (set to None if you want to display the plot instead of saving it)
    output_filename = f"{input_file}_plot.png"

    # Create and display the heatmap
    create_heatmap_from_csv(input_file, output_filename)
