#!/bin/bash
# Parameters are trec_eval -q output files.

if [ $# -ne 2 ]; then
    echo "Usage: $0 <eval-file1> <eval-file2>"
    echo "eval files: per-query evaluation result given by trec_eval"
    exit
fi

file1=$1
file2=$2
outfile=t-tests.r

### +++ FOR ndcg_cut_5
echo -n "v1 = c(" > t-tests.r
awk '/^ndcg_cut_5[ 	]/{if ($2 != "all") printf("%s, ", $3);}' $file1 | \
    sed 's/, $//' >> t-tests.r
echo -e ");\n\n" >> t-tests.r


echo -n "v2 = c(" >> t-tests.r
awk '/^ndcg_cut_5[	 ]/{if ($2 != "all") printf("%s, ", $3);}' $file2 | \
    sed 's/, $//' >> t-tests.r
echo -e ");\n\n" >> t-tests.r

cat >> t-tests.r <<EOF

m1 = mean(v1);
m2 = mean(v2);
x = t.test(v1, v2, paired=T);

output = sprintf("ndcg_cut_5\tMean1 = %6.4f\tMean2 = %6.4f\tdf = %d\tp-value = %.6f (%s)",
                 m1, m2, 
                 x[["parameter"]][["df"]], x[["p.value"]], x[["alternative"]]);

write.table(output, stdout(), 
  quote = FALSE, row.name = FALSE, col.names = FALSE);
EOF

R --no-save --slave < t-tests.r

rm -rf t-tests.r

### --- FOR ndcg_cut_5

### +++ FOR P_5

echo -n "v1 = c(" > t-tests.r
awk '/^P_5[ 	]/{if ($2 != "all") printf("%s, ", $3);}' $file1 | \
    sed 's/, $//' >> t-tests.r
echo -e ");\n\n" >> t-tests.r


echo -n "v2 = c(" >> t-tests.r
awk '/^P_5[	 ]/{if ($2 != "all") printf("%s, ", $3);}' $file2 | \
    sed 's/, $//' >> t-tests.r
echo -e ");\n\n" >> t-tests.r

cat >> t-tests.r <<EOF

m1 = mean(v1);
m2 = mean(v2);
x = t.test(v1, v2, paired=T);

output = sprintf("P_5\tMean1 = %6.4f\tMean2 = %6.4f\tdf = %d\tp-value = %.6f (%s)",
                 m1, m2, 
                 x[["parameter"]][["df"]], x[["p.value"]], x[["alternative"]]);

write.table(output, stdout(), 
  quote = FALSE, row.name = FALSE, col.names = FALSE);
EOF

R --no-save --slave < t-tests.r

rm -rf t-tests.r
### --- FOR P_5

### +++ FOR recip_rank

echo -n "v1 = c(" > t-tests.r
awk '/^recip_rank[ 	]/{if ($2 != "all") printf("%s, ", $3);}' $file1 | \
    sed 's/, $//' >> t-tests.r
echo -e ");\n\n" >> t-tests.r


echo -n "v2 = c(" >> t-tests.r
awk '/^recip_rank[	 ]/{if ($2 != "all") printf("%s, ", $3);}' $file2 | \
    sed 's/, $//' >> t-tests.r
echo -e ");\n\n" >> t-tests.r

cat >> t-tests.r <<EOF
m1 = mean(v1);
m2 = mean(v2);
x = t.test(v1, v2, paired=T);

output = sprintf("recip_rank\tMean1 = %6.4f\tMean2 = %6.4f\tdf = %d\tp-value = %.6f (%s)",
                 m1, m2, 
                 x[["parameter"]][["df"]], x[["p.value"]], x[["alternative"]]);

write.table(output, stdout(), 
  quote = FALSE, row.name = FALSE, col.names = FALSE);
EOF

R --no-save --slave < t-tests.r
#
#                 m1, m2,  x['p.value'], x['alternative']);
rm -rf t-tests.r
### --- FOR recip_rank
