import os
import base64
import asyncio
import uuid  # 고유한 파일명 생성을 위해 사용
import json  # Gemini 응답 파싱을 위해 사용

import cv2
import numpy as np
import PIL.Image
import requests
from flask import Flask, jsonify, request, send_from_directory
from flask_cors import CORS
from openai import AsyncOpenAI  # 비동기 OpenAI 클라이언트 사용
from ultralytics import YOLO
import google.generativeai as genai
from dotenv import load_dotenv

# 로컬 모듈 임포트 (detect_colors.py, create_mask.py 파일이 존재해야 함)
from detect_colors import extract_colors
from create_mask import create_empty_space_mask

load_dotenv() # .env 파일에서 환경 변수 로드

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY", "YOUR_GOOGLE_API_KEY_FALLBACK")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "YOUR_OPENAI_API_KEY_FALLBACK")

if GOOGLE_API_KEY == "YOUR_GOOGLE_API_KEY_FALLBACK" or OPENAI_API_KEY == "YOUR_OPENAI_API_KEY_FALLBACK":
    print("경고: API 키가 기본값으로 설정되어 있습니다. 실제 키를 환경 변수로 설정해주세요.")

# Flask 앱 설정
app = Flask(__name__, static_url_path='/static')
CORS(app, resources={r"/*": {"origins": "*"}})

UPLOAD_FOLDER = "uploads"  # 업로드된 원본 이미지가 저장될 폴더
RESULTS_FOLDER = "results"  # DALL-E 생성 결과 이미지가 저장될 폴더
MASKS_FOLDER = "masks"  # 생성된 마스크 이미지가 저장될 폴더

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(RESULTS_FOLDER, exist_ok=True)
os.makedirs(MASKS_FOLDER, exist_ok=True)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['RESULTS_FOLDER'] = RESULTS_FOLDER
app.config['MASKS_FOLDER'] = MASKS_FOLDER

# --- API 클라이언트 및 모델 초기화 ---
gemini_model = None
yolo_model = None
openai_client = None

try:
    if GOOGLE_API_KEY != "YOUR_GOOGLE_API_KEY_FALLBACK":
        genai.configure(api_key=GOOGLE_API_KEY)
        # 사용 가능한 최신 모델 또는 특정 모델 지정 (예: 'gemini-1.5-pro-latest', 'gemini-pro')
        gemini_model = genai.GenerativeModel('gemini-1.5-pro-latest')
    else:
        print("Google API 키가 설정되지 않아 Gemini 모델을 초기화할 수 없습니다.")
except Exception as e:
    print(f"Google Gemini 모델 초기화 중 오류 발생: {e}")

try:
    yolo_model = YOLO("yolo11m.pt")  # 또는 사용하려는 YOLO 모델 파일 (예: yolov5m.pt)
except Exception as e:
    print(f"YOLO 모델 로딩 중 오류 발생: {e}")

try:
    if OPENAI_API_KEY != "YOUR_OPENAI_API_KEY_FALLBACK":
        openai_client = AsyncOpenAI(api_key=OPENAI_API_KEY)
    else:
        print("OpenAI API 키가 설정되지 않아 OpenAI 클라이언트를 초기화할 수 없습니다.")
except Exception as e:
    print(f"OpenAI 클라이언트 초기화 중 오류 발생: {e}")


# --- 헬퍼 함수 ---

def resize_image_preserve_aspect_ratio(image, max_dim=640):
    """
    이미지의 가로 또는 세로 중 긴 쪽을 max_dim으로 맞추며 비율을 유지하며 리사이즈.
    이미지가 max_dim보다 작으면 원본 크기 유지.

    Args:
        image: 리사이즈할 이미지 (numpy array).
        max_dim: 최대 크기 (int).

    Returns:
        np.ndarray: 리사이즈된 이미지.
    """
    h, w = image.shape[:2]
    if max(h, w) > max_dim:
        if h > w:
            scale = max_dim / h
            new_h = max_dim
            new_w = int(w * scale)
        else:
            scale = max_dim / w
            new_w = max_dim
            new_h = int(h * scale)
        resized_image = cv2.resize(image, (new_w, new_h), interpolation=cv2.INTER_AREA)
        return resized_image
    return image


