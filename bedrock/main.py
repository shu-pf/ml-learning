import boto3

# --- 設定情報 ---
PROFILE_NAME = "shugo-dev-admin"  # 使用したいプロファイル名に書き換えてください
REGION = "ap-northeast-1"
KB_ID = "UGTOWROFJT"
MODEL_ARN = f"arn:aws:bedrock:{REGION}::foundation-model/anthropic.claude-3-5-sonnet-20240620-v1:0"

def ask_my_kb(question):
    # 1. 指定したプロファイルを使ってセッションを作成
    session = boto3.Session(profile_name=PROFILE_NAME)
    
    # 2. セッションからクライアントを作成
    client = session.client("bedrock-agent-runtime", region_name=REGION)

    try:
        response = client.retrieve_and_generate(
            input={'text': question},
            retrieveAndGenerateConfiguration={
                'type': 'KNOWLEDGE_BASE',
                'knowledgeBaseConfiguration': {
                    'knowledgeBaseId': KB_ID,
                    'modelArn': MODEL_ARN,
                }
            }
        )

        print(f"\n回答: {response['output']['text']}")
                
    except Exception as e:
        print(f"エラーが発生しました: {e}")

if __name__ == "__main__":
    ask_my_kb("情報通信白書の公表にあたって、総務大臣はどのように言っていますか？")
