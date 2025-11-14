from langchain_google_genai import ChatGoogleGenerativeAI
import os
import logging

# Logging 설정
logging.basicConfig(level='INFO', format='%(asctime)s %(name)s: %(message)s', datefmt='%Y-%m-%dT%H:%M:%S')
logger = logging.getLogger(__name__)


def get_model():
    try:
        model = ChatGoogleGenerativeAI(
            google_api_key=os.getenv("GOOGLE_API_KEY"),
            model="gemini-2.5-flash",
            temperature=0,
            max_tokens=4048
        )
        logger.info("llm 모델이 성공적으로 초기화되었습니다.")
        return model
    except Exception as e:
        logger.error(f"모델 초기화 중 오류 발생 : {e}")
        raise e