import boto3
from botocore.exceptions import ClientError
from app.config import settings
from app.models.article import Article
from app.models.event import Event
from boto3.dynamodb.conditions import Key, Attr

def get_dynamodb_table():

    db = boto3.resource(
        'dynamodb',
        endpoint_url=settings.dynamodb_endpoint,
        region_name=settings.dynamodb_region,
        aws_access_key_id=settings.aws_access_key_id,
        aws_secret_access_key=settings.aws_secret_access_key
    )
    return db.Table(settings.dynamodb_events_table)

def save_events_and_articles(articles: list[Article], events: list[Event]):

    table = get_dynamodb_table()
    
    with table.batch_writer() as batch:
        for event in events:
            try:
                item = event.model_dump(mode="json")
                item["pk"] = f"EVENT#{event.id}"
                item["type"] = "EVENT"
                batch.put_item(Item=item)
            except ClientError as e:
                print(f"Greška pri spremanju događaja {event.id}: {e}")

        for article in articles:
            try:
                item = article.model_dump(mode="json")
                item["pk"] = f"ARTICLE#{article.id}"
                item["type"] = "ARTICLE"
                if not item.get("event_id"):
                    item["event_id"] = None
                batch.put_item(Item=item)
            except ClientError as e:
                print(f"Greška pri spremanju članka {article.id}: {e}")

def get_all_active_events() -> list[Event]:

    table = get_dynamodb_table()
    try:
        response = table.scan(
            FilterExpression="#t = :type_val",
            ExpressionAttributeNames={"#t": "type"},
            ExpressionAttributeValues={":type_val": "EVENT"}
        )
        items = response.get("Items", [])
        return [Event(**item) for item in items]
    except ClientError as e:
        print(f"Greška pri dohvaćanju događaja: {e}")
        return []

def get_event_by_id(event_id: str):
    table = get_dynamodb_table()
    try:
        response = table.scan(
            FilterExpression=Attr("id").eq(event_id)
        )
        items = response.get("Items", [])
        
        if items:
            return items[0]
            
        return None
    except Exception as e:
        print(f"BOTO3 GREŠKA: {e}")
        return None