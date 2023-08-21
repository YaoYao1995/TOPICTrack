exp=mot17_val_ablation_new

folder_list=(
      "cache/embeddings/MOT17*"
      "cache/det_bytetrack_ablation.pkl"
      "results/trackers/MOT17-val/${exp}_post"
      "results/trackers/MOT17-val/${exp}"
    )

# 遍历文件夹列表
for folder_path in "${folder_list[@]}"; do
    rm -rf $folder_path
done
# Flags to disable all the new changes
python3 main.py --exp_name $exp --post --alpha_gate 0.3 --gate 0.3  --cmc_off --da_off --aw_off --grid_off --new_kf_off --dataset mot17 --w_assoc_emb 0.75 --aw_param 0.5

python3 external/TrackEval/scripts/run_mot_challenge.py \
    --SPLIT_TO_EVAL val \
    --METRICS HOTA Identity CLEAR \
    --TRACKERS_TO_EVAL ${exp} \
    --GT_FOLDER results/gt/ \
    --TRACKERS_FOLDER results/trackers/ \
    --BENCHMARK MOT17

python3 external/TrackEval/scripts/run_mot_challenge.py \
    --SPLIT_TO_EVAL val \
    --METRICS HOTA Identity CLEAR \
    --TRACKERS_TO_EVAL ${exp}_post \
    --GT_FOLDER results/gt/ \
    --TRACKERS_FOLDER results/trackers/ \
    --BENCHMARK MOT17