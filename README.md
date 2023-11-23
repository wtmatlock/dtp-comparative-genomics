# Comparative genomics practical

## Downloading the dataset
First, we want to download our dataset:
```
wget https://github.com/wtmatlock/dtp-comparative-genomics/archive/main.zip
unzip main.zip
```
I originally downloaded these sequences from [NCBI](https://www.ncbi.nlm.nih.gov), which is a database of biological data, including genome sequences. Each sequence in the `ecoli` and `mtb` directories is the complete chromosome from an *E. coli* and *M. tuberculosis* genome, respectively. The file names are their *accessions* e.g. `NZ_CP007391.1`, which is a unique identifier given by NCBI. If we want, we can [search for them on NCBI](https://www.ncbi.nlm.nih.gov/search/all/?term=NZ_CP007391.1). Each sequence is in the [FASTA](https://en.wikipedia.org/wiki/FASTA_format) format. What are required features of a FASTA file?
 
## Annotating sequences with Prokka

Now, we want to annotate our chromosomes. Whenever running a new software tool, it is crucial to understand the parameters, to make sure you're running it correctly, and the version, so you can cite it properly. For Prokka, we can run
```
prokka --help
```
Take some time to familiarise yourself with the syntax. For most tools, you use *flags*, terms with a double dash `--` before, to specify your parameters. To compliment the `--help` menu, it is important to [check the documentation](https://github.com/tseemann/prokka). Run Prokka first, then have a read whilst it's running:
```
cd ./sequences/mtb
for sample in ./*.fasta; do prokka --outdir "$sample"_prokka --prefix "$sample" --genus Mycobacterium --species tuberculosis $sample; done
cd ..
cd ./ecoli
for sample in ./*.fasta; do prokka --outdir "$sample"_prokka --prefix "$sample" --genus Escherichia --species coli $sample; done
cd ..
```
Make sure you understand the syntax of the Bash for loop: What is the variable? What is the range? Also, have a look in one of the Prokka output directories: What is the format and purpose of each output file? In particular, look at the information contained in the [GFF](https://en.wikipedia.org/wiki/General_feature_format) files. Try using the `cat` and `head` commands to explore the outputs. Can you find the length (bp) of each sequence?

## Pangenome analysis with Panaroo
We will now explore the pangenomes of our samples. Again, please read the [documentation](https://github.com/gtonkinhill/panaroo) whilst the tool is running.
```
panaroo --help
cd ./mtb
panaroo --input ./*_prokka/*.gff --out_dir mtb_panaroo_output --clean-mode strict
cd ..
cd ./ecoli
panaroo --input ./*_prokka/*.gff --out_dir ecoli_panaroo_output --clean-mode strict
cd ..
```
Again, take some time to explore the outputs. In particular, how do the `summary_statistics.txt` files compare between the *E. coli* and *M. tuberculosis* samples? Have a look at the Python script `accumulation.py`. What is it doing? Try running it with
```
python accumulation.py ./mtb/mtb_panaroo_output/gene_presence_absence.Rtab
python accumulation.py ./ecoli/ecoli_panaroo_output/gene_presence_absence.Rtab
```
How do the two plots compare? How could we improve this script?

## Comparing chromosomes in two ways
We are now going to test two approaches for sequence comparison. The first is based on our results from above, and will use the overlap of annotated genes between our sequences. The second will use an annotation-free technique based on the sharing of [*k*-mers](https://en.wikipedia.org/wiki/K-mer) between our sequences, using a tool called [Mash](https://github.com/marbl/Mash). To begin, we will run a script to plot the [Jaccard index](https://en.wikipedia.org/wiki/Jaccard_index) of genes as a heatmap:
```
python plotGenes.py ./mtb/mtb_panaroo_output/gene_presence_absence.Rtab
python plotGenes.py ./ecoli/ecoli_panaroo_output/gene_presence_absence.Rtab
```
Before you view the plots, what would you expect to see based on accumulation plots from before? After looking, how do the plots compare? Why did we use the Jaccard index instead of just the total number of genes shared? Next, we will use Mash to plot the (estimated) Jaccard index of *k*-mers:
```
mash --help
mash triangle
cd ./mtb
cat *.fasta > mtb_samples.fasta
mash triangle -E ./mtb_samples.fasta > ./mtb_mash.tsv
cd ..
cd ./ecoli
cat *.fasta > ecoli_samples.fasta
mash triangle -E ./ecoli_samples.fasta > ./ecoli_mash.tsv
cd ..
python plotMash.py ./mtb/mtb_mash.tsv
python plotMash.py ./ecoli/ecoli_mash.tsv
```
Open all four plots at once. How does each approach differ within and between samples? What were the main differences between the approaches? Why might your prefer the use of one over the other?

## Extra work: classifying *E. coli* sequences
The ways we have analysed our *E. ecoli* chromosomes above are often incoportated alongside other classification techniques. These techniques offer more coarse-grained resolution than the gene and *k*-mer sharing analysis we have just peformed. Have a look at the two tools below, explore their parameters, and try running them on our *E. coli* sample.
- [Multilocus sequence typing](https://en.wikipedia.org/wiki/Multilocus_sequence_typing) with [mlst](https://github.com/tseemann/mlst)
- [Phylotyping](https://ami-journals.onlinelibrary.wiley.com/doi/10.1111/1758-2229.12019) (*in silico*) with [EzClermont](https://github.com/nickp60/EzClermont)

Why might you want to give the results of these tools in an analysis?

## Extra extra work: antimicrobial resistance genes in *E. coli*
Put simply, bacterial antimicrobial resistance (AMR) describes when an isolate is no longer sensitive to antimicrobials. For *E. coli*, this is often due to the acquistion of certain genes that confer a resistant phenotype. To annotate for these genes, specific tools and databases are often employed. Try using [ABRicate](https://github.com/tseemann/abricate) to predict the resistance phyotypes of our *E. coli* chromosomes. What database is ABRicate using and why? Why might this analysis not give the full picture of AMR in our isolates?
