# 깃허브 명령어
1. 현재 폴더를 새로운 git 저장소로 초기화한다.
git init

1. 로컬 폴던를 원격 저장소와 연결
git remote add orgin https://github.com/jamesjin7088/capstoneDesign.git

2. 원격 커밋을 먼저 받아오기
git pull origin main --rebase

3. git에 추가
git add .

4. 커밋하기
git commit -m "메세지"

5. 원격 저장소에 push
git push  origin main
