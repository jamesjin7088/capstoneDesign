import cv2
import numpy as np
from sklearn.cluster import KMeans

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

def extract_colors(image, boxes, k_objects=3, k_background=3, margin=10, blur_kernel=(25, 25), brightness_threshold=100):
    """객체 및 배경 색상 추출.  마스크 생성 방식 개선, 벡터화, 밝기 필터 개선."""

    mask = np.zeros(image.shape[:2], dtype=np.uint8)

    # 객체 영역 마스크 생성 (margin 추가) - 벡터화
    for box in boxes:
        x1, y1, x2, y2 = map(int, box.xyxy[0])
        x1_m, y1_m = max(x1 - margin, 0), max(y1 - margin, 0)
        x2_m, y2_m = min(x2 + margin, image.shape[1]), min(y2 + margin, image.shape[0])
        cv2.rectangle(mask, (x1_m, y1_m), (x2_m, y2_m), 255, -1)

    # 객체 색상 추출 - 리스트 컴프리헨션 사용
    object_colors = [get_dominant_colors(image[int(box.xyxy[0][1]):int(box.xyxy[0][3]), int(box.xyxy[0][0]):int(box.xyxy[0][2])], k=k_objects) for box in boxes]
    object_palette = get_dominant_colors(np.concatenate(object_colors).reshape(-1, 1, 3), k=k_objects)

    # 배경 마스크 적용 후 블러 처리
    background = cv2.bitwise_and(image, image, mask=cv2.bitwise_not(mask))
    background_blurred = cv2.GaussianBlur(background, blur_kernel, 0)

    # 밝기 필터링 개선 (sum 대신 mean 사용)
    reshaped_bg = background_blurred.reshape((-1, 3))
    brightness_filter = np.mean(reshaped_bg, axis=1) > brightness_threshold
    reshaped_bg = reshaped_bg[brightness_filter]

    # 최종 배경 색상 추출
    if len(reshaped_bg) > 0:
        background_palette = get_dominant_colors(reshaped_bg.reshape(-1, 1, 3), k=k_background)
    else:
        background_palette = np.array([[255, 255, 255]])  # 배경 픽셀이 없으면 흰색으로 기본값 처리

    return object_palette, background_palette
