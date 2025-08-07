# -*- coding: utf-8 -*-
"""
author:     zhikang.zeng
time  :     2025-01-09 11:12
"""
import argparse
import os
import cv2
import imageio
import numpy as np
import matplotlib.pyplot as plt
import random

parser = argparse.ArgumentParser(description="Depth Render")
parser.add_argument('--img_dir', type=str, default=r'', help='render multiple frames of images')
parser.add_argument('--img_path', type=str, default=r'', help='render a single frame image')
parser.add_argument('--img_type', type=str, default=r'depth', help='optional: [depth, disp]')
parser.add_argument('--min_disp', type=float, default=2.0, help='min disp')
parser.add_argument('--max_disp', type=float, default=192.0, help='max disp')
parser.add_argument('--min_depth', type=float, default=0.0, help='min depth')
parser.add_argument('--max_depth', type=float, default=10000.0, help='max depth')
parser.add_argument('--save_dir', type=str, default=r'', help='directory to save results')
parser.add_argument('--save_gif', type=bool, default=False, help='save gif result')
parser.add_argument('--save_mp4', type=bool, default=False, help='save mp4 result')
parser.add_argument('--need_left_img', type=bool, default=False, help='gif image with left image')
parser.add_argument('--need_speckle_filter', type=bool, default=True, help='need speckle filter')
parser.add_argument('--need_value_show', type=bool, default=True, help='need value show')
args = parser.parse_args()

# args.img_dir = r'D:\3_HoBot\3_RDK_X3_X5\14_Stereo\render\stereonet_images_zed2i_1'
# args.img_dir = r'D:\3_HoBot\3_RDK_X3_X5\14_Stereo\render\stereonet_images_zed2i_2'
# args.img_dir = r'D:\3_HoBot\3_RDK_X3_X5\14_Stereo\render\stereonet_images_zed2i_3'
# args.img_dir = r'D:\3_HoBot\3_RDK_X3_X5\14_Stereo\render\stereonet_images_zed2i_4'
# args.img_dir = r'D:\3_HoBot\3_RDK_X3_X5\14_Stereo\render\stereonet_images_s316_1'
# args.img_dir = r'D:\3_HoBot\3_RDK_X3_X5\14_Stereo\render\stereonet_images_s316_2'
# args.img_dir = r'D:\3_HoBot\3_RDK_X3_X5\14_Stereo\render\view_rock_data'

# args.save_dir = os.path.split(args.img_dir)[0] + fr'\render_{args.img_type}_' + os.path.split(args.img_dir)[1]
# args.save_gif = True
# args.need_left_img = True
# args.img_dir = r'C:\StereoDataset\zed2i\zed2i-distance\20250220155025_38085162_NEURAL'
# args.img_dir = r'C:\StereoDataset\zed2i\zed2i-distance\20250220170229_38085162_NEURAL'
# args.img_dir = r'C:\StereoDataset\zed2i\zed2i-distance\20250220170917_38085162_NEURAL'
# args.img_dir = r'C:\StereoDataset\zed2i\zed2i-distance\20250220171321_38085162_NEURAL'
# args.img_dir = r'C:\StereoDataset\zed2i\zed2i-distance\20250220172241_38085162_NEURAL'
# args.img_dir = r'C:\StereoDataset\zed2i\zed2i-dataline\20250220172647_38085162_NEURAL'
# args.img_dir = r'C:\StereoDataset\zed2i\zed2i-dataline\20250220172913_38085162_NEURAL'
# args.img_dir = r'C:\StereoDataset\realsensed455\20250220_D455_215122252596_GT'
# args.img_dir = r'C:\StereoDataset\zed2i\zed2i-room\20250220174025_38085162_NEURAL'
# args.img_dir = r'C:\StereoDataset\realsensed455\20250220_D455_215122252596_room'
# args.img_dir = r'C:\StereoDataset\yg\room'
# args.img_dir = r'C:\StereoDataset\realsensed455\20250224145751_D455_215122252596'
# args.img_dir = r'C:\StereoDataset\realsensed455\20250225152258_D455_215122252596_createcity1'
# args.img_path = r'C:\StereoDataset\realsensed455\20250220_D455_215122252596_GT\001-20250220170512-ep-1-g-1-lp-1-depth.png'
# args.img_path = r'C:\StereoDataset\zed2i\zed2i-distance\20250220170229_38085162_NEURAL\000013_depth.pfm'
# args.img_path = r'C:\StereoDataset\yg\GT060cm\depth000069.png'
# args.img_path = r'C:\StereoDataset\yg\road\depth000257.png'

