import cv2
import numpy as np
import matplotlib.pyplot as plt

def create_empty_space_mask(image_shape, boxes, floor_threshold_ratio=0.6, margin=20, min_area_threshold=5000):
    """
    이미지에서 바닥을 제외한 영역에 대한 마스크를 생성합니다.
    바닥 영역은 floor_threshold_ratio 비율로 설정되며, margin과 min_area_threshold를 고려합니다.

    Args:
        image_shape: 이미지의 shape (높이, 너비).
        boxes: YOLO 모델의 예측 결과 (바운딩 박스).
        floor_threshold_ratio: 바닥 영역 비율 (0.0 ~ 1.0).
        margin: 바닥 영역 주변의 여유 공간 (픽셀 단위).
        min_area_threshold: 최소 면적 임계값 (픽셀 단위).

    Returns:
        mask: 바닥을 제외한 영역에 대한 마스크 (numpy array).
        None: 바닥 영역이 없을 경우.
    """
    height, width = image_shape[:2]
    # 1. 객체 영역 마스크 생성
    occupied_mask = np.zeros((height, width), dtype=np.uint8)

    if not boxes:
        print("No boxes detected.")
        # 또는 기본 바닥 마스크를 반환하도록 수정할 수 있습니다.
        # floor_mask = np.zeros((height, width), dtype=np.uint8)
        # floor_y_start = int(height * (1 - floor_threshold_ratio))
        # cv2.rectangle(floor_mask, (0, floor_y_start), (width, height), 255, -1)
        # return floor_mask
        return None

    for box in boxes:
        x1, y1, x2, y2 = map(int, box.xyxy[0])

        # 마진 추가 및 경계 체크
        x1_m = max(x1 - margin, 0)
        y1_m = max(y1 - margin, 0)
        x2_m = min(x2 + margin, width)
        y2_m = min(y2 + margin, height)

        # 객체 영역을 흰색으로 채움
        cv2.rectangle(occupied_mask, (x1_m, y1_m), (x2_m, y2_m), 255, -1)

        # 2. 잠재적 바닥 영역 마스크 생성
        potential_floor_mask = np.zeros((height, width), dtype=np.uint8)
        floor_y_start = int(height * (1 - floor_threshold_ratio))
        cv2.rectangle(potential_floor_mask, (0, floor_y_start), (width, height), 255, -1)

        # 3. 빈 공간 마스크 계산
        #   - 객체가 없는 영역 (occupied_mask의 반전)과
        #   - 잠재적 바닥 영역 (potential_floor_mask)의
        #   - 교집합 (AND 연산)
        inverted_occupied_mask = cv2.bitwise_not(occupied_mask)
        empty_space_mask = cv2.bitwise_and(inverted_occupied_mask, potential_floor_mask)

        # 4. 마스크 정제
        #    - 작은 노이즈 제거 (Opening: 침식 후 팽창)
        #    - 작은 구멍 메우기 (Closing: 팽창 후 침식)
        kernel = np.ones((5, 5), np.uint8)
        cleaned_mask = cv2.morphologyEx(empty_space_mask, cv2.MORPH_OPEN, kernel, iterations=2)
        cleaned_mask = cv2.morphologyEx(cleaned_mask, cv2.MORPH_CLOSE, kernel, iterations=3)  # Closing 반복 늘림

        #    - 너무 작은 영역 제거 (Contour Area Filtering)
        contours, _ = cv2.findContours(cleaned_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        final_mask = np.zeros((height, width), dtype=np.uint8)
        valid_contours_found = False
        for contour in contours:
            if cv2.contourArea(contour) > min_area_threshold:
                cv2.drawContours(final_mask, [contour], -1, 255, -1)  # 면적이 임계값 이상인 것만 그림
                valid_contours_found = True

        if not valid_contours_found:
            print(f"No empty space found with area larger than {min_area_threshold} pixels.")
            return None  # 유효한 큰 빈 공간이 없으면 None 반환

        return final_mask