import boto3
import json
import logging
from collections import defaultdict
import argparse

# boto3를 사용하여 DynamoDB 클라이언트를 생성합니다. 
# boto3 라이브러리는 자동으로 ECS 태스크 역할과 연결된 자격 증명을 사용하여 
# DynamoDB와 통신하므로 코드에서 자격 증명을 저장/관리할 필요가 전혀 없습니다!
region = 'ap-northeast-2'
client = boto3.client('dynamodb', region_name=region)

def get_todos_json(items):
    # 반환된 투두들을 순회하고 프론트엔드에서 예상하는 
    # JSON 응답 구조와 일치하는 새 딕셔너리에 속성을 추가합니다.
    todo_list = []

    for item in items:
        todo = {}

        todo["id"] = int(item["id"]["N"])
        todo["text"] = item["text"]["S"]
        todo["completed"] = item["completed"]["BOOL"]

        todo_list.append(todo)

    return todo_list

def get_all_todos():
    # DynamoDB 스캔 작업을 사용하여 DynamoDB에서 모든 투두를 검색합니다.
    # 참고: 스캔 API는 DynamoDB 테이블에 많은 수의 레코드가 포함되어 있고 
    # DynamoDB에서 응답이 반환되기 전에 테이블에서 많은 양의 데이터를 스캔해야 하는 
    # 필터가 작업에 적용될 때 지연 시간 측면에서 비용이 많이 들 수 있습니다.
    # 많은 요청을 받는 대용량 테이블의 경우 자주/공통 스캔 작업의 결과를 
    # 인메모리 캐시에 저장하는 것이 일반적입니다. DynamoDB Accelerator(DAX) 또는 
    # ElastiCache 사용으로 이러한 이점을 제공할 수 있습니다.
    # 하지만 투두리스트 API는 트래픽이 적고 테이블이 매우 작기 때문에 
    # 스캔 작업이 워크샵의 요구 사항에 적합합니다.
    response = client.scan(
        TableName='TodoTable'
    )

    logging.info(response["Items"])

    # 반환된 투두들을 순회하고 프론트엔드에서 예상하는 
    # JSON 응답 구조와 일치하는 새 딕셔너리에 속성을 추가합니다.
    todo_list = get_todos_json(response["Items"])

    return json.dumps(todo_list)

# 커맨드 라인에서 테스트할 수 있도록
if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    args = parser.parse_args()

    print("모든 투두 가져오기")
    items = get_all_todos()

    print(items) 