async def analyze_scene_with_gemini(object_names, object_palette, background_palette):
    """Gemini를 사용하여 장면 분석 (비동기)"""
    if not gemini_model:
        return '{"error": "Gemini 모델이 초기화되지 않았습니다."}'  # JSON 형태의 오류 메시지 반환

    object_colors_hex = ['#%02x%02x%02x' % (r, g, b) for r, g, b in object_palette]
    background_colors_hex = ['#%02x%02x%02x' % (r, g, b) for r, g, b in background_palette]

    # Gemini에게 JSON 형식으로 응답하도록 요청하는 프롬프트
    prompt = f"""
            Analyze the following scene details:
            Objects present: {", ".join(object_names) if object_names else "None detected"}.
            Dominant object colors (HEX): {", ".join(object_colors_hex) if object_colors_hex else "None"}.
            Dominant background colors (HEX): {", ".join(background_colors_hex) if background_colors_hex else "None"}.

            Provide your analysis in JSON format with the following keys:
            - "recommended_furniture": A list of 2-3 furniture items that would fit well.
            - "recommended_furniture_colors": A list of 2-3 color suggestions (HEX codes) for new furniture.

            Generate only the JSON object. No other text or explanations.
            Example output:
            {{
            "recommended_furniture": ["bookshelf", "floor lamp", "area rug"],
            "recommended_furniture_colors": ["#A0A0A0"]
            }}
            """
    try:
        chat = gemini_model.start_chat()
        response = await asyncio.to_thread(chat.send_message, prompt)

        # Clean and parse the JSON response
        raw_text = response.text.strip()

        # Gemini might wrap the JSON in ```json ... ```
        if raw_text.startswith("```json"):
            raw_text = raw_text[7:]
        if raw_text.endswith("```"):
            raw_text = raw_text[:-3]

        try:
            parsed_json = json.loads(raw_text)
            return parsed_json
        except json.JSONDecodeError as json_e:
            print(f"Gemini JSON decoding error: {json_e}")
            print(f"Problematic Gemini response text: {raw_text}")
            return {"error": "Failed to decode Gemini JSON response", "details": str(json_e), "raw_response": raw_text}

    except Exception as e:
        print(f"Gemini API call error: {e}")
        return {"error": f"Gemini API call failed: {str(e)}"}


async def generate_edited_image_with_dalle(original_image_path: str,
                                        mask_path: str,
                                        theme_description: str,
                                        existing_objects: list,
                                        existing_colors_hex: list):
    """DALL-E를 사용하여 이미지 편집 (비동기)"""
    if not openai_client:
        return None, "OpenAI 클라이언트가 초기화되지 않았습니다."

    prompt = f"""
        The room currently features: {", ".join(existing_objects) if existing_objects else "various items"}.
        Prominent colors in the current objects include: {", ".join(existing_colors_hex) if existing_colors_hex else "various colors"}.

        Redesign the provided room photo to embody a '{theme_description}' style.
        The mask indicates the areas to be significantly altered or where new elements should be introduced.
        Maintain the original room layout and structural elements visible through the transparent (unmasked) areas of the mask.
        Within the masked (non-transparent) regions, transform the furniture, decorations, and wall colors to align with the new '{theme_description}' theme.
        The final image should be photorealistic, seamlessly integrated, and devoid of any text or watermarks.
        """
    try:
        # original_image_path와 mask_path의 파일을 바이너리 읽기 모드로 열기
        with open(original_image_path, "rb") as img_file, open(mask_path, "rb") as mask_file:
            response = await openai_client.images.edit(
                image=img_file,  # 원본 이미지 파일 객체
                mask=mask_file,  # 마스크 파일 객체 (알파 채널이 있는 RGBA PNG)
                prompt=prompt,  # 생성 지시 프롬프트
                n=1,  # 생성할 이미지 개수
                size="1024x1024",  # 생성될 이미지 크기 (DALL-E 2는 256x256, 512x512, 1024x1024 지원)
                response_format="url"  # 응답 형식 (url 또는 b64_json)
            )

        generated_image_url = response.data[0].url
        # 생성된 이미지 URL에서 이미지 데이터 다운로드
        img_data_response = requests.get(generated_image_url)
        img_data_response.raise_for_status()  # HTTP 오류 발생 시 예외 발생
        img_data = img_data_response.content

        unique_id = uuid.uuid4()  # 결과 이미지 파일명을 위한 고유 ID
        result_image_filename = f"dalle_result_{unique_id}.png"
        result_image_path = os.path.join(app.config['RESULTS_FOLDER'], result_image_filename)

        with open(result_image_path, "wb") as f:
            f.write(img_data)  # 다운로드한 이미지 데이터를 파일로 저장

        print(f"DALL-E 결과 이미지 저장 완료: {result_image_path}")
        return result_image_filename, None  # 성공 시 파일명과 None(오류 없음) 반환
    except requests.exceptions.RequestException as e:
        print(f"DALL-E 결과 이미지 다운로드 오류: {e}")
        return None, f"DALL-E 결과 이미지 다운로드 실패: {str(e)}"
    except Exception as e:
        print(f"DALL-E 이미지 생성 오류: {e}")
        return None, f"DALL-E 이미지 생성 실패: {str(e)}"  # 실패 시 None과 오류 메시지 반환


