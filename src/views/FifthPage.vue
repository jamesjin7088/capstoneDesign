<template>
    <div class="result-page">
      <!-- 상단 내비게이션 -->
      <header class="header">
        <h1>🖌️ AI 디자인 스튜디오</h1>
        <nav class="nav-links">
          <button class="nav-button">🏠 홈</button>
          <button class="nav-button active">🧱 스튜디오</button>
          <button class="nav-button">🖼️ 갤러리</button>
        </nav>
      </header>
  
      <!-- 결과 헤더 -->
      <div class="section-header">
        <h2>Result</h2>
        <p class="step-indicator">Step 4 of 4</p>
      </div>
      <div class="progress-bar">
        <div class="progress-fill"></div>
      </div>
  
      <!-- 결과 카드 -->
      <div class="result-card">
        <div class="images">
          <div class="image-section">
            <p>원본</p>
            <img src="@/assets/images/pillow.png">
          </div>
          <div class="image-section">
            <p>변환됨</p>
            <img src="@/assets/images/pillow.png">
          </div>
        </div>
  
        <!-- 액션 버튼 -->
        <div class="button-row">
          <button class="action-button download">⬇ 다운로드</button>
          <button class="action-button share">🔗 공유하기</button>
        </div>
  
        <button class="retry-button">✏️ 프롬프트 수정하고 다시 시도하기</button>
      </div>
  
      <!-- 이전 버튼 -->
      <div class="footer">
        <button @click="$router.push('/step3')" class="nav-button">← Previous</button>
      </div>
    </div>
  </template>
  
  
  <style scoped>
  .result-page {
    background-color: #0f172a;
    color: white;
    padding: 30px;
    min-height: 100vh;
    font-family: 'Noto Sans KR', sans-serif;
  }
  
  .header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 30px;
  }
  
  .nav-links {
    display: flex;
    gap: 12px;
  }
  
  .nav-button {
    background: #1e293b;
    color: white;
    padding: 8px 14px;
    border-radius: 6px;
    font-weight: 600;
    border: none;
    cursor: pointer;
  }
  
  .nav-button.active {
    background-color: #a855f7;
  }
  
  .section-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
  }
  
  .section-header h2 {
    font-size: 22px;
    font-weight: bold;
  }
  
  .step-indicator {
    font-size: 14px;
    color: #94a3b8;
  }
  
  .progress-bar {
    height: 4px;
    background: #334155;
    margin: 10px 0 20px;
    border-radius: 2px;
  }
  
  .progress-fill {
    width: 100%;
    height: 100%;
    background: #a855f7;
    border-radius: 2px;
  }
  
  .result-card {
    background: #1e293b;
    padding: 24px;
    border-radius: 16px;
    text-align: center;
  }
  
  .images {
    display: flex;
    justify-content: space-around;
    margin-bottom: 20px;
  }
  
  .image-section {
    display: flex;
    flex-direction: column;
    align-items: center;
  }
  
  .image-section p {
    margin-bottom: 10px;
    font-size: 14px;
  }
  
  .image-section img {
    width: 300px;
    border-radius: 10px;
    box-shadow: 0 2px 10px rgba(0,0,0,0.3);
  }
  
  .button-row {
    display: flex;
    justify-content: space-around;
    margin: 16px 0;
  }
  
  .action-button {
    flex: 1;
    margin: 0 10px;
    padding: 12px;
    font-weight: bold;
    border: none;
    border-radius: 10px;
    color: white;
    cursor: pointer;
    transition: 0.3s;
  }
  
  .download {
    background-color: #a855f7;
  }
  
  .share {
    background-color: #334155;
  }
  
  .retry-button {
    margin-top: 10px;
    background-color: #334155;
    border: none;
    color: white;
    padding: 10px;
    width: 100%;
    border-radius: 10px;
    cursor: pointer;
  }
  
  .footer {
    margin-top: 30px;
    text-align: left;
  }
</style>