import os
from http.client import responses

from ultralytics import YOLO
import cv2
import base64
import numpy as np
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt
import pathlib
import textwrap
from openai import OpenAI

import google.generativeai as genai

# Google Gemini Pro Vision API 설정
google_api = "API"  # 여기에 실제 API 키를 입력
genai.configure(api_key=google_api)

model = genai.GenerativeModel('gemini-2.5-pro-exp-03-25')

chat = model.start_chat()

# OpenAI API 설정
os.environ[
    "OPENAI_API_KEY"] = "API"  # 여기에 실제 API 키를 입력
openai_api_key = os.getenv("OPENAI_API_KEY")
client = OpenAI()


def resize_image_preserve_aspect_ratio(image, max_dim=640):
    """
    이미지의 가로 또는 세로 중 긴 쪽을 max_dim으로 맞추며 비율을 유지하며 리사이즈합니다.
    이미지가 max_dim보다 작으면 원본 크기 유지.

    Args:
        image: 리사이즈할 이미지 (numpy array).
        max_dim: 최대 크기 (int).

    Returns:
        np.darray: 리사이즈된 이미지.
    """

    h, w = image.shape[:2]

    # image가 max_dim보다 크면 리사이즈
    if max(h, w) > max_dim:
        if h > w:
            scale = max_dim / h
            new_h = max_dim
            new_w = int(w * scale)
        else:
            scale = max_dim / w
            new_w = max_dim
            new_h = int(h * scale)

        # 이미지 리사이즈
        resized_image = cv2.resize(image, (new_w, new_h), interpolation=cv2.INTER_AREA)
        print(f"Image resized from ({w}, {h}) to ({new_w}, {new_h})")  # 리사이즈 정보 출력
        return resized_image
    else:
        # 이미지가 max_dim보다 작거나 같으면 원본 반환
        print(f"Image size ({w}, {h}) is within max_dim ({max_dim}), no resize needed.")
        return image


def get_dominant_colors(image, k=1):
    """이미지에서 k개의 주요 색상 추출 (색상 빈도에 따른 가중치 적용). uint8, RGB 처리 포함."""
    if image.dtype != np.uint8:
        image = image.astype(np.uint8)

    if len(image.shape) == 3 and image.shape[2] == 4:
        image = cv2.cvtColor(image, cv2.COLOR_BGRA2RGB)
    elif len(image.shape) == 3 and image.shape[2] == 3:  # 이미 RGB인 경우 변환하지 않음
        pass
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


def extract_colors(image, boxes, k_objects=3, k_background=3, margin=10, blur_kernel=(25, 25),
                   brightness_threshold=100):
    """객체 및 배경 색상 추출.  마스크 생성 방식 개선, 벡터화, 밝기 필터 개선."""

    mask = np.zeros(image.shape[:2], dtype=np.uint8)

    # 객체 영역 마스크 생성 (margin 추가) - 벡터화
    for box in boxes:
        x1, y1, x2, y2 = map(int, box.xyxy[0])
        x1_m, y1_m = max(x1 - margin, 0), max(y1 - margin, 0)
        x2_m, y2_m = min(x2 + margin, image.shape[1]), min(y2 + margin, image.shape[0])
        cv2.rectangle(mask, (x1_m, y1_m), (x2_m, y2_m), 255, -1)

    # 객체 색상 추출 - 리스트 컴프리헨션 사용
    object_colors = [
        get_dominant_colors(image[int(box.xyxy[0][1]):int(box.xyxy[0][3]), int(box.xyxy[0][0]):int(box.xyxy[0][2])],
                            k=k_objects) for box in boxes]
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


def visualize_results(image_rgb, boxes, results, object_palette, background_palette):
    """결과 시각화 함수.  불필요한 imshow 제거 및 효율적인 팔레트 생성."""
    fig, axes = plt.subplots(1, 3, figsize=(18, 6))

    # 원본 이미지 및 바운딩 박스
    axes[0].imshow(image_rgb)
    axes[0].axis("off")
    axes[0].set_title("Detected Objects")

    for box in boxes:
        x1, y1, x2, y2 = map(int, box.xyxy[0])
        label = results[0].names[int(box.cls[0])]  # results[0] 사용
        conf = box.conf[0]
        cv2.rectangle(image_rgb, (x1, y1), (x2, y2), (255, 0, 0), 2)
        cv2.putText(image_rgb, f"{label} {conf:.2f}", (x1, y1 - 10),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 2)

    axes[0].imshow(image_rgb)  # 바운딩 박스가 그려진 이미지를 표시

    # 객체 색상 팔레트
    object_patches = np.hstack([np.full((100, 100, 3), color, dtype=np.uint8) for color in object_palette])
    axes[1].imshow(object_patches)
    axes[1].axis("off")
    axes[1].set_title("Objects Color Palette")

    # 배경 색상 팔레트
    background_patches = np.hstack([np.full((100, 100, 3), color, dtype=np.uint8) for color in background_palette])
    axes[2].imshow(background_patches)
    axes[2].axis("off")
    axes[2].set_title("Background Color Palette")

    plt.tight_layout()
    plt.show()


