import sys
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from scipy.cluster.hierarchy import linkage, dendrogram

def convert_distance(distance_str):
    try:
        a, b = map(int, distance_str.split('/'))
        return a / b
    except (ValueError, ZeroDivisionError):
        return np.nan

def create_heatmap_with_dendrogram(csv_file, output_file):
    # Read the CSV file into a DataFrame without headers
    df = pd.read_csv(csv_file, header=None, names=['seq1', 'seq2', 'distance', 'pval', 'hashes'], delimiter='\t')

    # Convert the "distance" column to numeric values
    df['hashes'] = df['hashes'].apply(convert_distance)

    # Create a set of unique sequences
    unique_seqs = sorted(set(df['seq1'].unique()) | set(df['seq2'].unique()))

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
        similarity_matrix[index_seq2, index_seq1] = row.hashes  # Symmetric

    # Set diagonal elements to 1.0
    np.fill_diagonal(similarity_matrix, 1.0)

    # Perform hierarchical clustering on the similarity matrix
    condensed_distance = 1 - similarity_matrix[np.triu_indices(matrix_size, k=1)]
    linkage_matrix = linkage(condensed_distance, method='average')

    # Create the dendrogram without labels
    fig, ax = plt.subplots(1, 2, figsize=(15, 8), gridspec_kw={'width_ratios': [1, 3]})
    
    dendro = dendrogram(linkage_matrix, no_labels=True, orientation='left', ax=ax[0])
    reordered_indices = dendro['leaves']

    # Reverse the order of the leaves to flip the dendrogram vertically
    reordered_indices = reordered_indices[::-1]

    # Reorder the similarity matrix based on the dendrogram
    reordered_similarity_matrix = similarity_matrix[reordered_indices, :][:, reordered_indices]

    # Create the heatmap
    cax = ax[1].imshow(reordered_similarity_matrix, cmap='viridis', interpolation='nearest')
    ax[1].set_xticks(range(matrix_size))
    ax[1].set_xticklabels(np.array(unique_seqs)[reordered_indices], rotation=45, ha='right')
    ax[1].set_yticks(range(matrix_size))
    ax[1].set_yticklabels(np.array(unique_seqs)[reordered_indices])

    fig.colorbar(cax, ax=ax[1], label='Similarity')

    ax[0].set_title('Hierarchical Clustering')
    ax[1].set_title('k-mer Jaccard Index Heatmap')

    # Save or display the heatmap and dendrogram
    if output_file:
        plt.savefig(output_file, bbox_inches='tight')
    else:
        plt.show()

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python script.py edgelist.tsv")
        sys.exit(1)

    input_file = sys.argv[1]

    # Output file name (set to None if you want to display the plot instead of saving it)
    output_filename = f"{input_file}_heatmap_with_dendrogram.png"

    # Create and display the heatmap with dendrogram
    create_heatmap_with_dendrogram(input_file, output_filename)
