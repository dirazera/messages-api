from flask import jsonify, request, abort
import messages.message_helpers as helper 
from messages import app


# Send message
@app.route('/recipients/<path:recipient>/messages', methods=['POST'])
def create(recipient):
    if request.content_type != 'application/json':
        abort(400,"Invalid content-type") 
    body = request.get_json()    
    sender = body.get("sender")
    subject = body.get("subject")
    content = body.get("content")

    if not sender:
        abort(400,"Email invalid")
    if not subject:
        abort(400,"Subject missing")
    if not content:
        abort(400,"Content missing")
    
    result = helper.create_message(sender,recipient,subject,content)
    return jsonify(result), 201 


# Fetch only new, all messages and paginated
@app.route('/recipients/<path:recipient>/messages', methods=['GET'])  
def get_all_new(recipient):
    page = request.args.get("page")
    page_size = request.args.get("page_size")
    
    try:  
        if page is not None:
            page = int(page)
            if page_size is not None:
                page_size = int(page_size)
    except ValueError as error:
        abort (400,description="Page and page size must be an int")
                
    all =  request.args.get("all","false").lower()
    result = helper.get_messages(recipient,all!="false",page,page_size)
    return jsonify(result)


#Fetch single message (by id)
@app.route('/recipients/<path:recipient>/messages/<string:message_id>', methods=['GET'])
def get_by_id(recipient,message_id):
    result = helper.get_message_by_id(recipient,message_id)
    if result:
        return jsonify(result)
    else:
        abort (404, description="No message found for that id")
        

# Delete single message (by id)
@app.route('/recipients/<string:recipient>/messages/<string:message_id>', methods=['DELETE'])
def delete_by_id(recipient,message_id): 
    count = helper.delete_messages_by_id(recipient,[message_id])
    return jsonify(count_deleted=count)
    

# Delete multiple
@app.route('/recipients/<string:recipient>/messages', methods=['DELETE'])
def delete_multiple_messages(recipient):
    body = request.get_json() 
    ids_to_delete = body.get("ids",[])
    
    for id in ids_to_delete:
        if not isinstance(id,str):
            abort(400,"The list of ids must contain only string")
    
    count = helper.delete_messages_by_id(recipient,ids_to_delete)
    return jsonify(count_deleted=count)


@app.errorhandler(404)
@app.errorhandler(400)
def error_handler(e):
    return jsonify(error=str(e)), e.code 