# args.img_path = r'C:\StereoDataset\yg\road\depth000833.png'
# args.img_path = r'C:\StereoDataset\realsensed455\20250224145751_D455_215122252596_road\534-20250224150157-ep-1-g-1-lp-1-depth.png'
# args.img_path = r'C:\StereoDataset\zed2i\zed2i-road\20250224145658_38085162_NEURAL\000797_depth.pfm'

# args.img_path = r'C:\StereoDataset\yg\createcity1\depth000833.png'
# args.img_path = r'C:\StereoDataset\realsensed455\20250225152258_D455_215122252596_createcity1\406-20250225153003-ep-1-g-1-lp-1-depth.png'
# args.img_path = r'C:\StereoDataset\zed2i\zed2i-createcity1\20250225151823_38085162_NEURAL\000985_depth.pfm'

# args.img_path = r'C:\StereoDataset\yg\room\depth001049.png'
# args.img_path = r'C:\StereoDataset\realsensed455\20250306213625_D455_215122252596_room2\171-20250306214101-ep-1-g-1-lp-1-depth.png'
# args.img_path = r'D:\zed2i-room2\20250306213713_38085162_NEURAL\001325_depth.pfm'
# args.img_path = r'C:\StereoDataset\distance\zed2i\20250312151655_38085162_NEURAL_min'
# args.img_dir = r'C:\StereoDataset\distance\realsense\20250312154803_D455_215122252596_50cm'
# root_dir = r'C:\StereoDataset\distance\zed2i'
# root_dir = r'C:\StereoDataset\distance\realsense'
# sub_dir = os.listdir(root_dir)
# args.img_dir = os.path.join(root_dir, sub_dir[4])
# args.img_dir = r'C:\StereoDataset\distance\yg\stereonet_images_300cm'
# args.img_dir = r'C:\StereoDataset\tree\Realsense\20250325165402_D455_215122252596'
# args.img_dir = r'C:\StereoDataset\tree\yx\tree'
# args.img_dir = r'C:\StereoDataset\pr\Realsense1'
# args.img_dir = r'C:\StereoDataset\pr\Realsense2'
# args.img_dir = r'C:\StereoDataset\pr\Realsense3'
# args.img_dir = r'C:\Users\zhikang.zeng\Downloads\Motorcycle-perfect'
# args.need_left_img = False
# args.img_type = 'disp'
# args.max_disp = 2000
# args.need_value_show = False
# if 'yg' in args.img_dir or 'yx' in args.img_dir or 'drobotics' in args.img_dir:
#     args.need_speckle_filter = True
# else:
#     args.need_speckle_filter = False
# args.save_dir = os.path.split(args.img_dir)[0] + fr'\render_{args.img_type}_' + os.path.split(args.img_dir)[1]
# # args.save_dir = os.path.split(args.img_path)[0] + fr'\..\render_{args.img_type}_' + os.path.split(os.path.split(args.img_path)[0])[1]
# args.save_gif = False
# args.save_mp4 = False
# args.max_depth = 20000

def is_cv16uc1(image):
    # 检查图像数据类型和通道数
    return image.dtype == np.uint16 and len(image.shape) == 2


def is_cv32fc1(image):
    # 检查图像数据类型和通道数
    return image.dtype == np.float32 and len(image.shape) == 2


