from elasticsearch import Elasticsearch, helpers
import pandas as pd

def create_es_client(host="localhost", port=8080):
    host = "localhost"  # Или используйте ваш хост
    port = 9200        # Стандартный порт Elasticsearch
    scheme = "http"     # Укажите протокол (http или https)

    es = Elasticsearch([{"host": host, "port": port, "scheme": scheme}])
    return es

def create_index(es_client, index_name):
    if es_client.indices.exists(index=index_name):
        es_client.indices.delete(index=index_name)
    
    mapping = {
        "mappings": {
            "properties": {
                "Department": {"type": "keyword"},
                "Score": {"type": "integer"}
            }
        }
    }
    es_client.indices.create(index=index_name, body=mapping)
    print(f"Индекс {index_name} создан.")

def load_data_to_es(es_client, index_name, csv_file):
    data = pd.read_csv(csv_file)
    actions = [
        {
            "_index": index_name,
            "_source": {
                "Department": row["Department"],
                "Score": int(row["Score"]),
            },
        }
        for _, row in data.iterrows()
    ]
    helpers.bulk(es_client, actions)
    print(f"Данные из {csv_file} загружены в индекс {index_name}.")

def calculate_average_scores(es_client, index_name):
    query = {
        "size": 0,
        "aggs": {
            "departments": {
                "terms": {"field": "Department"},
                "aggs": {
                    "average_score": {"avg": {"field": "Score"}}
                }
            }
        }
    }
    response = es_client.search(index=index_name, body=query)
    results = {
        bucket["key"]: bucket["average_score"]["value"]
        for bucket in response["aggregations"]["departments"]["buckets"]
    }
    print("Средние значения оценок для департаментов:")
    for department, avg_score in results.items():
        print(f"{department}: {avg_score:.2f}")

if __name__ == "__main__":
    # Параметры
    index_name = "departments_scores"
    csv_file = "generated_data.csv"  # Укажите ваш CSV-файл

    # Запуск
    es_client = create_es_client()
    create_index(es_client, index_name)
    load_data_to_es(es_client, index_name, csv_file)
    calculate_average_scores(es_client, index_name)
