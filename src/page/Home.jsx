import "./Home.css";
import { useNavigate } from "react-router-dom";

const Home = () => {
  const nav = useNavigate();

  const onChangePage = (page) => {
    nav(`/${page}`);
  };

  return (
    <div className="Home">
      <div>
        <section className="section1">
          <h1>AI로 이미지를 새롭게 디자인하세요</h1>
          <p>
            AI 기반 디자인의 힘을 경험해보세요. 이미지를 업로드하고 고급 스타일
            변환 기술로 멋진 작품으로 변환해보세요.
          </p>
          <button
            onClick={() => {
              onChangePage("studio");
            }}
          >
            <span>시작하기</span>
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
              className="lucide lucide-arrow-right w-5 h-5"
            >
              <path d="M5 12h14"></path>
              <path d="m12 5 7 7-7 7"></path>
            </svg>
          </button>
        </section>
        <section className="section2">
          <div>
            <div>
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
                className="lucide lucide-panels-top-left w-6 h-6 text-purple-400"
              >
                <rect width="18" height="18" x="3" y="3" rx="2"></rect>
                <path d="M3 9h18"></path>
                <path d="M9 21V9"></path>
              </svg>
            </div>
            <h3>다양한 스타일</h3>
            <p>
              다양한 예술 스타일 중에서 선택하거나 고급 프롬프트 시스템으로
              나만의 스타일을 만들어보세요.
            </p>
          </div>
          <div>
            <div>
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
                className="lucide lucide-wand2 w-6 h-6 text-purple-400"
              >
                <path d="m21.64 3.64-1.28-1.28a1.21 1.21 0 0 0-1.72 0L2.36 18.64a1.21 1.21 0 0 0 0 1.72l1.28 1.28a1.2 1.2 0 0 0 1.72 0L21.64 5.36a1.2 1.2 0 0 0 0-1.72Z"></path>
                <path d="m14 7 3 3"></path>
                <path d="M5 6v4"></path>
                <path d="M19 14v4"></path>
                <path d="M10 2v2"></path>
                <path d="M7 8H3"></path>
                <path d="M21 16h-4"></path>
                <path d="M11 3H9"></path>
              </svg>
            </div>
            <h3>AI 기술</h3>
            <p>
              최첨단 AI 기술을 활용하여 이미지의 본질은 유지하면서 새로운
              모습으로 변환합니다.
            </p>
          </div>
          <div>
            <div>
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
                className="lucide lucide-image w-6 h-6 text-purple-400"
              >
                <rect width="18" height="18" x="3" y="3" rx="2" ry="2"></rect>
                <circle cx="9" cy="9" r="2"></circle>
                <path d="m21 15-3.086-3.086a2 2 0 0 0-2.828 0L6 21"></path>
              </svg>
            </div>
            <h3>커뮤니티 갤러리</h3>
            <p>
              여러분의 작품을 공유하고 커뮤니티 갤러리에서 다른 사람들의 변환된
              이미지를 감상해보세요.
            </p>
          </div>
        </section>
        <section className="section3">
          <h2>이용 방법</h2>
          <div>
            <div>
              <h1>01</h1>
              <h3>이미지 업로드</h3>
              <p>변환하고 싶은 이미지를 업로드하세요.</p>
            </div>
            <div>
              <h1>02</h1>
              <h3>스타일 선택</h3>
              <p>프롬프트를 작성하여 원하는 스타일을 설정하세요.</p>
            </div>
            <div>
              <h1>03</h1>
              <h3>생성 및 공유</h3>
              <p>변환된 이미지를 생성하고 커뮤니티와 공유하세요.</p>
            </div>
          </div>
        </section>
      </div>
    </div>
  );
};

export default Home;
