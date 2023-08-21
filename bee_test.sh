
exp=bee_test_M
# 指定要删除的文件夹列表
folder_list=(
  "cache/embeddings/BEE*"
  "cache/det_bee.pkl"
  "results/trackers/BEE-val/${exp}_post"
  "results/trackers/BEE-val/${exp}"
)

# 遍历文件夹列表
for folder_path in "${folder_list[@]}"; do
  rm -rf $folder_path
done

# iou_thresh 
python3 main.py --exp_name $exp --post \
  --alpha_gate 0.9 --gate 0.099 --gate2 0.3 --alpha_fixed_emb 0.95 --iou_thresh 0.2 \
  --track_thresh 0.6 \
  --cmc_off --da_off --aw_off --grid_off --new_kf_off \
  --dataset bee \
  --metric coine \
  --aspect_ratio_thresh 1.6 --w_assoc_emb 0.7

python3 external/TrackEval/scripts/run_mot_challenge.py \
  --SPLIT_TO_EVAL val \
  --METRICS HOTA Identity CLEAR \
  --TRACKERS_TO_EVAL ${exp} \
  --GT_FOLDER results/gt/ \
  --TRACKERS_FOLDER results/trackers/ \
  --BENCHMARK BEE

python3 external/TrackEval/scripts/run_mot_challenge.py \
  --SPLIT_TO_EVAL val \
  --METRICS HOTA Identity CLEAR \
  --TRACKERS_TO_EVAL ${exp}_post \
  --GT_FOLDER results/gt/ \
  --TRACKERS_FOLDER results/trackers/ \
  --BENCHMARK BEE