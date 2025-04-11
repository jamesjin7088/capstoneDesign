<template>
    <div class="bg-[#0f172a] text-white px-8 py-16">
      <!-- 상단 카드 영역 -->
      <div class="grid grid-cols-1 md:grid-cols-3 gap-8 max-w-6xl mx-auto mb-16">
        <FeatureCard
          title="다양한 스타일"
          description="다양한 예술 스타일 중에서 선택하거나 고급 프롬프트 시스템으로 나만의 스타일을 만들어보세요."
        />
        <FeatureCard
          title="AI 기술"
          description="최첨단 AI 기술을 활용하여 이미지의 본질은 유지하면서 새로운 모습으로 변환합니다."
        />
        <FeatureCard
          title="커뮤니티 갤러리"
          description="여러분의 작품을 공유하고 커뮤니티 갤러리에서 다른 사람들의 변환된 이미지를 감상해보세요."
        />
      </div>
  
      <!-- 이용 방법 -->
      <div class="max-w-6xl mx-auto">
        <h2 class="text-2xl font-bold mb-8">이용 방법</h2>
        <div class="grid grid-cols-1 md:grid-cols-3 gap-8">
          <HowToCard
            step="01"
            title="이미지 업로드"
            description="변환하고 싶은 이미지를 업로드하세요."
          />
          <HowToCard
            step="02"
            title="스타일 선택"
            description="프롬프트를 작성하여 원하는 스타일을 설정하세요."
          />
          <HowToCard
            step="03"
            title="생성 및 공유"
            description="변환된 이미지를 생성하고 커뮤니티와 공유하세요."
          />
        </div>
      </div>
    </div>
  </template>
  
  <script setup>
  import { defineComponent } from 'vue'
  
  const FeatureCard = defineComponent({
    props: ['title', 'description'],
    template: `
      <div class="bg-[#1e293b] p-6 rounded-xl flex flex-col gap-3">
        <h3 class="text-lg font-bold">{{ title }}</h3>
        <p class="text-sm text-gray-300">{{ description }}</p>
      </div>
    `
  })
  
  const HowToCard = defineComponent({
    props: ['step', 'title', 'description'],
    template: `
      <div class="bg-[#1e293b] p-6 rounded-xl">
        <p class="text-purple-400 font-bold text-lg">{{ step }}</p>
        <h4 class="text-white text-xl font-semibold mt-2">{{ title }}</h4>
        <p class="text-sm text-gray-300 mt-1">{{ description }}</p>
      </div>
    `
  })
  </script>
  