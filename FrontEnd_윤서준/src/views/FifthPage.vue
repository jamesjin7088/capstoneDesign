<template>
  <div class="container">
    <!-- 상단 내비게이션 -->
    <div class="title">
      <h3 @click="goToMainPage" class="clickable_title">Neural Network</h3>
    </div>
    <hr />
      
    <!-- 제목 및 진행 바 -->
    <div class="bowl">
      <div class="text">
        <h2>4. 결과</h2>
        <p>Step 4 of 4</p>
      </div>
      
      <!-- 진행 바 -->
      <div class = "progress-container">
        <div class="progress_bar">
          <div class="progress"></div>
        </div>
      </div> 

  
      <!-- 결과 카드 -->
      <div class="result-card">
        <div class="images">

          <div class="image-section">
            <p>원본</p>
            <img v-if="uploadedImage" :src="uploadedImage" alt="Uploaded Room" class="uploaded_image" />
          </div>
          
          <div class="image-section">
            <p>변환됨</p>
            <img v-if="uploadedImage" :src="uploadedImage" alt="Uploaded Room" class="uploaded_image" />
          </div>
        </div>
    
        <!-- 액션 버튼 -->
        <div class="button-row">
          <button class="action-button download">⬇ 다운로드</button>
          <button class="action-button share">🔗 공유하기</button>
        </div>
    
        <button class="retry-button">✏️ 프롬프트 수정하고 다시 시도하기</button>

    
        <!-- 버튼 영역 -->
        <div class="bottom_buttons">
          <button @click="$router.push('/fourth')" class="prev_button">← Previous</button>
        </div>
      </div>
    </div>
  </div>
</template>


<script>
export default {
  data() {
    return {
      uploadedImage: null,
    };
  },

  mounted() {
    // 이미지 불러오기
    const savedImage = localStorage.getItem('uploadedImage');
    if (savedImage) {
      this.uploadedImage = savedImage;
    }
  },
  
  methods: {
    goToMainPage() {
      this.$router.push('/');
    },
  },
};
</script>



  
  
<style scoped>
  .container {
    background-color: #0f172a;
  }

  .title {
    padding-left: 150px;   /* 좌측 padding 크기 */
  
    background-color: #121826; /* padding 내부 배경색 */
    border-top: 10px solid #121826; /* 상단 border 크기 */
    border-bottom: 10px solid #121826; /* 하단 border 크기 */
  
    color: #bcb0da;
  }
  /* 제목 스타일 */
  .clickable_title {
    cursor: pointer;
    transition: color 0.3s ease;
    font-weight: bold;
  }

  .clickable_title:hover {
    color: #8A2BE2;
  }


    /* 컨테이너 */
  .bowl {
    background-color: #0f172a;
    color: white;
    padding: 40px;
    min-height: 100vh;
  }

  .text {
    display: flex;
    justify-content: space-between;
    align-items: center;
  }

  /* 진행 바 */
  .progress-container {
      margin-top: 10px;
      width: 100%;
      padding-bottom: 30px;
    }
  .progress_bar {
    background: #2c3e50;
    height: 5px;
    border-radius: 5px;
    overflow: hidden;
  }
  .progress {
    width: 100%;
    height: 100%;
    background: #6A0DAD;
    border-radius: 5px;
  }
  
  /* 결과 창 */
  .result-card {
    background: #1e293b;
    padding: 24px;
    padding-top: 20px;
    border-radius: 16px;
    text-align: center;
  }
  
  .images {
    display: flex;
    flex-wrap: wrap; /* 한 줄에 안 들어가면 아래로 내림 */
    justify-content: center;
    gap: 20px;
    margin-bottom: 20px;
  }

  .image-section {
    flex: 1 1 300px; /* 최소 너비 300px, 넘으면 자동 줄어듦 */
    max-width: 400px;
    text-align: center;
  }
  
  .image-section p {
    margin-bottom: 10px;
    background-color: #334155;
    
    padding-left: 30px;
    padding-right: 30px;
    padding-top: 5px;
    padding-bottom: 5px;
    border-radius: 10px;
    font-weight: bold;
  }
  
  .image-section img {
    max-width: 100%;
    height: auto;
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
  
  /* 하단 버튼 */
  .bottom_buttons {
    display: flex;
    justify-content: space-between;
    margin-top: 30px;
  }
  /* 이전 버튼 */
  .prev_button { 
    background: #475569;
    color: white;
    padding: 10px 18px;
    border: none;
    border-radius: 6px;
    cursor: pointer;
    font-weight: 600;
    transition: 0.3s;
  }
  .prev_button:hover {
    background: #d3d3d3;
  }

  /* 그 외 사항 */
  h3, h4, h5 {
    margin: 0; /* 기본 여백 제거 */
  }
  
  hr {
    border: 0; /* 기본 테두리 제거 */
    height: 1px; /* 선의 높이 설정 */
    background-color: #2a0860; /* 배경색 설정 */
    border-top: 1px solid #5a5a5a; /* 선의 색상 설정 */
  }
</style>