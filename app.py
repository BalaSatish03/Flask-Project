

from flask import Flask, request, jsonify
from elasticsearch import Elasticsearch
from elasticsearch.helpers import bulk
import json

app = Flask(__name__)


es = Elasticsearch()

@app.route('/<index_name>/create', methods=['POST'])
def index_documents(index_name):
    try:
        if 'file' in request.files:
            file = request.files['file']
            docs = json.load(file)
        else:
            raw_data = request.get_json()
            if raw_data is None:
                return jsonify({"error": "Invalid JSON data"}), 400
                
            docs = [raw_data]

        bulk_data = [
            {"_op_type": "index", "_index": index_name, "_source": doc}
            for  doc in enumerate(docs)
        ]

        success, failed = bulk(es, bulk_data, index=index_name, raise_on_error=False)

        return jsonify({
            "success": success,
            "failed": failed
        }), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
        


@app.route('/get_data/<index_name>', methods=['GET'])
def get_data(index_name):
    try:
        request_data = request.get_json()
      
        query = request_data.get('query')

        if  not query:
            result = es.search(index=index_name)
            hits = result.get('hits', {}).get('hits', [])
            documents = [hit['_source'] for hit in hits]

            
        else:

            result = es.search(index=index_name, body={"query": query})

            hits = result.get('hits', {}).get('hits', [])
            documents = [hit['_source'] for hit in hits]

        return jsonify(documents)
    except Exception as e:
        return jsonify({"error": f"Error retrieving data: {str(e)}"}), 500


@app.route('/update_data/<index_name>',methods=['POST'])
def update_data(index_name):
    try:
        request_data=request.get_json()

        Updated_data=es.update_by_query(index=index_name,body=request_data)
        
        return jsonify({'message':'document updated successfully'})
    except Exception as e:
        return jsonify({"error": f"Error updating data: {str(e)}"}), 500

@app.route('/delete_data/<index_name>',methods=['DELETE'])
def deleted_data(index_name):
    try:
        request_data=request.get_json()
        query=request_data.get('query')
        if  not query:
            return jsonify({"error": " 'query' parameters are required."}), 400
        deleted_data=es.delete_by_query(index=index_name,body={'query':query})
        return jsonify(deleted_data)
    except Exception as e:
        return jsonify({"error": f"Error deleting data: {str(e)}"}), 500




    

if __name__ == '__main__':
    app.run(debug=True)
