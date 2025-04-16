from http.client import responses

from ultralytics import YOLO
import cv2
import numpy as np
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt
import pathlib
import textwrap
import os

from dotenv import load_dotenv
load_dotenv()

import google.generativeai as genai

def get_dominant_colors(image, k=1):
    """이미지에서 k개의 주요 색상 추출 (색상 빈도에 따른 가중치 적용). uint8, RGB 처리 포함."""
    if image.dtype != np.uint8:
        image = image.astype(np.uint8)

    if len(image.shape) == 3 and image.shape[2] == 4:
        image = cv2.cvtColor(image, cv2.COLOR_BGRA2RGB)
    elif len(image.shape) == 3 and image.shape[2] == 3:  # 이미 RGB인 경우 변환하지 않음
        pass  # 이미 RGB
    else:
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    reshaped_img = image.reshape((-1, 3))

    # K-Means 클러스터링 수행
    kmeans = KMeans(n_clusters=k, n_init=10, random_state=42, algorithm='elkan')  # elkan 알고리즘 추가
    labels = kmeans.fit_predict(reshaped_img)

    # 클러스터의 빈도를 계산하여 가중치를 적용
    label_counts = np.bincount(labels)
    sorted_indices = np.argsort(-label_counts)

    dominant_colors = kmeans.cluster_centers_[sorted_indices].astype(int)

    return dominant_colors