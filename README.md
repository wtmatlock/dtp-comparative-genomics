# Comparative genomics practical 2023

The aim of this practical is to compare the chromosomes of 10 *Escherichia coli* isolates and 10 *Mycobacterium tuberculosis* isolates. We will be using most of the techniques covered in the lecture this morning. By the end, you should have a better grasp of how these tools work, as well as a deeper understanding of the biology of our case study species. Both of these organisms are some of the most ubiquitous human pathogens, with *E. coli* the leading cause of many common human infections, and tuberculosis killing more people annually than HIV/AIDs or malaria. The steps we will work through today are very similar to those carried out by clinical microbiologists when characterising bacterial pathogens.

## Downloading the dataset
First, we want to download our dataset:
```
wget https://github.com/wtmatlock/dtp-comparative-genomics/archive/main.zip
unzip main.zip
```
I originally downloaded these sequences from [NCBI](https://www.ncbi.nlm.nih.gov), which is a database of biological data, including genome sequences. Each sequence in the `ecoli` and `mtb` directories is the complete chromosome from an *E. coli* and *M. tuberculosis* genome, respectively. The files are all in the [FASTA](https://en.wikipedia.org/wiki/FASTA_format) format. 
- What does FASTA stand for?
- What are the features of a FASTA file?
- What is the purpose of the header line?
- Can a FASTA file contain multiple sequences? If yes, how?

The file names are their *accessions* e.g. `NZ_CP007391.1`, which is a unique identifier given by NCBI. If we want, we can [search for them on NCBI](https://www.ncbi.nlm.nih.gov/search/all/?term=NZ_CP007391.1). Try searching for each *E. coli* accession in NCBI.
- What is the difference between an assembly, nucleotide, and genome accession?
- Can you find the (i) country, (ii) submission date, and (iii) original study associated with each sequence?
- Do you the submission date is the same as the isolation data? Why might this pose problems for future studies?

> All of the software you need for this practical should be pre-installed on your laptop.
 
## Annotating sequences with Prokka

Now, we want to [annotate](https://en.wikipedia.org/wiki/DNA_annotation) our chromosomes. Whenever running a new software tool, it is crucial to understand the parameters, to make sure you're running it correctly, and the version, so you can cite it properly. For Prokka, we can run
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
- Make sure you understand the syntax of the Bash for loop. What is the variable? What is the range?
- Have a look in one of the Prokka output directories. What is the format and purpose of each output file?
- In particular, look at the information contained in the [GFF](https://en.wikipedia.org/wiki/General_feature_format) files. Try using the `cat` and `head` commands to explore the outputs.
- Can you find the length (bp) of each sequence?
- Try exploring the annotations in [UniProt](https://www.uniprot.org). For example, the recF annotation in `NZ_CP041844.1` seems to control [DNA replication and repair](https://www.uniprot.org/uniprotkb/P0A7H0/entry).

## Pangenome analysis with Panaroo
We will now explore the [pangenomes](https://en.wikipedia.org/wiki/Pan-genome) of our samples. Please read the [documentation](https://github.com/gtonkinhill/panaroo) whilst the tool is running.
```
panaroo --help
cd ./mtb
panaroo --input ./*_prokka/*.gff --out_dir mtb_panaroo_output --clean-mode strict
cd ..
cd ./ecoli
panaroo --input ./*_prokka/*.gff --out_dir ecoli_panaroo_output --clean-mode strict
cd ..
```
Take some time to explore the outputs. In particular, how do the `summary_statistics.txt` files compare between the *E. coli* and *M. tuberculosis* samples? Have a look at the Python script `accumulation.py`. What is it doing? Try running it with
```
python accumulation.py ./mtb/mtb_panaroo_output/gene_presence_absence.Rtab
python accumulation.py ./ecoli/ecoli_panaroo_output/gene_presence_absence.Rtab
```
- How do the two plots compare? 
- How could we improve this script?

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
Open all four plots at once. 
- How does each approach differ within and between samples?
- What were the main differences between the approaches?
- Why might your prefer the use of one over the other?
- What happens when you increase the Mash sketch size?

## Classifying *E. coli* sequences
The ways we have analysed our *E. coli* chromosomes above are often incoportated alongside other classification techniques. These techniques offer more coarse-grained resolution than the gene and *k*-mer sharing analysis we have just peformed. Have a look at the two tools below, explore their parameters, and try running them on our *E. coli* sample:

- [Multilocus sequence typing](https://en.wikipedia.org/wiki/Multilocus_sequence_typing) with [mlst](https://github.com/tseemann/mlst)
- [Phylotyping](https://ami-journals.onlinelibrary.wiley.com/doi/10.1111/1758-2229.12019) (*in silico*) with [EzClermont](https://github.com/nickp60/EzClermont)

> Running these new tools is no different syntactically to running those above. Take some time to read the documentation if you get stuck.

- What is MLST, and what is its primary purpose in molecular biology and epidemiology?
- Explain the concept of *loci* in the context of MLST. How are loci used in MLST analysis?
- What is the significance of allele numbers in MLST analysis, and how are they assigned to different sequences?
- Describe the process of sequence typing using MLST. How does it contribute to the characterization of bacterial strains?
- What is phylotyping, and how does it contribute to the study of microbial diversity and evolution?
- How is phylotyping traditionally carried out with PCR?
- Explain the term *in silico* in the context of phylotyping. How does *in silico* phylotyping differ from traditional PCR-based methods?
- Why might you want to give the results of these tools in an analysis?
- How do they compare with our heatmaps?

## Antimicrobial resistance genes in *E. coli*
Put simply, bacterial antimicrobial resistance (AMR) describes when an isolate is no longer sensitive to antimicrobials. For *E. coli*, this is often due to the acquistion of certain genes that confer a resistant phenotype. To annotate for these genes, specific tools and databases are often employed. Try using [ABRicate](https://github.com/tseemann/abricate) to predict the resistance phenotypes of our *E. coli* chromosomes. 
> **Hint:** Once you have found a command that words, you can follow it with `> ecoli_abricate.tsv` to write the output to a file in your present working directory.
- What database is ABRicate using and why?
- Why might this analysis not give the full picture of AMR in our isolates?
- How do the annotations (and predicited resistance phenotypes) vary across the sample? Which are common? Which are rare?
- How can we use the ABRicate output to examine the quality of the annotations?
ABRicate comes pre-installed with other specialised databases. Try running ABRicate with another database. We can then combine outputs as follows:
```
abricate --summary ecoli_abricate_1.tsv ecoli_abricate_2.tsv > ecoli_abricate_combined.tsv
```
- Why might it be useful to annotate with multiple, potentially similar, databases?
