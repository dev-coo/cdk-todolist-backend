from flask import Flask, jsonify, json, Response, request
from flask_cors import CORS
import todo_table_client

# Flask로 생성된 매우 기본적인 API로 요청에 대한 두 가지 가능한 라우트가 있습니다.

app = Flask(__name__)
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = False
CORS(app)

# 서비스 기본 경로는 서비스 루트에 전송된 상태 확인이
# 정상적인 응답을 받을 수 있도록 간단한 응답을 제공합니다.
@app.route("/")
def health_check_response():
    return jsonify({"message" : "Nothing here, used for health check. Try /todos instead."})

# 투두리스트 웹사이트의 다음 버전이 활용할 메인 API 리소스입니다.
# 웹사이트에 표시될 모든 투두의 데이터를 반환합니다.
# 이제 정적 JSON 파일이 아닌 DynamoDB 데이터베이스에서 투두를 가져옵니다.
@app.route("/todos")
def get_todos():
    # DynamoDB에서 모든 투두를 가져옵니다.
    service_response = todo_table_client.get_all_todos()
    
    # 브라우저가 응답이 JSON으로 포맷되어 있음을 알 수 있도록 
    # Content-Type 헤더를 설정하고 프론트엔드 JavaScript 코드가
    # 응답을 적절히 파싱할 수 있도록 합니다.
    flask_response = Response(service_response)
    flask_response.headers["Content-Type"] = "application/json"

    return flask_response

# 배포된 로컬 서버에서 서비스를 실행하고,
# 8080 포트에서 수신 대기합니다.
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080) 