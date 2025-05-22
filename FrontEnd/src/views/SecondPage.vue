<template>
  <div class = "container">
    <div class="title">
      <h3 @click="goToMainPage" class="clickable_title">Neural Network</h3>
    </div>
    <hr />

    <div class="bowl">
      <div class="text">
        <h2>1. 방 이미지 업로드</h2>
        <p>Step 1 of 3</p>
      </div>
    
      <!-- 진행 바 -->
      <div class = "progress-container">
        <div class="progress_bar">
          <div class="progress"></div>
        </div>
      </div>  
        
      <!-- 업로드 박스 -->
      <div 
        class="upload_box" 
        :class="{ 'drag-active': isDragging }"
        @dragover.prevent="onDragOver" 
        @dragleave="onDragLeave" 
        @drop.prevent="onDrop"
        @click="triggerFileInput"
      >
      <p v-if="uploadedFileName">{{ uploadedFileName }}</p>
      <p v-else>이미지를 드래그하여 업로드하세요<br>또는 클릭하여 파일 선택</p>

        <input
          ref="fileInput"
          type="file"
          accept="image/*"
          @change="handleFileChange"
          style="display: none"
        />
      </div>

      <!-- 페이지 버튼 -->
      <div class="bottom_buttons">
        <button @click="$router.push('/')" class="prev_button">← 이전 페이지</button>
        <button @click="handleNextClick" class="next_button" >다음 페이지 -></button>
      </div>
    </div>
  </div>
</template>


