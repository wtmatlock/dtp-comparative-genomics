# Comparative genomics tutorial

## Annotating genomes with Prokka

Whenever running a new software tool, it is crucial to understand the parameters, to make sure you're running it correctly, and the version, so you can cite it properly. For Prokka, we can run
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
Make sure you understand the syntax of the Bash for loop: What is the variable? What is the range? Also, have a look in one of the Prokka output directories: What is the format and purpose of each output file? In particular, look at the information contained in the [GFF](https://www.ensembl.org/info/website/upload/gff.html) files. Try using the `cat` and `head` commands to explore the outputs.

## Pangenome analysis with Panaroo
[Documentation](https://github.com/gtonkinhill/panaroo).
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
