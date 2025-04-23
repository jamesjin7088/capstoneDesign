import "./Home.css";

import { useState } from "react";
import axios from "axios";

export default function Home() {
  const [selectedImage, setSelectedImage] = useState(null);
  const [previewUrl, setPreviewUrl] = useState(null);
  const [prompt, setPrompt] = useState("");

  // 이미지 업로드
  const handleImageUpload = async (event) => {
    const file = event.target.files[0];
    if (file) {
      // 로컬 상태 업데이트
      setSelectedImage(file);
      const imageUrl = URL.createObjectURL(file);
      setPreviewUrl(imageUrl);

      // FormData를 직접 생성하여 전송
      const formData = new FormData();
      formData.append("file", file);

      try {
        const response = await axios.post(
          "http://127.0.0.1:8000/image",
          formData,
          {
            headers: {
              "Content-Type": "multipart/form-data",
            },
          }
        );
        // 성공 처리
        console.log(response);
      } catch (error) {
        console.error("에러 상세 정보:", error.response?.data);
        alert("이미지 업로드 중 오류가 발생했습니다.");
        // 에러 처리
      }
    }
  };

  const handlePrompt = (e) => {
    setPrompt(e.target.value);
  };

  //   const handleSubmitImage = () => {

  //   }

  return (
    <div className="Home">
      <input type="file" accept="image/*" onChange={handleImageUpload} />

      {previewUrl && (
        <div>
          <h3>이미지 생성 결과 : </h3>
          <img src={previewUrl} />
          {selectedImage && (
            <div>
              <p>파일 이름: {selectedImage.name}</p>
              <p>파일 크기: {(selectedImage.size / 1024).toFixed(2)} KB</p>
              <p>파일 이름: {selectedImage.type}</p>
            </div>
          )}
        </div>
      )}

      <input
        value={prompt}
        type="text"
        placeholder="프롬프트를 입력하세요."
        onChange={handlePrompt}
      ></input>
      <button>이미지 생성하기</button>
    </div>
  );
}
