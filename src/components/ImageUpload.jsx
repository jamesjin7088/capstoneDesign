import { useState } from "react";
import "./ImageUpload.css";

export default function ImageUpload() {
  const [uploadedImage, setUploadedImage] = useState(null);

  const handleImageUpload = (e) => {
    const file = e.target.files[0];
    if (!file) return;

    const reader = new FileReader();
    reader.onload = () => {
      setUploadedImage({
        name: file.name,
        dataUrl: reader.result,
      });
    };
    reader.readAsDataURL(file);
  };
  
  if (!uploadedImage) {
    return (
      <div className="notUploaded">
        <section className="section1">
          <div>
            <input
              type="file"
              accept="image/*"
              id="fileInput"
              onChange={handleImageUpload}
            />
            <label htmlFor="fileInput">
              <svg
                xmlns="http://www.w3.org/2000/svg"
                width="24"
                height="24"
                viewBox="0 0 24 24"
                fill="none"
                stroke="currentColor"
                strokeWidth="2"
                strokeLinecap="round"
                strokeLinejoin="round"
              >
                <path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"></path>
                <polyline points="17 8 12 3 7 8"></polyline>
                <line x1="12" x2="12" y1="3" y2="15"></line>
              </svg>
              <p className="p1">이미지를 드래그하여 업로드하세요</p>
              <p className="p2">또는 클릭하여 파일 선택</p>
            </label>
          </div>
        </section>
        <section className="section2">
          <button>
            <svg
              xmlns="http://www.w3.org/2000/svg"
              width="24"
              height="24"
              viewBox="0 0 24 24"
              fill="none"
              stroke="currentColor"
              strokeWidth="2"
              strokeLinecap="round"
              strokeLinejoin="round"
            >
              <path d="m15 18-6-6 6-6"></path>
            </svg>
            <span>Previous</span>
          </button>
        </section>
      </div>
    );
  }

  return (
    <div>
      <div className="uploaded">
        <section className="section1">
          <div>
            <div>
              <img src={uploadedImage.dataUrl} className="img" />
            </div>

            <div className="imageFeature">
              <div>
                <div>
                  <h3>감지된 가구</h3>
                </div>
                <ul>
                  <li>모던 소파</li>
                  <li>커피 테이블</li>
                  <li>플로어 램프</li>
                  <li>벽걸이 아트</li>
                </ul>
              </div>

              <div>
                <div>
                  <h3>색상 팔레트</h3>
                </div>
              </div>

              <div>
                <div>
                  <h3>현재 스타일</h3>
                </div>
                <p>스칸디나비안 영향을 받은 모던 미니멀리즘</p>
              </div>
            </div>
          </div>
          <button>
            <span>디자인 커스터마이징으로 계속하기</span>
          </button>
        </section>
      </div>
      <section className="uploaded_button">
        <button>
          <svg
            xmlns="http://www.w3.org/2000/svg"
            width="24"
            height="24"
            viewBox="0 0 24 24"
            fill="none"
            stroke="currentColor"
            strokeWidth="2"
            strokeLinecap="round"
            strokeLinejoin="round"
          >
            <path d="m15 18-6-6 6-6"></path>
          </svg>
          <span>Previous</span>
        </button>
        <button>
          <span>Next</span>
          <svg
            xmlns="http://www.w3.org/2000/svg"
            width="24"
            height="24"
            viewBox="0 0 24 24"
            fill="none"
            stroke="currentColor"
            strokeWidth="2"
            strokeLinecap="round"
            strokeLinejoin="round"
          >
            <path d="m9 18 6-6-6-6"></path>
          </svg>
        </button>
      </section>
    </div>
  );
}