def parse_gemini_json_response(json_string: str):
    """Gemini의 JSON 응답을 안전하게 파싱합니다."""
    try:
        data = json.loads(json_string)
        return data
    except json.JSONDecodeError as e:
        print(f"Gemini JSON 응답 디코딩 오류: {e}")
        print(f"문제의 JSON 문자열: {json_string}")
        # 파싱 실패 시 기본값 또는 오류 구조 반환
        return {
            "error": "JSON 파싱 실패",
            "recommended_furniture": ["정보 없음"],
            "recommended_furniture_colors": ["정보 없음"],
            "room_type": "알 수 없음",
            "ambiance_style_suggestions": ["정보 없음"]
        }
    except Exception as e:  # 다른 예외 처리
        print(f"JSON 파싱 중 예기치 않은 오류 발생: {e}")
        return {"error": "JSON 파싱 중 예기치 않은 오류"}


# --- Flask 라우트 ---
# 업로드된 파일, 마스크, 결과 이미지를 서빙하기 위한 정적 라우트
@app.route('/uploads/<path:filename>')  # path:filename으로 변경하여 하위 폴더도 지원 가능
def display_upload(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)


@app.route('/results/<path:filename>')
def display_result(filename):
    return send_from_directory(app.config['RESULTS_FOLDER'], filename)


@app.route('/masks/<path:filename>')
def display_mask(filename):
    return send_from_directory(app.config['MASKS_FOLDER'], filename)


