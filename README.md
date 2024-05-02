<<<<<<< HEAD
# RADA

The RADA model is a rapid antibody generation and screening model for antigens


#### Preparation
```bash
mkdir data/0_antigen_pdb
ANTIGEN=HER2
### put in antigen structure pdb file and info.txt
```


#### Antibody sequence generation
```bash
mkdir data/1_sequence_generate
mkdir data/2_ab_structure
python rada/hern_generate.py -i data/0_antigen_pdb/info.xlsx -o data/1_sequence_generate/output.txt
python rada/hern_after_process_data.py -i data/1_sequence_generate/output.txt -o data/1_sequence_generate/data_refine.txt
python rada/hern_assemble.py -i data/1_sequence_generate/data_refine.txt -o data/2_ab_structure/input.csv
```

#### Antibody structure prediction
```bash
python rada/igfold_run.py -i data/2_ab_structure/input.csv
mkdir data/2_ab_structure/ab_structure && mv *.pdb data/2_ab_structure/ab_structure
mkdir data/2_ab_structure/ab_fasta && mv *.fasta data/2_ab_structure/ab_fasta
mkdir data/2_ab_structure/ab_structure_renum
python rada/igfold_renum.py -i data/2_ab_structure/ab_structure -o data/2_ab_structure/ab_structure_renum
python rada/igfold_rmsd_all.py -i data/2_ab_structure/ab_structure_renum -o data/2_ab_structure/rmsd.csv
```

#### Antibody-antigen docking

```bash
####zdock
mkdir data/3_zdock
cp zdock/uniCHARMM ./
cp zdock/create_lig ./
mkdir data/3_zdock/antibody_m
mkdir data/3_zdock/out
mkdir data/3_zdock/out_1
mkdir data/3_zdock/pdb
rada/zdock/mark_sur data/0_antigen_pdb/$ANTIGEN.pdb data/3_zdock/$ANTIGEN_m.pdb
for i in `ls data/2_ab_structure/ab_structure_renum/` ; do zdock/mark_sur data/2_ab_structure/ab_structure_renum/$i data/3_zdock/antibody_m/$i;done
python rada/zdock.py -i data/3_zdock/antibody_m/ -a data/3_zdock/${ANTIGEN}_m.pdb -o data/3_zdock/out/
for i in `ls data/3_zdock/out`;do 
head -n 6 data/3_zdock/out/$i >  data/3_zdock/out_1/${i%%.*}.out
rada/zdock/create.pl data/3_zdock/out_1/${i%%.*}.out -O out
mv complex.1.pdb data/3_zdock/pdb/${i%%.*}.pdb
done
python rada/zdock_score.py -i data/3_zdock/out -o data/3_zdock/zdock_scores.csv
done
```



```bash
####hdock
mkdir data/3_hdock
mkdir data/3_hdock/out
mkdir data/3_hdock/pdb

python rada/hdock.py -i data/2_ab_structure/ab_structure_renum/ -a data/0_antigen_pdb/$ANTIGEN.pdb -o data/3_hdock/out/
cd data/3_hdock/out/
for i in `ls`
do
rada/hdock/createpl $i complex.pdb -nmax 1 -complex -models
mv model_1.pdb ../pdb/${i%%.*}.pdb
done 
cd ../../../
python rada/hdock_score.py -i /data/3_hdock/out -o data/3_hdock/hdock_scores.csv
```

#### Calculate binding energy and output the final result
```bash
python rada/prodigy.py -i data/3_zdock/pdb -o data/4_binding_affinity/zdock_result.csv
python rada/prodigy.py -i data/3_hdock/pdb -o data/4_binding_affinity/hdock_result.csv
cp data/2_ab_structure/input.csv data/4_binding_affinity/input.csv
python rada/result_merge.py -z data/4_binding_affinity/zdock_result.csv -d data/4_binding_affinity/hdock_result.csv -i data/4_binding_affinity/input.csv -o data/4_binding_affinity/merged_results.csv
python rada/final_output.py -f data/4_binding_affinity/merged_results.csv -n 5 -o data/4_binding_affinity/filtered_n_results.csv
python rada/final_output.py -f data/4_binding_affinity/merged_results.csv -g -9 -o data/4_binding_affinity/filtered_g_results.csv
```

