# -*- coding: utf-8 -*-
"""
Created on Tue May 28 18:47:59 2024

@author: user
"""

import geopandas as gpd 
from shapely.geometry import Point 
from shapely.geometry import LineString 

# 建立儲存所有線段端點的串列 
all_points = [] 
# 建立1.5m內配對點的串列 
paired_points = [] 
#建立生成的線的串列     
paired_lines = [] 
#建立檢查點的串列
chk_point = []
  
# 讀取shp 
gdf = gpd.read_file(r'C:\Users\user\Desktop\ceci_程式練習\河流_project1\圖資\line2.shp') 
 
# 從線段中提取出每個線段的端點 
for geom in gdf.geometry: 
        
    #取出每個線段的起點跟終點
    start_point = geom.coords[0] 
    end_point = geom.coords[-1] 
    # 將起點和終點添加到all point串列中
    all_points.append(start_point) 
    all_points.append(end_point)

# 為了避免取到重覆線段的重複端點，因此計算all point中端點出現的次數，只取出現過一次的點    
for point in all_points:
    if all_points.count(point) == 1:
        chk_point.append(point)
     
# 遍歷chk point中所有的點
for a, point1 in enumerate(chk_point): 
    # 創建point 
    p1 = Point(point1) 
    # 建立串列儲存1.5m內的點 
    close_points = [] 
    # 這裡在做的是，不要讓檢查過的點重複，避免重複生成線段
    for b, point2 in enumerate(chk_point): 
        # 跳過自己還有已經被配對過的點
        #配對過的點
        point_repeat = [p[0] for p in paired_points]
        if a == b or point2 in point_repeat: 
            continue 
        # 再創建一次point來跟p1做比較 
        p2 = Point(point2) 
        # 計算p1跟p2的距離
        dist = p1.distance(p2) 
        # 如果兩點距離小於1.5m，將另一個點儲存到close_points 串列中 
        if dist <= 1.5: 
            close_points.append(point2) 
    # 若找到離距離小於等於 1.5 米的點，將他們一起儲存到 paired_points 串列中 
    if close_points: 
        paired_points.append([point1] + close_points) 
 
# print 點的對(只是為了看有沒有抓到點而已，可以省略) 
for i, pair in enumerate(paired_points): 
    print(f"Pair {i + 1}: {pair}") 
 
#瀏覽paired_points中的每一對點 
for pair in paired_points: 
    #取出兩點座標 
    point3 = pair[0] 
    point4 = pair[1] 
     
    #將兩點生成線資料 
    line = LineString([point3, point4]) 
    #將線储存到列表中 
    paired_lines.append(line) 
     
# =============================================================================
# #print生成的線，一樣也可省略 
# for i, line in enumerate(paired_lines): 
#     print(f"Line {i + 1}: {line}") 
# =============================================================================

# 將生成的線另外建立一個gdf 
gdf_paired_lines = gpd.GeoDataFrame(geometry = paired_lines) 
 
# 指定輸出的文件路徑
output_shapefile = r'C:\Users\user\Desktop\ceci_程式練習\河流_project1\圖資\paired_lines.shp' 
 
# 將gdf導出為shp 
gdf_paired_lines.to_file(output_shapefile)
        
        