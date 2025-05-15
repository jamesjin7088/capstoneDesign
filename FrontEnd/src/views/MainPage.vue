<template>
  <div class = "container">
    <div class="title">
      <h3>Neural Network</h3>
    </div>
    <hr />
  
    <div class="main_text">
      <h1>머신러닝 기반 가구 추천 서비스</h1>
    </div>

    <div class = "main_text_sub">
      <h4>방 사진만 업로드하면, 어울리는 가구를 추천해드립니다!</h4>
    </div>
    <div class = "main_text_sub2">
      <h4>간편하게 알아보세요.</h4>
    </div>

    <!-- 이미지 업로드 버튼을 추천 내용 위로 이동 -->
    <div class="start_button">
      <!-- 시작하기 누르면 router로 다음 사이트로 이동 -->
      <button @click="$router.push('/second')" class="btn_start">시작하기</button>
    </div>

    <div class="usage">
      <h2>이용 방법</h2>
      <div class="usage_steps">
        <div class="step">
          <h4>01</h4>
          <h4>이미지 업로드</h4>
          <h5>버튼을 눌르고 방 이미지를 업로드하세요.</h5>
        </div>
        <div class="step">
          <h4>02</h4>
          <h4>가구추천 시작</h4>
          <h5>업로드 이미지를 확인하고 실행 해보세요.</h5>
        </div>
        <div class="step">
          <h4>03</h4>
          <h4>생성 및 공유</h4>
          <h5>나온 결과를 보고 공유해보세요.</h5>
        </div>
      </div>
    </div>
      

  </div>
  
</template>


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
  font-weight: bold;
}

.main_text {
  background-color: #121826; /* padding 내부 배경색 */
  border-top: 15px solid #121826; /* 상단 border 크기 */
  color: #b578c5;
  box-sizing: border-box; /* padding과 border 포함하여 요소 크기 계산 */

  display: flex; /* 플렉스를 사용하여 중앙 정렬 */
  flex-direction: column; /* 세로 방향으로 정렬 */
  align-items: center; /* 수평 중앙 정렬 */
  justify-content: flex-start; /* 콘텐츠가 위에서부터 배치되도록 설정 */
}

.main_text_sub,
.main_text_sub2 {
  color: #e8e3f3;

  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: flex-start; /* 상단 정렬 */
  
  margin: 0; /* 기본 여백 제거 */
  padding: 0; /* 기본 패딩 제거 */
}

.start_button {
  border-top: 20px solid #121826; /* 상단 border 크기 */
  border-bottom: 50px solid #121826; /* 상단 border 크기 */

  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: flex-start; /* 상단 정렬 */
}
.btn_start {
  cursor: pointer;
}

/* 사용 방법 부분 */
.usage {
  color: rgb(234, 234, 234);
  background-color: #1e293b; /* 배경색 설정 */
  
  border-top: 30px solid #121826; /* 상단 border 크기 */
  border-bottom: 200px solid #121826; /* 상단 border 크기 */
  border-left: 150px solid #121826;
  border-right: 150px solid #121826;

  padding: 20px;
}

.usage_steps {
  display: flex;
  justify-content: space-between;
  gap: 30px;
  margin-top: 20px;
}

/* 각 step 박스 */
.step {
  background-color: #28374f;
  padding: 20px;
  border-radius: 12px;
  flex: 1;
  text-align: center;
  color: white;
}
/* 숫자 강조 */
.step h4:first-child {
  color: #a78cff;
  font-size: 20px;
  font-weight: bold;
  margin-bottom: 10px;
}
/* 설명 부분 */
.step h5 {
  color: #959595;
  font-size: 14px;
  margin-top: 8px;
}

/* 반응형: 작은 화면일 때 세로 정렬 */
@media (max-width: 768px) {
  .usage_steps {
    flex-direction: column;
    align-items: center;
  }

  .step {
    width: 100%;
  }
}
/* */

/* 버튼 디자인 */
.btn_start {
  background-color: #7134b2; /* 배경색 설정 */
  color: rgb(234, 234, 234);

  padding-top: 10px;
  padding-bottom: 10px;
  padding-left: 20px;
  padding-right: 20px;

  border: none;
  border-radius: 5px;

  font-weight: bold;
  transition: 0.3s; 
}
.btn_start:hover {
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