<template>
  <div class="container">
    <div class="title">
        <h3 @click="goToMainPage" class="clickable_title">Neural Network</h3>
    </div>
    <hr />

    <!-- 제목 및 진행 바 -->
    <div class="bowl">
      <div class="text">
        <h2>2. 이미지 분석</h2>
        <p>Step 2 of 3</p>
      </div>
    
        <!-- 진행 바 -->
      <div class = "progress-container">
        <div class="progress_bar">
          <div class="progress"></div>
        </div>
      </div>  

      <!--<div class="content_container"> -->
      <div class="content">
        <!-- 이미지 업로드 영역 -->
        <div class="image_section">
          <!--SecondPage 에서 가져온 이미지-->
          <img v-if="uploadedImage" :src="uploadedImage" alt="Uploaded Room" class="uploaded_image" />
          <p v-else>업로드된 이미지가 없습니다.</p> 
          <!--<img src="@/assets/images/chair.png" alt="Uploaded Room Image" class="uploaded_image"> -->
        </div>

        <!-- 감지된 정보 -->
        <div class="info_section">
          <div class="info_card">
            <h4>🪑 감지된 가구</h4>
            <ul>
              <!-- 백엔드 메세지 출력 -->
              <li>
                <p v-if="responseMessage">{{ responseMessage }}</p>
              </li>
            </ul>
          </div>

          <div class="info_card">
            <h4>🎨 색상 팔레트</h4>
            <div class="color_palette">
              <div class="color_circle" :style="{ background: responseMessage_color1 }"></div>
              <div class="color_circle" :style="{ background: responseMessage_color2 }"></div>
              <div class="color_circle" :style="{ background: responseMessage_color3 }"></div>
            </div>
          </div>

          <div class="info_card">
            <h4>💡 현재 스타일</h4>
            <p v-if="responseMessage_style">{{ responseMessage_style }}</p>
          </div>
        </div>
      </div>

      <!-- 버튼 영역 -->
      <div class="bottom_buttons">
        <button @click="$router.push('/second')" class="prev_button">← Previous</button>
        <button @click="$router.push('/fifth')" class="next_button">Next →</button>
      </div>
    </div>
  </div>
</template>


<script>
export default {
  data() {
    return {
      uploadedImage: null,
      responseMessage: '', // 서버 응답 메세지
      responseMessage_style: '', // 서버 이미지 스타일
      responseMessage_color1: '', // 서버 색상 정보
      responseMessage_color2: '',
      responseMessage_color3: '',
    };
  },

  mounted() {
    // 이미지 불러오기
    const savedImage = localStorage.getItem('uploadedImage');
    if (savedImage) {
      this.uploadedImage = savedImage;
    }

    // 서버 메세지 불러오기
    const message = localStorage.getItem('responseMessage');
    if (message) {
      this.responseMessage = message;
    }
    const message_style = localStorage.getItem('responseMessage_style');
    if (message_style) {
      this.responseMessage_style = message_style;
    }

    // 색상값 가져오기
    const color_1 = localStorage.getItem('responseMessage_color1');
    if (color_1) {
      this.responseMessage_color1 = color_1 || '#ffffff';
    }
    const color_2 = localStorage.getItem('responseMessage_color2');
    if (color_2) {
      this.responseMessage_color2 = color_2 || '#ffffff';
    }
    const color_3 = localStorage.getItem('responseMessage_color3');
    if (color_3) {
      this.responseMessage_color3 = color_3 || '#ffffff';
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
/* 전체 레이아웃 스타일 */
.container {
  background-color: #121826;
  color: white;
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
  font-family: 'Noto Sans KR', sans-serif;
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
  }
.progress_bar {
  background: #2c3e50;
  height: 5px;
  border-radius: 5px;
  overflow: hidden;
}
.progress {
  width: 66%;
  height: 100%;
  background: #6A0DAD;
  border-radius: 5px;
}

.content_container {
  display: flex;
  justify-content: center;
  align-items: center;
  width: 100%;
}
/* 콘텐츠 영역 스타일 */
.content {
  margin-top: 30px;
  border: 2px;
  border-radius: 10px;
  text-align: center;
  padding: 20px;
  gap: 20px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 18px;
  background: #27303f;
}

/* 이미지 섹션 */
.image_section {
  flex: 1;
  
}

.uploaded_image {
  width: 100%;
  border-radius: 12px;
}

/* 정보 섹션 */
.info_section {
  flex: 1;
  display: flex;
  flex-direction: column;
  gap: 15px;
}

.info_card {
  background: #1d2735;
  padding: 15px;
  border-radius: 10px;
}

.info_card h4 {
  margin-bottom: 5px;
}

/* 색상 팔레트 */
.color_palette {
  display: flex;
  gap: 10px;
}

.color_circle {
  width: 20px;
  height: 20px;
  border-radius: 50%;
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
/* 다음 버튼 */
.next_button {
  padding: 10px 18px;
  border: none;
  background: #6A0DAD;
  color: white;
  cursor: pointer;
  border-radius: 5px;
  font-weight: bold;
  transition: 0.3s;
}
.next_button:hover {
  background: #8A2BE2;
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