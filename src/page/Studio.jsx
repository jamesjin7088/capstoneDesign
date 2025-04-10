import "./Studio.css";

const Studio = () => {
  return (
    <div className="Studio">
      <div>
        <section className="section1">
          <div className="section1-1">
            <h2>Upload Image</h2>
            <span>Step 1 of 4</span>
          </div>
          <div className="section1-2"></div>
        </section>
        <section className="section2">
          <div>
            <input type="file" accept="image/*" id="fileInput" />
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
                className="lucide lucide-upload w-12 h-12 mx-auto mb-4 text-gray-400"
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
        <section className="section3">
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
              className="lucide lucide-chevron-left w-5 h-5"
            >
              <path d="m15 18-6-6 6-6"></path>
            </svg>
            <span>Previous</span>
          </button>
        </section>
      </div>
    </div>
  );
};

export default Studio;