async def analyze_scene(object_names, object_palette, background_palette):
    """Gemini Pro Vision을 사용하여 장면 분석."""

    object_colors_hex = ['#%02x%02x%02x' % (r, g, b) for r, g, b in object_palette]
    background_colors_hex = ['#%02x%02x%02x' % (r, g, b) for r, g, b in background_palette]

    prompt = f"""
        This space contains: {", ".join(object_names)}. 
        Object colors: {", ".join(object_colors_hex)}. 
        Background colors: {", ".join(background_colors_hex)}.

        - Based on the objects, what other furniture would fit well here?
        - Based on the object colors, what other furniture color would fit well here?
        - What kind of room is this (e.g., living room, bedroom, kitchen)?

        using korean.
        And when answer, just pull out the list without any additional explanation.
        (e.g., (가구1, 가구2, 가구3), (색깔), (방))
        """
    try:
        response = chat.send_message(prompt)

        return response.text

    except Exception as e:
        print(f"Gemini API 호출 오류: {e}")
        return "Gemini API 호출에 실패했습니다."


async def open_ai_recommend_furniture(room, object):
    """
    openai를 사용한 가구 합성 Flow

    YOLO를 통한 객체 추출
    ->
    Gemini를 통한 가구, 색깔 추천
    ->
    gpt4o를 사용하여 마스크 공간 자동생성
    ->
    Dall-E를 사용하여 마스크 공간에 가구 합성
    """

    prompt = f"""
        Room: {room}
        Object: {object}

        Make mask image in the room for furniture.
        """
    try:
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[{
                "role": "user",
                "content": [
                    {"type": "text", "text": prompt},
                    {
                        "type": "image_url",
                        "image_url": f"data:image/png;base64,{encode_image('room.png')}",
                    },
                ],
            }
            ],
        )

        return response.choices[0].message.content

    except Exception as e:
        print(f"OpenAI API 호출 오류: {e}")
        return "OpenAI API 호출에 실패했습니다."


def parse_furniture_and_room(input_string):
    """
    "(가구1, 가구2, 가구3), (방)" 형태의 문자열을 파싱하여
    가구 목록과 방 종류를 분리된 배열로 반환합니다.

    Args:
        input_string: 파싱할 문자열 (예: "(가구1, 가구2, 가구3), (방)")

    Returns:
        가구 목록 (list)과 방 종류 (str)를 담은 튜플.
        파싱에 실패하면 (None, None)을 반환합니다.
    """
    try:
        # 1. 괄호와 쉼표를 기준으로 문자열 분리
        parts = input_string.replace("(", "").replace(")", "").split(", ")

        # 2. 가구 목록과 방 종류 분리
        furniture_list = parts[:-2]  # 마지막에서 세번째 요소부터 가구 목록
        room_type = parts[-1]  # 마지막 요소가 방 종류
        recommend_color = parts[-2]  # 마지막에서 두번째가 추천 색깔

        return furniture_list, recommend_color, room_type

    except Exception as e:
        print(f"파싱 오류: {e}")
        return None, None


def encode_image(image_path):
    """이미지를 base64로 인코딩합니다."""
    with open(image_path, "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read()).decode('utf-8')
    return encoded_string


# YOLOv11 모델 로드
model = YOLO("yolo11m.pt")  # 사전 학습된 모델 사용

# 방 사진 불러오기
image_path = "test3.jpeg"  # 이미지 경로 설정 필요
image = cv2.imread(image_path)

if image is None:
    print("이미지를 불러오는 데 실패했습니다. 경로를 확인하세요.")

else:
    image = resize_image_preserve_aspect_ratio(image, max_dim=640)  # 이미지 리사이즈
    image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    results = model(image)  # 객체 검출

    # 객체 검출 후 박스 정보 추출
    boxes = []
    object_names = []  # 검출된 객체 이름을 저장할 리스트
    if results:  # results가 비어있지 않은지 확인
        for result in results:
            if result.boxes is not None:  # result 안에 boxes가 있는지 확인
                for box in result.boxes:
                    if box.conf is not None and len(box.conf) > 0 and box.conf[0] >= 0.4:  # box.conf 확인 추가
                        boxes.append(box)
                        if box.cls is not None and len(box.cls) > 0 and result.names:  # box.cls 및 result.names 확인 추가
                            class_index = int(box.cls[0])
                            if 0 <= class_index < len(result.names):
                                object_names.append(result.names[class_index])  # 클래스 이름 추가

    # 빈 배열이 아닐 경우 객체 및 배경 색상 팔레트 추출
    if result is not None and len(boxes) > 0:
        object_palette, background_palette = extract_colors(image_rgb, boxes)

        # 객체 및 배경 색상 팔레트 시각화
        visualize_results(image_rgb.copy(), boxes, results, object_palette, background_palette)  # image_rgb 복사본 전달

# Gemini Pro Vision을 사용하여 장면 분석 및 결과 출력
import asyncio
async def main():
    if not object_names:
        print("No objects detected.")
        return
    # object_palette와 background_palette가 정의되었는지 확인
    if 'object_palette' in locals() and 'background_palette' in locals():
        analysis_result = await analyze_scene(object_names, object_palette, background_palette)
        if analysis_result and analysis_result != "Gemini API 호출에 실패했습니다.":
            furniture, recommend_color, room = parse_furniture_and_room(analysis_result)
            if furniture is not None and room is not None:
                print(f'가구 : {furniture}\n추천 색깔: {recommend_color}\n방: {room}')
                # OpenAI API를 사용하여 가구 합성
                # openai_result = await open_ai_recommend_furniture(room, furniture) # 주석 처리 (필요시 해제)
                # print(f'가구 합성 결과: {openai_result}') # 주석 처리 (필요시 해제)
            else:
                print(f"Could not parse analysis result: {analysis_result}")
        else:
            print(f"Scene analysis failed or returned an error: {analysis_result}")
    else:
        print("Color palettes could not be extracted, skipping scene analysis.")


if 'google_api' in locals():  # api키가 존재할 시 실행
    print("Analyze Start")
    asyncio.run(main())
else:
    print("Google API key not found.")  # API 키 없을 시 메시지