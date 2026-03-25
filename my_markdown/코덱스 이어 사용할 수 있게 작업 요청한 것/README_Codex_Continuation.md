# Codex continuation pack

이 패키지는 **새로운 Codex 세션 / 새 채팅 / 새 환경**에서도 지금까지의 금융 데이터 파이프라인 작업을 이어가기 위한 전달용 파일 모음입니다.

## 권장 사용법
1. 이 패키지의 파일들을 **프로젝트 루트(CODEX 폴더)** 안으로 복사합니다.
2. 특히 아래 2개는 꼭 repo 안에 넣어두세요.
   - `docs/CODEX_SESSION_STATE.md`
   - `prompts/CODEX_RESUME_PROMPT_QDATA.txt`
3. 새 Codex 세션을 열면, `prompts/CODEX_RESUME_PROMPT_QDATA.txt` 내용을 그대로 붙여넣고 시작합니다.
4. 각 milestone이 끝날 때마다 `docs/CODEX_SESSION_STATE.md`의 "현재 상태"와 "다음 작업"만 갱신합니다.

## 왜 이 방식이 안전한가
- 채팅 히스토리에 의존하지 않고, **프로젝트 폴더 안의 파일**로 상태를 고정합니다.
- Codex가 새 환경이어도 **파일만 읽으면 현재 맥락을 복원**할 수 있습니다.
- 이후 QDATA, 종목코드 매칭, 지표 표준화 단계로 가도 같은 방식으로 누적 가능합니다.

## 현재 핵심 상태
- inventory/runtime/inspection 완료
- KDATA1 parser 완료
- KDATA2 parser 완료
- 다음 milestone: **QDATA parser 구현**
