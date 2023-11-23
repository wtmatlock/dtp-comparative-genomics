import sys
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

def create_jaccard_heatmap_from_tsv(tsv_file, output_file):
    # Read the TSV file into a DataFrame
    df = pd.read_csv(tsv_file, sep='\t', index_col='Gene')

    # Transpose the DataFrame to have genes as columns and samples as rows
    df = df.T

    # Sort rows and columns alphabetically by gene name
    df = df.sort_index(axis=0).sort_index(axis=1)

    # Calculate the Jaccard index matrix
    jaccard_matrix = pd.DataFrame(index=df.index, columns=df.index, dtype=float)
    
    for gene1 in df.index:
        for gene2 in df.index:
            if gene1 != gene2:
                intersection = sum(df.loc[gene1] & df.loc[gene2])
                union = sum(df.loc[gene1] | df.loc[gene2])
                jaccard_index = intersection / union if union > 0 else 0.0
                jaccard_matrix.at[gene1, gene2] = jaccard_index
    
    # Set diagonal entries to 1
    np.fill_diagonal(jaccard_matrix.values, 1.0)

    # Create a heatmap using Matplotlib
    plt.figure(figsize=(10, 8))
    plt.imshow(jaccard_matrix, cmap='viridis', interpolation='nearest')
    plt.xticks(range(len(df.index)), df.index, rotation=45, ha='right')
    plt.yticks(range(len(df.index)), df.index)
    plt.colorbar(label='Similarity')
    plt.title('Gene Jaccard index heatmap')
    plt.xlabel('Chromosome accession')
    plt.ylabel('Chromosome accession')

    # Save or display the heatmap
    if output_file:
        plt.savefig(output_file)
    else:
        plt.show()

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python script.py input.tsv")
        sys.exit(1)

    input_file = sys.argv[1]

    # Output file name (set to None if you want to display the plot instead of saving it)
    output_filename = f"{input_file}_heatmap_plot.png"

    # Create and display the Jaccard index heatmap
    create_jaccard_heatmap_from_tsv(input_file, output_filename)
