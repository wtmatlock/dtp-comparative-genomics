# Comparative genomics tutorial

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

## Clustering chromosomes in two ways
- Mash similarity heatmap
- Gene overlap heatmap

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
```

## Extra work: classifying *E. coli* sequences

- mlst: https://github.com/tseemann/mlst
- ezclermont: https://github.com/nickp60/EzClermont
