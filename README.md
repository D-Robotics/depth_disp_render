# depth_disp_render

## 描述

深度图/视差图伪彩色渲染

## 运行

1. 安装python依赖包

```shell
pip install -r requirements.txt
```

2. 文件组织格式

![folder_contents.png](doc%2Ffolder_contents.png)

程序会读取`depth`、`disp`、`left`开头的文件，对应`深度图`、`视差图`、`左图`，其中`深度图`支持`png`格式的`16bit`
图像，其中`视差图`支持`pfm/tiff`格式的`float32`图像，请固定文件的开头，并保证`深度图`、`视差图`、`左图`的后缀是一致的。

3. 批量渲染

```shell
# 通过img_dir指定文件夹路径，img_type指定渲染深度图还是视差图，save_dir指定保存路径
python render.py --img_dir=./stereonet_images_zed2i_4 --img_type=depth --save_dir=./render_stereonet_images_zed2i_4
```

4. 单张图渲染

```shell
# 通过img_path指定但张图路径，img_type指定渲染深度图还是视差图，save_dir指定保存路径
python render.py --img_path=D:\3_HoBot\3_RDK_X3_X5\14_Stereo\render\template\depth000001.png --img_type=depth --save_dir=./render_template
```

5. 参数说明

| 名称                  | 默认值                       | 类型     | 说明                                          |
|---------------------|---------------------------|--------|---------------------------------------------|
| img_dir             | ''                        | string | 文件夹目录，按渲染需求包含需要的左图、深度图、视差图                  |
| img_path            | ''                        | string | 渲染图像的路径，指定单张深度图/视差图的路径                      |
| img_type            | depth                     | string | 渲染图像的类型，可设置为[depth, disp]，一定要指定渲染的是深度图还是视差图 |
| min_disp            | 2.0                       | float  | 视差小于该值，不进行渲染，颜色为黑色                          |
| max_disp            | 192.0                     | float  | 视差大于该值，不进行渲染，颜色为黑色                          |
| min_depth           | 0.0                       | float  | 深度小于该值，不进行渲染，颜色为黑色                          |
| max_depth           | 10000.0 (默认单位是mm，这里表示10m) | float  | 深度大于该值，不进行渲染，颜色为黑色                          |
| save_dir            | ''                        | string | 保存结果的目录，会自动创建                               |
| save_gif            | False                     | bool   | 是否保存gif图像，设置会True会在结果目录保存gif动图              |
| need_left_img       | False                     | bool   | 是否在保存结果时附带左图，需要对应的文件夹下有左图，左图会拼接在深度图/视差图上方   |
| need_speckle_filter | True                      | bool   | 是否需要speckle filter，会去除深度图/视差图的散点            |

## 结果展示

| 相机类型  | 深度渲染结果                                        | 视差渲染结果                                      |
|-------|-----------------------------------------------|---------------------------------------------|
| zed2i | ![depth_zed2i_1.gif](doc%2Fdepth_zed2i_1.gif) | ![disp_zed2i_1.gif](doc%2Fdisp_zed2i_1.gif) |
| zed2i | ![depth_zed2i_2.gif](doc%2Fdepth_zed2i_2.gif) | ![disp_zed2i_2.gif](doc%2Fdisp_zed2i_2.gif) |
| zed2i | ![depth_zed2i_3.gif](doc%2Fdepth_zed2i_3.gif) | ![disp_zed2i_3.gif](doc%2Fdisp_zed2i_3.gif) |
| zed2i | ![depth_zed2i_4.gif](doc%2Fdepth_zed2i_4.gif) | ![disp_zed2i_4.gif](doc%2Fdisp_zed2i_4.gif) |
| s316  | ![depth_s316_1.gif](doc%2Fdepth_s316_1.gif)   | ![disp_s316_1.gif](doc%2Fdisp_s316_1.gif)   |
| s316  | ![depth_s316_2.gif](doc%2Fdepth_s316_2.gif)   | ![disp_s316_2.gif](doc%2Fdisp_s316_2.gif)   |


