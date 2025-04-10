<template>
    <div class="customize-design-page">
      <!-- 제목 및 단계 -->
      <div class="top-header">
        <h2>Customize Design</h2>
        <p>Step 3 of 4</p>
      </div>
  
      <!-- 진행 바 -->
      <div class="progress-container">
        <div class="progress-bar">
          <div class="progress-fill"></div>
        </div>
      </div>
  
      <!-- 중앙 카드 영역 -->
      <div class="design-card">
        <h3>🖌️ 디자인 지시사항</h3>
        <p class="description">
          공간을 어떻게 변화시키고 싶은지 설명해주세요. 원하는 스타일, 색상, 또는 특별히 중점을 두고 싶은 요소들을 구체적으로 작성해주세요.
        </p>
        <textarea
          v-model="designInstructions"
          placeholder="예시: 이 공간을 따뜻한 자연색으로 꾸미고, 나무 가구와 식물을 추가하여 아늑한 모던한 공간으로 변화시켜주세요..."
        ></textarea>
  
        <!-- 프롬프트 팁 -->
        <div class="prompt-tips">
          <p><strong>프롬프트 작성 팁:</strong></p>
          <ul>
            <li>선호하는 스타일을 구체적으로 언급하세요</li>
            <li>원하는 색상 구성을 설명하세요</li>
            <li>변경하고 싶은 가구를 지정하세요</li>
            <li>원하는 분위기나 느낌을 포함하세요</li>
          </ul>
        </div>
  
        <button class="generate-button">디자인 생성하기</button>
      </div>
  
      <!-- 하단 버튼 -->
      <div class="bottom-buttons">
        <button @click="$router.push('/third')" class="nav-button">← Previous</button>
        <button @click="$router.push('/fifth')" class="nav-button next">Next →</button>
      </div>
    </div>
  </template>
  
  <script>
  export default {
    data() {
      return {
        designInstructions: "",
      };
    },
  };
  </script>
  
  <style scoped>
  .customize-design-page {
    background-color: #0f172a;
    color: white;
    padding: 40px;
    min-height: 100vh;
    font-family: 'Noto Sans KR', sans-serif;
  }
  
  .top-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
  }
  
  h2 {
    font-size: 24px;
    font-weight: bold;
  }
  
  .progress-container {
    margin-top: 10px;
    width: 100%;
  }
  
  .progress-bar {
    background: #2c3e50;
    height: 5px;
    border-radius: 5px;
    overflow: hidden;
  }
  
  .progress-fill {
    background: #a855f7;
    width: 75%;
    height: 100%;
  }
  
  .design-card {
    background: #1e293b;
    padding: 30px;
    border-radius: 12px;
    margin-top: 30px;
  }
  
  .description {
    margin-top: 8px;
    margin-bottom: 12px;
    color: #cbd5e1;
  }
  
  textarea {
    width: 100%;
    height: 130px;
    background: #334155;
    color: white;
    border: none;
    border-radius: 8px;
    padding: 12px;
    resize: none;
    font-size: 14px;
    margin-bottom: 20px;
  }
  
  .prompt-tips {
    background: #1e293b;
    border: 1px solid #475569;
    padding: 15px;
    border-radius: 8px;
    margin-bottom: 20px;
    font-size: 14px;
    color: #e2e8f0;
  }
  
  .prompt-tips ul {
    padding-left: 18px;
    margin-top: 6px;
  }
  
  .generate-button {
    background: #8b5cf6;
    color: white;
    padding: 12px 20px;
    border: none;
    border-radius: 8px;
    cursor: pointer;
    font-weight: bold;
    transition: 0.3s;
    width: 100%;
  }
  
  .generate-button:hover {
    background: #a78bfa;
  }
  
  .bottom-buttons {
    display: flex;
    justify-content: space-between;
    margin-top: 30px;
  }
  
  .nav-button {
    background: #475569;
    color: white;
    padding: 10px 18px;
    border: none;
    border-radius: 6px;
    cursor: pointer;
    font-weight: 600;
    transition: 0.3s;
  }
  
  .nav-button.next {
    background: #a855f7;
  }
  
  .nav-button:hover {
    opacity: 0.85;
  }
</style>