<script>
export default {
  data() {
    return {
      selectedFile: null, // 하나의 선택된 파일
      image: null,
      uploadedFileName: null, // 파일 이름 확인
      isDragging: false, // 드래그 상태 추적

      showRecommendedImages: false, // 추천 이미지 표시 여부
      isImageUploaded: false, // 이미지 업로드 여부 체크

      responseMessage_style: '', // 서버에서 받은 이미지 스타일 정보
      responseMessage_detected: '', // 감지된 가구
      responseMessage_color1: '', // 서버에서 받은 색상 정보 저장
      responseMessage_color2: '',
      responseMessage_color3: '',
      responseMessage_furniture: '', // 가구 추천 저장 변수
      responseMessage_room_type: '', // 방의 유형
      responseMessage_created_image: '', // 생성된 이미지
      
      resultImageUrl: '', // 서버에서 받은 이미지 url
    };
  },

  methods: {
    // 메인 페이지로 이동
    goToMainPage() {
      this.$router.push('/');
    },
    // 이미지 전송 후 다음페이지 이동
    async handleNextClick() {
      await this.uploadImage(); // 업로드 완료될 때까지 기다림
      this.$router.push('/third'); // 그 후에 이동
    },
    
    // 드롭창에 마우스 이동
    onDragOver(event) {
      this.isDragging = true;
    },
    // 드롭창에 마우스 없음
    onDragLeave(event) {
      this.isDragging = false;
    },
    
    // 이미지 드롭 시
    onDrop(event) {
      const files = event.dataTransfer.files;
      this.processFile(files[0]);
      this.isDragging = false;
    },  
    // 드롭창 클릭 시
    triggerFileInput() {
      this.$refs.fileInput.click();
    },
    // input으로 파일 선택했을 때
    handleFileChange(event) {
      const file = event.target.files[0];
      this.processFile(file);
    },

    // 파일 처리 공통 함수
    processFile(file) {
      if (file && file.type.startsWith('image/')) {
        this.selectedFile = file;
        this.uploadedFileName = file.name; // 이미지 파일이름 저장

        const reader = new FileReader();
        reader.onload = (e) => {
          this.image = e.target.result;

          // base64 이미지 localStorage에 저장
          // 서버에 이미지 전송
          localStorage.setItem('uploadedImage', this.image);
        };
        reader.readAsDataURL(file);
      } else {
        alert('이미지 파일만 선택 가능합니다!');
        this.selectedFile = null;
        this.uploadedFileName = null;
        this.image = null;
      }
    },

    // 선택된 이미지 업로드
    async uploadImage() {
        if (this.selectedFile) {
          const formData = new FormData();
          formData.append('image', this.selectedFile);
  
          // 혼자 테스트 할 때 사용함
          // 이미지 업로드 성공 시 "추천 이미지 보기" 버튼 활성화
          // this.isImageUploaded = true;
          
          try {
            // 'http://192.168.7.19:5000/upload'
            // 'http://192.168.12.107:8000/image'
            const response = await fetch('http://192.168.1.34:5000/upload', {
                method: 'POST',
                body: formData, // 그냥 이대로만!
                // ❌ headers 생략해야 함!
            });

            if (!response.ok) {
              const errorText = await response.text();
              console.error('서버 응답 오류:', response.status, errorText);
              return;
            }

            // 서버 url 받아오기
            const data = await response.json();
            this.resultImageUrl = data.result_image_url;
            console.log(this.resultImageUrl)

            
            // 팀원과 같이 테스트 할 시
            this.isImageUploaded = true; // 이미지 업로드 성공 시 상태 변경

            // 서버 응답 처리 (예: 메시지, 색상 가져오기)
            this.responseMessage_color1 = data.color_1;
            this.responseMessage_color2 = data.color_2;
            this.responseMessage_color3 = data.color_3;

            this.responseMessage_detected = data.message; // 감지된 가구
            this.responseMessage_style = data.message_style; // 스타일
            this.responseMessage_furniture = data.furniture; // 추천 가구 내용
            this.responseMessage_room_type = data.room_type; // 방의 유형
            this.responseMessage_created_image = data.image_url; // 생성된 이미지
            
            // 테스트 용도... 가구 변수가 저장되는지 확인용
            if (!this.responseMessage_furniture) {
              console.error('추천 가구 정보 없음!');
              return;
            }
            
            // Secondpage -> 다른 페이지 전송
            // 감지된 가구
            localStorage.setItem('responseMessage_detected', data.message);
            // 색상 팔레트
            localStorage.setItem('responseMessage_color1', data.color_1);
            localStorage.setItem('responseMessage_color2', data.color_2);
            localStorage.setItem('responseMessage_color3', data.color_3);
            // 가구 추천 리스트
            localStorage.setItem('responseMessage_furniture', data.furniture);
            // 현재 스타일
            localStorage.setItem('responseMessage_style', data.message_style);
            // 현재 스타일
            localStorage.setItem('responseMessage_room_type', data.room_type);
            // 생성된 이미지
            localStorage.setItem('responseMessage_created_image', data.image_url);
            

  
          } catch (error) {
            console.error('업로드 실패:', error);
            // 팀원과 같이 테스트 할 시
            this.isImageUploaded = false; // 실패 시 상태 초기화
          }
        } else {
          alert('이미지를 선택하세요!');
          
        }
      },
  }
};
</script>


<style scoped>
.container {
  background-color: #121826; /* padding 내부 배경색 */
}

.title {
  padding-left: 150px;   /* 좌측 padding 크기 */

  background-color: #121826; /* padding 내부 배경색 */
  border-top: 10px solid #121826; /* 상단 border 크기 */
  border-bottom: 10px solid #121826; /* 하단 border 크기 */

  color: #bcb0da;
}

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
  width: 33%;
  height: 100%;
  background: #6A0DAD;
  border-radius: 5px;
}

/* 업로드 박스 */
.upload_box {
  margin-top: 30px;
  border: 2px dashed #696868;
  border-radius: 10px;
  text-align: center;
  padding: 30px;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 20px;
  background: #27303f;
  transition: all 0.3s ease;
}
.upload_box:hover {
  border-color: #6A0DAD;
  background: #2f2f46;
  
}
/* 드래그 중일 때 */
.upload_box.drag-active {
  border-color: #6A0DAD;
  background: #2f2f46;
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