@app.route('/upload', methods=['POST'])
async def upload_and_process_image():  # 라우트를 비동기로 정의
    # 필수 모델 및 클라이언트 초기화 확인
    if not yolo_model:
        return jsonify({'error': 'YOLO 모델이 로드되지 않았습니다. 서버 로그를 확인해주세요.'}), 500
    if not gemini_model:
        return jsonify({'error': 'Gemini 모델이 초기화되지 않았습니다. 서버 로그를 확인해주세요.'}), 500
    if not openai_client:
        return jsonify({'error': 'OpenAI 클라이언트가 초기화되지 않았습니다. 서버 로그를 확인해주세요.'}), 500

    if 'image' not in request.files:
        return jsonify({'error': '이미지 파일이 제공되지 않았습니다.'}), 400

    file = request.files['image']
    if file.filename == '':
        return jsonify({'error': '이미지 파일이 선택되지 않았습니다.'}), 400

    try:
        unique_id = uuid.uuid4()  # 각 요청에 대한 고유 ID
        original_filename_base, original_file_ext = os.path.splitext(file.filename)
        # 보안을 위해 파일명 직접 사용보다 고유 ID 기반으로 생성
        original_filename = f"upload_{unique_id}{original_file_ext}"
        save_path = os.path.join(app.config['UPLOAD_FOLDER'], original_filename)
        file.save(save_path)

        # OpenCV로 이미지 읽기
        image = cv2.imread(save_path)
        if image is None:
            app.logger.error(f"이미지 파일을 읽을 수 없습니다: {save_path}")
            return jsonify({'error': '업로드된 이미지를 읽을 수 없습니다. 유효한 이미지 형식인지 확인해주세요.'}), 400

        # DALL-E 입력용 이미지 준비 (1024x1024 정사각형 PNG)
        # 1. 비율 유지하며 리사이즈
        resized_image = resize_image_preserve_aspect_ratio(image, max_dim=1024)
        h, w = resized_image.shape[:2]
        target_dim = 1024  # DALL-E 이미지 크기

        # 2. 정사각형으로 패딩 (검은색 배경)
        top_pad = (target_dim - h) // 2
        bottom_pad = target_dim - h - top_pad
        left_pad = (target_dim - w) // 2
        right_pad = target_dim - w - left_pad

        # 패딩값이 음수가 되지 않도록 보정
        top_pad, bottom_pad = max(0, top_pad), max(0, bottom_pad)
        left_pad, right_pad = max(0, left_pad), max(0, right_pad)

        # 패딩 적용하여 정사각형 이미지 생성
        dalle_input_image = cv2.copyMakeBorder(resized_image, top_pad, bottom_pad, left_pad, right_pad, cv2.BORDER_CONSTANT, value=[0, 0, 0])

        # 최종적으로 1024x1024로 리사이즈 (패딩 후 미세 조정)
        dalle_input_image_final = cv2.resize(dalle_input_image, (target_dim, target_dim), interpolation=cv2.INTER_AREA)

        # DALL-E 입력용 이미지를 PNG로 저장
        dalle_image_filename = f"dalle_input_{unique_id}.png"
        dalle_image_path = os.path.join(app.config['UPLOAD_FOLDER'], dalle_image_filename)
        cv2.imwrite(dalle_image_path, dalle_input_image_final)

        # 객체 탐지를 위한 RGB 이미지 (리사이즈된 이미지 사용)
        image_rgb_for_detection = cv2.cvtColor(resized_image, cv2.COLOR_BGR2RGB)

        # 객체 탐지 (YOLO)
        yolo_results = yolo_model(image_rgb_for_detection)
        boxes_data = []  # YOLO 박스 정보를 저장할 리스트
        object_names = []
        if yolo_results:
            for result in yolo_results:  # results는 list of Results objects
                if result.boxes is not None:  # result.boxes는 Boxes object
                    for box in result.boxes:  # box는 하나의 bounding box 정보 (xyxy, conf, cls 등)
                        if box.conf is not None and len(box.conf) > 0 and box.conf[0] >= 0.4:  # 신뢰도 0.4 이상
                            boxes_data.append(box)  # 나중에 마스크 생성 시 사용
                            if box.cls is not None and len(box.cls) > 0 and result.names:
                                class_index = int(box.cls[0])
                                if 0 <= class_index < len(result.names):
                                    object_names.append(result.names[class_index])
        object_names = sorted(list(set(object_names)))  # 중복 제거 및 정렬

        # 빈 공간 마스크 생성 (DALL-E 입력 이미지 크기에 맞춰야 함)
        # 1. 원본 비율 이미지(resized_image) 기준으로 마스크 생성
        empty_space_mask_orig_res = create_empty_space_mask(resized_image.shape, boxes_data,
                                                            floor_threshold_ratio=0.6,
                                                            margin=30, min_area_threshold=5000)
        if empty_space_mask_orig_res is None:
            app.logger.warning("빈 공간 마스크 생성 실패. 기본 마스크 사용 또는 오류 처리.")
            # 예: 전체를 변경 영역으로 하는 마스크 생성 또는 오류 반환
            # 여기서는 오류로 처리하지 않고 진행하나, 실제로는 처리가 필요할 수 있음
            empty_space_mask_orig_res = np.full((resized_image.shape[0], resized_image.shape[1]), 255,
                                                dtype=np.uint8)  # 전체를 변경
            # return jsonify({'error': '유효한 빈 공간 마스크를 생성할 수 없습니다.'}), 500

        # 2. 생성된 마스크를 DALL-E 입력 이미지(dalle_input_image_final)의 패딩에 맞게 조정
        #    (resized_image 마스크를 dalle_input_image_final의 중앙에 배치)
        mask_padded_to_square = np.zeros((target_dim, target_dim), dtype=np.uint8)  # 검은색 배경
        mask_padded_to_square[top_pad: top_pad + h, left_pad: left_pad + w] = empty_space_mask_orig_res

        # 최종 마스크 리사이즈 (패딩 후 미세 조정)
        empty_space_mask_final_resized = cv2.resize(mask_padded_to_square, (target_dim, target_dim),
                                                    interpolation=cv2.INTER_NEAREST)  # 이진 마스크이므로 INTER_NEAREST

        # DALL-E용 RGBA 마스크 생성
        # 알파 채널: 0 (투명) = DALL-E가 채울 영역, 255 (불투명) = 원본 유지 영역
        # create_empty_space_mask는 변경할 영역(빈 공간)을 255로 반환하므로, 이 부분을 알파 0으로 설정
        mask_for_dalle_rgba = np.zeros((target_dim, target_dim, 4), dtype=np.uint8)
        mask_for_dalle_rgba[:, :, 3] = 255  # 기본적으로 모든 픽셀을 불투명하게 설정 (원본 유지)
        mask_for_dalle_rgba[empty_space_mask_final_resized == 255, 3] = 0  # 변경할 영역(마스크에서 255)을 투명하게 설정

        mask_filename = f"mask_{unique_id}.png"
        mask_path = os.path.join(app.config['MASKS_FOLDER'], mask_filename)
        cv2.imwrite(mask_path, mask_for_dalle_rgba)  # RGBA 마스크 저장

        # 색상 추출 (객체 탐지 결과가 있을 경우에만)
        object_palette_rgb_np, background_palette_rgb_np = [], []
        if boxes_data:
            # 색상 추출은 리사이즈된 RGB 이미지(image_rgb_for_detection)와 해당 이미지에서의 박스 좌표 사용
            object_palette_rgb_np, background_palette_rgb = extract_colors(image_rgb_for_detection, boxes_data)

        # 색상 변환 (numpy array -> list of int)
        object_palette_rgb = [list(map(int, color)) if isinstance(color, np.ndarray) else [int(c) for c in color] for color in object_palette_rgb_np]
        background_palette_rgb = [list(map(int, color)) if isinstance(color, np.ndarray) else [int(c) for c in color] for color in background_palette_rgb_np]

        object_colors_hex = ['#%02x%02x%02x' % (r, g, b) for r, g, b in object_palette_rgb]

        # 장면 분석 (Gemini)
        gemini_analysis_data = await analyze_scene_with_gemini(object_names, object_palette_rgb, background_palette_rgb)
        # gemini_analysis_data = parse_gemini_json_response(gemini_analysis_json_str)
        """
        # DALL-E 이미지 생성
        # Gemini 분석 결과에서 스타일 제안 사용, 없으면 기본값 사용
        suggested_styles = gemini_analysis_data.get("ambiance_style_suggestions", ["현대적이고 미니멀한 스타일"])
        theme_to_generate = suggested_styles[0] if suggested_styles and suggested_styles[
            0] != "정보 없음" else "아늑하고 현대적인 스타일"

        generated_image_filename, dalle_error_msg = await generate_edited_image_with_dalle(
            original_image_path=dalle_image_path,  # DALL-E 입력용으로 준비된 이미지 경로
            mask_path=mask_path,  # DALL-E용 RGBA 마스크 경로
            theme_description=theme_to_generate,
            existing_objects=object_names,
            existing_colors_hex=object_colors_hex
        )

        if dalle_error_msg:
            app.logger.error(f"DALL-E 이미지 생성 중 오류: {dalle_error_msg}")
            # DALL-E 실패 시에도 다른 정보는 반환할 수 있도록 처리
        """

        print(gemini_analysis_data)

        # 최종 응답 데이터 구성
        response_data = {
            'message': object_names,
            'original_image_url': request.url_root + f"uploads/{original_filename}",
            # 'dalle_input_image_url': request.url_root + f"uploads/{dalle_image_filename}",  # DALL-E 입력 이미지
            'mask_url': request.url_root + f"masks/{mask_filename}",  # 사용된 마스크
            'color_1': object_colors_hex[0],
            'color_2': object_colors_hex[1] if len(object_colors_hex) > 1 else None,
            'color_3': object_colors_hex[2] if len(object_colors_hex) > 2 else None,
            'furniture': gemini_analysis_data,  # 파싱된 JSON 데이터
            # 'dalle_generated_image_url': request.url_root + f"results/{generated_image_filename}" if generated_image_filename else None,
            # 'dalle_error': dalle_error_msg  # DALL-E 오류 메시지 (있을 경우)
        }
        return jsonify(response_data), 200

    except FileNotFoundError as e:  # 파일 관련 오류
        app.logger.error(f"파일 찾기 오류: {e}", exc_info=True)
        return jsonify({'error': f"서버 파일 오류: {e.strerror}"}), 500
    except RuntimeError as e:  # YOLO 등에서 발생할 수 있는 런타임 오류 (예: CUDA 메모리 부족)
        app.logger.error(f"처리 중 런타임 오류: {e}", exc_info=True)
        return jsonify({'error': f"처리 오류: {str(e)}"}), 500
    except Exception as e:  # 그 외 모든 예외 처리
        app.logger.error(f"예기치 않은 오류 발생: {e}", exc_info=True)  # exc_info=True로 스택 트레이스 로깅
        return jsonify({'error': f'예기치 않은 오류가 발생했습니다: {str(e)}'}), 500


if __name__ == '__main__':
    # 서버 시작 전 필수 요소 확인
    if not all([GOOGLE_API_KEY != "YOUR_GOOGLE_API_KEY_FALLBACK",
                OPENAI_API_KEY != "YOUR_OPENAI_API_KEY_FALLBACK",
                yolo_model, gemini_model, openai_client]):
        print("ERROR: 하나 이상의 API 키 또는 모델이 올바르게 설정되지 않았습니다. 애플리케이션이 정상적으로 작동하지 않을 수 있습니다.")

    # Flask 내장 서버를 사용.
    app.run(host='0.0.0.0', port=5000, debug=True)