if __name__ == '__main__':
    img_dir = args.img_dir
    img_path = args.img_path
    img_type = args.img_type
    min_disp = args.min_disp
    max_disp = args.max_disp
    min_depth = args.min_depth
    max_depth = args.max_depth
    save_dir = args.save_dir
    save_gif = args.save_gif
    save_mp4 = args.save_mp4
    need_left_img = args.need_left_img
    need_speckle_filter = args.need_speckle_filter
    need_value_show = args.need_value_show
    print('=> args: ')
    print(f'       img_dir: {img_dir}')
    print(f'       img_path: {img_path}')
    print(f'       img_type: {img_type}')
    print(f'       min_disp: {min_disp}')
    print(f'       max_disp: {max_disp}')
    print(f'       min_depth: {min_depth}')
    print(f'       max_depth: {max_depth}')
    print(f'       save_dir: {save_dir}')
    print(f'       save_gif: {save_gif}')
    print(f'       save_mp4: {save_mp4}')
    print(f'       need_left_img: {need_left_img}')
    print(f'       need_speckle_filter: {need_speckle_filter}')
    print(f'       need_value_show: {need_value_show}')
    try:
        assert img_type in ['depth', 'disp']
    except:
        print('=> img_type needs to be set to [depth, disp]')

    waitkey_time = 10
    if img_path != '':
        img_path_list = [img_path]
        # waitkey_time = 0
    elif img_dir != '':
        img_path_list = [os.path.join(img_dir, filename) for filename in os.listdir(img_dir) if
                         (img_type in filename and 'color' not in filename) or filename.endswith('.tiff')]
        # img_path_list = random.sample(img_path_list, 10)
    else:
        print('=> please enter image path!')
        exit(0)

    print(f'=> img count: {len(img_path_list)}')
    gif_frames = []
    for org_img_path in img_path_list:
        print('=============================================================')
        if not os.path.exists(org_img_path):
            print(f'=> {org_img_path} not exist')
            continue
        if not org_img_path.endswith(('.png', '.pfm', '.tiff')): continue
        # read img
        print(f'=> process {org_img_path}')
        org_img = cv2.imread(org_img_path, cv2.IMREAD_UNCHANGED)
        org_img[org_img == np.inf] = 0
        print(f'=> org_img [min, max]: [{org_img.min():.2f}, {org_img.max():.2f}]')

        # Limit the max and min values
        if img_type == 'disp':
            if not is_cv32fc1(org_img):
                print('=> disparity image format error!')
                continue
            org_img[org_img < min_disp] = 0
            org_img[org_img > max_depth] = 0
        if img_type == 'depth':
            # if not is_cv16uc1(org_img):
            #     print('=> depth image format error!')
            #     continue
            org_img[org_img < min_depth] = 0
            org_img[org_img > max_depth] = 0
        print(f'=> limit org_img [min, max]: [{org_img.min():.2f}, {org_img.max():.2f}]')

        # speckle filter
        if need_speckle_filter:
            norm_img = cv2.normalize(org_img, None, 0, 255, cv2.NORM_MINMAX, cv2.CV_8UC1)
            cv2.filterSpeckles(norm_img, newVal=0, maxSpeckleSize=10, maxDiff=3)
            _, mask = cv2.threshold(norm_img, 0, 1, cv2.THRESH_BINARY)
            org_img *= mask

        # sort data
        flattened_data = org_img.flatten()
        sorted_data = np.sort(flattened_data[flattened_data > 0])
        # calc percentile
        percentile1 = np.percentile(sorted_data, 10)
        percentile2 = np.percentile(sorted_data, 50)
        percentile3 = np.percentile(sorted_data, 90)
        print(f'=> percentile: [{percentile1:.2f}, {percentile2:.2f}, {percentile3:.2f}]')
        # split data
        values1 = flattened_data[flattened_data <= percentile1]
        values2 = flattened_data[(flattened_data > percentile1) & (flattened_data <= percentile2)]
        values3 = flattened_data[(flattened_data > percentile2) & (flattened_data <= percentile3)]
        values4 = flattened_data[flattened_data > percentile3]
        # norm data
        # Jet伪彩色映射（0到1范围）的颜色段：
        # 0.0 - 0.25：从深蓝色逐渐过渡到浅蓝色
        # 0.25 - 0.5：从浅蓝色逐渐过渡到青绿色
        # 0.5 - 0.75：从青绿色逐渐过渡到黄色
        # 0.75 - 1.0：从黄色逐渐过渡到红色
        values1_norm = (values1 - np.min(values1)) / (percentile1 - np.min(values1)) * 0.25
        values2_norm = 0.25 + (values2 - percentile1) / (percentile2 - percentile1) * 0.25
        values3_norm = 0.5 + (values3 - percentile2) / (percentile3 - percentile2) * 0.25
        values4_norm = 0.75 + (values4 - percentile3) / (np.max(values4) - percentile3) * 0.25
        # merge norm data
        norm_data = np.zeros_like(flattened_data, dtype=float)
        norm_data[flattened_data <= percentile1] = values1_norm
        norm_data[(flattened_data > percentile1) & (flattened_data <= percentile2)] = values2_norm
        norm_data[(flattened_data > percentile2) & (flattened_data <= percentile3)] = values3_norm
        norm_data[flattened_data > percentile3] = values4_norm
        # revert to the shape of the org_img
        norm_data = norm_data.reshape(org_img.shape)

        # render
        colormap = plt.cm.jet
        colored_img = colormap(norm_data)
        colored_img[org_img == 0] = (0, 0, 0, 1)
        colored_img = (colored_img[:, :, :3] * 255).astype(np.uint8)
        colored_img = cv2.cvtColor(colored_img, cv2.COLOR_RGB2BGR)
        if need_left_img:
            filepath, filename = os.path.split(org_img_path)
            filename_without_extension, _ = os.path.splitext(filename)
            left_filename = filename_without_extension.replace(img_type, f'left') + '.png'
            left_filepath = os.path.join(filepath, left_filename)
            if os.path.exists(left_filepath):
                left_img = cv2.imread(left_filepath, cv2.IMREAD_COLOR)
                colored_img = np.vstack((left_img, colored_img))
                if need_value_show and img_type == 'depth':
                    h, w, c = colored_img.shape
                    x_step_num = 6
                    y_step_num = 12
                    x_step = w // x_step_num
                    y_step = h // y_step_num
                    for j in range(y_step_num):
                        cv2.line(colored_img, (0, j * y_step), (w, j * y_step), (255, 255, 255), 1)
                    for i in range(x_step_num):
                        cv2.line(colored_img, (i * x_step, 0), (i * x_step, h), (255, 255, 255), 1)
                    for i in range(1, x_step_num):
                        for j in range(1, y_step_num):
                            try:
                                font_size = 1.0 if w >= 1280 else 0.5
                                depth_val = org_img[i * y_step, j * x_step]
                                cv2.putText(colored_img, f'{depth_val / 1000:.3f}m', (j * x_step + 3, i * y_step - 3),
                                            cv2.FONT_HERSHEY_SIMPLEX, font_size, (255, 255, 255), 2)
                                cv2.putText(colored_img, f'{depth_val / 1000:.3f}m',
                                            (j * x_step + 3, h // 2 + i * y_step - 6), cv2.FONT_HERSHEY_SIMPLEX, font_size,
                                            (255, 255, 255), 2)
                            except:
                                continue

                    print(x_step, y_step)
        cv2.namedWindow("render img", cv2.WINDOW_NORMAL)
        cv2.resizeWindow("render img", 640, 800)
        cv2.imshow("render img", colored_img)
        cv2.waitKey(waitkey_time)

        if save_dir != '':
            os.makedirs(save_dir, exist_ok=True)
            filepath, filename = os.path.split(org_img_path)
            filename_without_extension, _ = os.path.splitext(filename)
            result_filename = filename_without_extension.replace(img_type, f'render_{img_type}') + '.png'
            result_filepath = os.path.join(save_dir, result_filename)
            colored_img = cv2.cvtColor(colored_img, cv2.COLOR_BGR2RGB)
            imageio.imwrite(result_filepath, colored_img)
            print(f'=> save render result to {result_filepath}')

            if save_gif or save_mp4:
                gif_frames.append(colored_img)

    if os.path.exists(save_dir) and save_gif and len(gif_frames) > 2:
        print('=============================================================')
        result_filepath = os.path.join(save_dir, 'result.gif')
        print(f'=> save gif result to {result_filepath}')
        imageio.mimsave(result_filepath, gif_frames, fps=5, loop=0)

    if os.path.exists(save_dir) and save_mp4 and len(gif_frames) > 2:
        result_filepath = os.path.join(save_dir, 'result.mp4')
        height, width, _ = gif_frames[0].shape
        # 定义视频编码器和输出对象
        fourcc = cv2.VideoWriter_fourcc(*"mp4v")  # 使用 'mp4v' 编码
        video_writer = cv2.VideoWriter(result_filepath, fourcc, 5, (width, height))

        # 写入每帧到视频文件
        for image in gif_frames:
            frame = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
            video_writer.write(frame)

        # 释放资源
        video_writer.release()
        print(f"=> mp4 save to: {result_filepath}")