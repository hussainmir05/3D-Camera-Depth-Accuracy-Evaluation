# 3D Camera Depth Accuracy Evaluation
Evaluation of 3D camera accuracy using RGB images and point-cloud data. The project performs ROI-based surface segmentation, SVD plane fitting, plane-to-plane distance measurement, and point-to-plane error analysis to evaluate depth accuracy and surface noise at different camera distances.

## Plane to Plane Distance
Method 
1. Load RGB + 3D point cloud data
2. Crop each stair region using polygon ROI
3. Fit a plane to each stair surface using SVD
4. Compute perpendicular plane-to-plane distance
5. Compare measured distances with ground truth
The stair regions used for plane fitting and measurement were segmented manually on the RGB image as shown below 

| Original RGB Image | Segmented Stair Regions |
|---|---|
| <img src="ground_truth_rgb_img.bmp" width="250">| <img src="segment_rgb.png" width="250">  |

| Cam Distance     | Step 1 → 2 (mm) | Step 2 → 3 (mm) | Step 3 → 4 (mm) | Step 4 → 5 (mm) | Error (RMSE mm) |
| ---------------- | --------------- | --------------- | --------------- | --------------- | --------------- |
| 33 cm            | 1.162           | 1.998           | 3.918           | 7.805           | **0.1332**      |
| 43 cm            | 1.013           | 1.993           | 4.012           | 8.060           | **0.0315**      |
| 53 cm            | 1.009           | 1.983           | 3.976           | 8.041           | **0.0256**      |
| 63 cm            | 0.994           | 1.956           | 3.938           | 7.973           | **0.0404**      |
| 73 cm            | 0.998           | 1.929           | 3.866           | 7.661           | **0.1865**      |
| **Ground Truth** | **1**           | **2**           | **4**           | **8**           |    0            |



##  Point to Plane Error 
After fitting a plane to each segmented stair surface using SVD, the point-to-plane residuals are computed to evaluate surface fitting quality and noise consistency across different camera distances.

The error metrics are reported as:

MAE (Mean Absolute Error): average deviation of points from the fitted plane
STD (Standard Deviation): spread of point-to-plane residuals (surface noise)

MAE (mm)gi

| Step | 33 cm  | 45 cm  | 53 cm  | 63 cm  | 70 cm  |
| ---- | ------ | ------ | ------ | ------ | ------ |
| 1    | 0.071  | 0.216  | 0.265  | 0.189  | 0.267  |
| 2    | 0.052  | 0.215  | 0.268  | 0.186  | 0.268  |
| 3    | 0.044  | 0.222  | 0.265  | 0.185  | 0.266  |
| 4    | 0.051  | 0.224  | 0.256  | 0.186  | 0.259  |
| 5    | 0.065  | 0.220  | 0.237  | 0.190  | 0.251  |
| Avg  | 0.0566 | 0.2194 | 0.2582 | 0.1872 | 0.2622 |

STD (mm)

| Step | 33 cm  | 45 cm  | 53 cm  | 63 cm  | 70 cm  |
| ---- | ------ | ------ | ------ | ------ | ------ |
| 1    | 0.052  | 0.148  | 0.188  | 0.150  | 0.256  |
| 2    | 0.039  | 0.148  | 0.200  | 0.149  | 0.220  |
| 3    | 0.043  | 0.159  | 0.197  | 0.153  | 0.220  |
| 4    | 0.040  | 0.154  | 0.189  | 0.148  | 0.208  |
| 5    | 0.303  | 0.283  | 0.177  | 0.149  | 0.205  |
| Avg  | 0.0954 | 0.1784 | 0.1902 | 0.1498 | 0.2218 |


Number of Points per Plane
| Step | 33 cm   | 45 cm   | 53 cm   | 63 cm   | 70 cm   |
| ---- | ------- | ------- | ------- | ------- | ------- |
| 1    | 355,066 | 375,926 | 594,901 | 663,107 | 340,247 |
| 2    | 290,838 | 486,701 | 473,272 | 443,501 | 223,287 |
| 3    | 291,383 | 481,151 | 465,429 | 440,647 | 221,181 |
| 4    | 310,155 | 482,891 | 478,708 | 441,686 | 221,604 |
| 5    | 250,614 | 717,197 | 624,440 | 658,972 | 336,100 |

