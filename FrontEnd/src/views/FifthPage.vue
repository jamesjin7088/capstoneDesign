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
        <p>Step 3 of 3</p>
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
            <p>원본 이미지</p>
            <img v-if="uploadedImage" :src="uploadedImage" alt="Uploaded Room" class="uploaded_image" />
          </div>
          

        </div>
    

        <!-- 수정된 목록 가구 이미지 보여주기 -->
        <div class="furniture-section">
          <!--<p>추천 스타일</p>-->
          

          <div class="info_card" v-if="responseMessage_style">
            <h2>이미지 분석 결과</h2>
            <p>💡 현재 스타일 : {{ responseMessage_style }}</p>
            <p>💡 추천 가구 : {{ Result_Furniture }}</p>
            <p>💡 방의 유형 : {{ responseMessage_room_type }}</p>
          </div>

          
          <!-- 🔽 추가된 추천 이미지 목록 영역 -->
          <p>추천 가구 리스트</p>
          <div class="furniture-box">  
            <div class="furniture-title">예시 사진</div>
            <div class="image-list">
              <div class="image-item" v-for="(img, index) in furnitureImages" :key="index">
                <img :src="img" alt="Furniture Option" />
                <img v-if="responseMessage_created_image" :src="responseMessage_created_image" alt="Uploaded Room" class="uploaded_image" />
              </div>
            </div>
          </div>
        </div>
    

    
        <!-- 버튼 영역 -->
        <div class="bottom_buttons">
          <button @click="$router.push('/third')" class="prev_button">← Previous</button>
        </div>
      </div>
    </div>
  </div>
</template>


<script>
import { FullscreenIcon } from 'lucide-vue-next';

export default {
  data() {
    return {
      uploadedImage: null,
      Result_Image: null,
      Result_Furniture: '',
      
      responseMessage_style: '', // 서버 이미지 스타일
      responseMessage_room_type: '', // 방의 유형
      responseMessage_created_image: '', // 생성된 이미지

      // 가구 이미지 예시 (로컬 혹은 URL 사용 가능)
      furnitureImages: [
      'src/assets/furniture/chair/chair1.jpg',
      'src/assets/furniture/chair/chair2.png',
      'src/assets/furniture/chair/chair3.jpg',
      'src/assets/furniture/chair/chair4.png',
      'src/assets/furniture/desk/desk1.png',
      ]
    };
  },

  mounted() {
    // 이미지 불러오기
    const savedImage = localStorage.getItem('uploadedImage');
    if (savedImage) {
      this.uploadedImage = savedImage;
    }

    const designResult = localStorage.getItem('responseResult');
    if (designResult) {
      this.Result_Image = designResult;
    }


    // 이미지 스타일 출력
    const message_style = localStorage.getItem('responseMessage_style');
    if (message_style) {
      this.responseMessage_style = message_style;
    }
    // 사용된 가구
    const FurnitureResult = localStorage.getItem('responseMessage_furniture');
    if (FurnitureResult) {
      this.Result_Furniture = FurnitureResult;
    }
    // 방의 유형
    const RoomType = localStorage.getItem('responseMessage_room_type');
    if (RoomType) {
      this.responseMessage_room_type = RoomType;
    }
    // 생성된 이미지
    const created_image = localStorage.getItem('responseMessage_created_image');
    if (created_image) {
      this.responseMessage_created_image = created_image;
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

  .uploaded_image {
  width: 60%;
  max-width: 600px;  /* 원하는 최대 너비 */
  height: auto;
  border-radius: 10px;
  margin: 0 auto;
  display: block;
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

  .furniture-section p {
    margin-bottom: 10px;
    background-color: #334155;
    
    padding-left: 30px;
    padding-right: 30px;
    padding-top: 5px;
    padding-bottom: 5px;
    border-radius: 10px;
    font-weight: bold;
  }

  /* 추천 스타일 */
.info_card {
  padding: 15px;
  background-color: #334155;
  color: white;
  border-radius: 10px;
  margin-bottom: 20px;
  /*text-align: left;*/
  font-weight: 500;
}


  /* 수정 부분 가구 이미지 */
.image-list {
  display: flex;
  justify-content: space-between;
  flex-wrap: wrap;
  margin-top: 20px;
  gap: 10px;
}

.image-item {
  flex: 1 1 18%;
  max-width: 18%;
  text-align: center;
}

.image-item img {
  width: 100%;
  border-radius: 10px;
  box-shadow: 0 2px 10px rgba(0,0,0,0.2);
}

/* 가구 박스 전체 */
.furniture-box {
  background-color: #1e293b;
  border: 2px solid #64748b;
  border-radius: 20px;
  padding: 20px;
  margin-top: 20px;
}

/* '의자' 제목 박스 */
.furniture-title {
  text-align: center;
  font-weight: bold;
  font-size: 20px;
  background-color: #334155;
  color: white;
  padding: 10px 0;
  border-radius: 10px 10px 0 0;
  margin-bottom: 20px;
}

/* 이미지 리스트 스타일 */
.image-list {
  display: flex;
  justify-content: space-between;
  flex-wrap: wrap;
  gap: 10px;
}

.image-item {
  flex: 1 1 18%;
  max-width: 18%;
  text-align: center;
}

.image-item img {
  width: 100%;
  border-radius: 10px;
  box-shadow: 0 2px 10px rgba(0,0,0,0.2);
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