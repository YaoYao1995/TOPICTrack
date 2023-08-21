time_now=$(date +%Y-%m-%d_%H-%M-%S)
echo $time_now
exp=$time_now+best_paper_ablations

# 指定要删除的文件夹列表
folder_list=(
  "cache/embeddings/dancetrack*"
  "cache/det_bytetrack_dance_model.pkl"
  # "results/trackers/DANCE-val/${exp}_post"
  # "results/trackers/DANCE-val/${exp}"
)

# 遍历文件夹列表
for folder_path in "${folder_list[@]}"; do
  rm -rf $folder_path
done


python3 main.py --exp_name $exp --post --cmc_off --da_off --aw_off --grid_off --new_kf_off --dataset dance --aspect_ratio_thresh 1000 --w_assoc_emb 1.25 --aw_param 1

python3 external/TrackEval/scripts/run_mot_challenge.py \
  --SPLIT_TO_EVAL val \
  --METRICS HOTA Identity CLEAR \
  --TRACKERS_TO_EVAL ${exp}_post \
  --GT_FOLDER results/gt/ \
  --TRACKERS_FOLDER results/trackers/ \
  --BENCHMARK DANCE
