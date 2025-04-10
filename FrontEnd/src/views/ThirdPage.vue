<template>
  <div class="container">
    <div class="title">
        <h3 @click="goToMainPage" class="clickable_title">Neural Network</h3>
      </div>
    <hr />

    <!-- 제목 및 진행 바 -->
    <div class="header">
      <h3>Image Analysis</h3>
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
              <li>모던 소파</li>
              <li>커피 테이블</li>
              <li>플로어 램프</li>
              <li>벽걸이 아트</li>
            </ul>
          </div>

          <div class="info_card">
            <h4>🎨 색상 팔레트</h4>
            <div class="color_palette">
              <div class="color_circle" style="background: #dce4f2;"></div>
              <div class="color_circle" style="background: #e8eff8;"></div>
              <div class="color_circle" style="background: #baf4d4;"></div>
            </div>
          </div>

          <div class="info_card">
            <h4>💡 현재 스타일</h4>
            <p>스칸디나비안 영향을 받은 모던 미니멀리즘</p>
          </div>
        </div>
      </div>

      <!-- 버튼 영역 -->
      <div class="button_section">
        <button @click="$router.push('/second')" class="prev_button">← Previous</button>
        <button @click="$router.push('/fourth')" class="next_button">Next →</button>
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

.header {
  display: flex;
  flex-direction: column;
  align-items: center;
}

/* 진행 바 */
.progress_bar {
  width: 60%;
  height: 5px;
  background: #485874;
  border-radius: 5px;
  margin-top: 5px;
}

.progress {
  width: 50%;
  height: 100%;
  background: #8A2BE2;
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
  display: flex;
  justify-content: center;
  align-items: center;
  gap: 20px;
  width: 80%;
  margin: 40px auto 0; /* 가운데 정렬 + 위쪽 여백 */
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

/* 버튼 영역 */
.button_section {
  display: flex;
  justify-content: center;
  align-items: center;
  gap: 20px;
  width: 80%;
  margin: 40px auto 0; /* 가운데 정렬 + 위쪽 여백 */
}

.prev_button,
.next_button {
  padding: 10px 20px;
  border: none;
  border-radius: 5px;
  cursor: pointer;
  font-weight: bold;
  transition: 0.3s;
}

.prev_button {
  background: #9c9c9c;
  color: black;
}

.prev_button:hover {
  background: #d3d3d3;
}

.next_button {
  background: #6A0DAD;
  color: white;
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