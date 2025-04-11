<template>
  <div class = "container">
    <div class="title">
      <h3 @click="goToMainPage" class="clickable_title">Neural Network</h3>
    </div>
    <hr />

    <div class="bowl">
      <div class="text">
        <h2>1. 방 이미지 업로드</h2>
        <p>Step 1 of 4</p>
      </div>
    
      <!-- 진행 바 -->
      <div class="progress_bar">
        <div class="progress"></div>
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

      <!-- 이전 페이지 버튼 -->
      <div class="button_container">
        <button @click="$router.push('/')" class="prev_button">← 이전 페이지</button>
        <button @click="$router.push('/third')" class="next_button">다음 페이지 -></button>
      </div>
    </div>
  </div>
</template>


<script>
export default {
  data() {
    return {
      selectedFile: null,
      image: null,
      uploadedFileName: null, // 파일 이름 확인
      isDragging: false, // 드래그 상태 추적
    };
  },

  methods: {
    // 메인 페이지로 이동
    goToMainPage() {
      this.$router.push('/');
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
          // 다른 vue 폴더로 이미지 이동
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


body {
  font-family: Arial, sans-serif;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  height: 100vh;
  width: 100vw;
  margin: 0;
  background: #121826;
  color: #FFFFFF;
}

/* 컨테이너 */
.bowl {
  width: 100%;
  height: 100%;
  max-width: 100vw;
  max-height: 100vh;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  background: #121826;
  border-bottom: 270px solid #121826;
  border-radius: 12px;
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.3);
  color: white;
}

.text {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

/* 진행 바 */
.progress_bar {
  width: 65%;
  height: 5px;
  background: #485874;
  border-radius: 5px;
  position:relative;
  margin-bottom: 20px;
}
.progress {
  width: 25%;
  height: 100%;
  background: #6A0DAD;
  border-radius: 5px;
}

/* 업로드 박스 */
.upload_box {
  width: 60%;
  height: 50%;
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

/* 버튼 컨테이너 */
.button_container {
  padding-top: 30px;
  bottom: 20px;
  left: 20px;

  display: flex;
  justify-content: space-between;
}

/* 이전 버튼 */
.prev_button { 
  padding: 10px 15px;
  border: none;
  background: #9c9c9c;
  color: black;
  cursor: pointer;
  border-radius: 5px;
  font-weight: bold;
  transition: 0.3s; 
  margin-right: 560px; /* 오른쪽 간격 추가 */
}
.prev_button:hover {
  background: #d3d3d3;
}

/* 다음 버튼 */
.next_button {
  padding: 10px 15px;
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