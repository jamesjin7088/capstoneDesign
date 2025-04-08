<template>
    <div class = "container">
      <div class="title">
        <h3 @click="goToMainPage" class="clickable_title">Neural Network</h3>
      </div>
      <hr />
  
      <div class="bowl">
        <div class="text">
          <h2>1. 방 이미지 업로드</h2>
        </div>
      
        <!-- 진행 바 -->
        <div class="progress_bar">
          <div class="progress"></div>
        </div>
  
        <!-- 업로드 박스 -->
        <div 
          class="upload_box" 
          @dragover.prevent="onDragOver" 
          @dragleave="onDragLeave" 
          @drop.prevent="onDrop"
        >
          <p>이미지를 드래그하여 업로드하세요<br>또는 클릭하여 파일 선택</p>
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
    methods: {
      goToMainPage() {
        this.$router.push('/');
      },
      
      onDragOver(event) {
        event.currentTarget.style.borderColor = "#6A0DAD";
        event.currentTarget.style.background = "#333";
      },
      onDragLeave(event) {
        event.currentTarget.style.borderColor = "#bbb";
        event.currentTarget.style.background = "#252525";
      },
      // 파일을 드래그 드랍 시
      onDrop(event) {
        const files = event.dataTransfer.files;
        alert(`${files.length}개의 파일이 업로드되었습니다.`);
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
    border-bottom: 400px solid #121826;
    border-radius: 12px;
    box-shadow: 0 4px 10px rgba(0, 0, 0, 0.3);
    color: white;
  }
  
  .text {
    margin-right: 580px;
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
  
  /* 버튼 컨테이너 */
  .button_container {
    padding-top: 20px;
    bottom: 20px;
    left: 20px;
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