import os.path
import numpy as np
import cv2

def sort_output(txt_path):
    with open(txt_path, 'r') as f:
        list = []
        for line in f:
            list.append(line.strip())

    with open(txt_path, "w") as f:
        for item in sorted(list, key=lambda x: int(str(x).split(',')[0])):
            f.writelines(item)
            f.writelines('\n')
        f.close()


def draw_mot(video_id,gt_path, save_dir):
    txt_name = gt_path + '/' + video_id + '.txt'  # txt文本内容
    file_path_img = 'data/MOT20/test/' + video_id + '/img1'  # img图片路径
    # 生成新的文件夹来存储画了bbox的图片
    if not os.path.exists(os.path.join(save_dir,video_id)):
        os.makedirs(os.path.join(save_dir,video_id),exist_ok=True)
        print('The %s/' % os.path.join(save_dir,video_id) + '  have create!')
    save_file_path = os.path.join(save_dir,video_id)
    sort_output(txt_name)  # 这是一个对txt文本结果排序的代码，key=frame，根据帧数排序

    source_file = open(txt_name)
    records = source_file.readlines()
    # 把frame存入列表img_names
    i = 0
    img_names = []
    for line in records:
        staff = line.split(',')
        img_name = staff[0]
        img_names.append(img_name)
        if i == 0:
            num = int(float(staff[1])) - 1
        i += 1

    # 将每个frame的bbox数目存入字典
    name_dict = {}
    for i in img_names:
        if img_names.count(i):
            name_dict[i] = img_names.count(i)
    # print(name_dict)
    # source_file.close()

    # source_file = open(txt_name)
    l =0
    for idx in name_dict:
        # print(str(idx).rjust(6, '0'))
        # 因为图片名称是000001格式的，所以需要str(idx).rjust(6, '0')进行填充
        print(os.path.join(file_path_img, str(idx).rjust(6, '0') + '.jpg'))
        img = cv2.imread(os.path.join(file_path_img, str(idx).rjust(6, '0') + '.jpg'))
        for i in range(name_dict[idx]):
            # line = source_file.readline()
            line = records[l]
            l+=1
            staff = line.split(',')
            # id = int(float(staff[1])) - num
            id = staff[1]
            cls = staff[7]
            box = staff[2:6]
            # print(id, box)
            # draw_bbox
            
            cv2.rectangle(img, (int(float(box[0])), int(float(box[1]))),
                        (int(float(box[0])) + int(float(box[2])), int(float(box[1])) + int(float(box[3]))),
                        (255, 255, 0), 2,cv2.LINE_4)
            cv2.rectangle(img, (int(float(box[0])), int(float(box[1]))),
                            ((int(float(box[0])) + 30), (int(float(box[1])) + 35)),
                            (255,255,0), thickness=-1)
            cv2.putText(img, str(int(float(id))), (int(float(box[0])), int(float(box[1]))+22),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 2, bottomLeftOrigin=False)
        img = cv2.resize(img,dsize=(1920,1080))
        # 保存图片
        cv2.imwrite(os.path.join(save_file_path, str(idx).rjust(6, '0') + '.png'), img)

    source_file.close()


if __name__ == '__main__':
    # gt_path = '/remote-home/zhengyiyao/OC_SORT/evaldata/trackers/mot_challenge/MOT17-test/mot20_test_ocsort_results/data'
    # gt_path = '/remote-home/zhengyiyao/topictrack/results/trackers/MOT20-val/baseline_mot20_test_beetrack/data'
    # gt_path = '/remote-home/zhengyiyao/ByteTrack/YOLOX_outputs/yolox_x_mix_mot20_ch/track_results'
    gt_path = '/remote-home/zhengyiyao/topictrack/results/trackers/MOT20-val/baseline_mot20_test/data'
    filename = os.listdir(gt_path)
    # print(filename)
    for name in filename:
        if "MOT20-06" not in name:
            continue
        print('The video ' + name.split('.')[0] + ' begin!')
        # draw_mot(name.split('.')[0],gt_path,save_dir="pic_track/mot20_ocsort/")
        draw_mot(name.split('.')[0],gt_path,save_dir="pic_track/mot20_fairmot/")
        print('The video ' + name.split('.')[0] + ' Done!')
