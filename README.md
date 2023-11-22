# Comparative Genomics

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
```
