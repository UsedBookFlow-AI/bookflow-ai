from services.llm import get_model
import json
import logging

# Logging 설정
logging.basicConfig(level='INFO', format='%(asctime)s %(name)s: %(message)s', datefmt='%Y-%m-%dT%H:%M:%S')
logger = logging.getLogger(__name__)

class ExtractEntitiesService:
    @staticmethod
    def extract_entities(raw_sentence):
        model = get_model()
        prompt =f"""
        You are an expert at extracting key entities from the sentence given.
        The sentence is about book request information and our aim is to identify the main entities in the sentence along with their importance weight.
        The weight should range from 0 to 1, where 1 indicates the highest importance.
        # Sentence: "{raw_sentence}"
        # Output Format :
        {{
            "target_age":{{"value": "age_value1", "weight": weight_value1}}, 
            "book_category":{{"value": "category_value", "weight": weight_value2}},
            "book_amount": {{"value": "category_value", "weight": weight_value2}},
            "others": {{"entity1": {{"value": "value1", "weight": weight1}}, "entity2": {{"value": "value2", "weight": weight2}}...}}
            
        }}

        # **Instructions** :
        Include all the other entities that are not related to age, category, and amount to 'others'.
        When there are no entities for age, category or amount, set their value to null and weight to 0.
        If the sentence is not about book requests, return the following JSON: {{"message": "The sentence does not contain book request information."}}.
        Please provide the output in pure JSON format only (Do NOT include ```json)
        """

        response = model.invoke(prompt)
        if isinstance(response.content, list):
            content = "".join([part.text for part in response.content])
        else:
            content = response.content

        try:
            parsed = json.loads(content)
            logger.info("LLM 개체 추출 성공")
            return parsed
        except json.JSONDecodeError as e:
            logger.warning(f"JSON 구문 분석 오류: {e}")
            return response


