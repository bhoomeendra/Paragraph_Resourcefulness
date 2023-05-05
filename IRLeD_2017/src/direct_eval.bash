#!/bin/bash

echo "Document Level:"
../../trec_eval/trec_eval -m recall.100 -m P.10 -m map -m recip_rank ../data/raw/trec_ground_truth ../data/query_results/jud_level
echo -e "\n\nParagraph Level Mean:"
../../trec_eval/trec_eval -m recall.100 -m P.10 -m map -m recip_rank ../data/raw/trec_ground_truth ../data/query_results/para_level_mean
echo -e "\n\nParagraph Level Fix:"
../../trec_eval/trec_eval -m recall.100 -m P.10 -m map -m recip_rank ../data/raw/trec_ground_truth ../data/query_results/para_level_fix
echo -e "\n\nParagraph Level Dynamic:"
../../trec_eval/trec_eval -m recall.100 -m P.10 -m map -m recip_rank ../data/raw/trec_ground_truth ../data/query_results/para_level_per
echo -e "\n\nParagraph Level Hybrid:"
../../trec_eval/trec_eval -m recall.100 -m P.10 -m map -m recip_rank ../data/raw/trec_ground_truth ../data/query_results/para_level_hybrid
