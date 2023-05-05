for i in $(seq 0.01 0.01 0.20)
do
    python ranking.py 3 $i
    python trec_format.py 3
    echo -e "\n\nParagraph Level Dynamic: $i"
    ../../trec_eval/trec_eval -m recall.100 -m P.10 -m map -m recip_rank ../data/raw/trec_ground_truth ../data/query_results/para_level_per
done
