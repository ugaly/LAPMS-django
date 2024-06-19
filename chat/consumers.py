from channels.generic.websocket import AsyncWebsocketConsumer
from channels.layers import get_channel_layer
from channels.db import database_sync_to_async
import json
from .models import Customer
from django.contrib.auth import get_user_model
from datetime import datetime



User = get_user_model()


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        # Accept the WebSocket connection
        await self.accept()

        # Add the client to the chat group
        await self.channel_layer.group_add(
            'chat_group',  # Group name
            self.channel_name  # Channel name
        )

    async def disconnect(self, close_code):
        # Remove the client from the chat group
        await self.channel_layer.group_discard(
            'chat_group',  # Group name
            self.channel_name  # Channel name
        )

    async def receive(self, text_data):
        # Parse the received JSON message
        text_data_json = json.loads(text_data)
        message = text_data_json.get('message', '')

        # Broadcast the message to all clients in the chat group
        await self.channel_layer.group_send(
            'chat_group',  # Group name
            {
                'type': 'chat.message',
                'message': message,
            }
        )

    async def chat_message(self, event):
        # Send the received message to the WebSocket client
        message = event.get('message', '')
        await self.send(text_data=json.dumps({
            'message': message
        }))


# inafanya kazi ya kuadd

# class CustomerConsumer(AsyncWebsocketConsumer):
#     async def connect(self):
#         await self.accept()

#     async def disconnect(self, close_code):
#         pass

#     async def receive(self, text_data):
#         text_data_json = json.loads(text_data)
#         command = text_data_json.get('command')

#         if command == 'create':
#             await self.create_customer(text_data_json)

#     @database_sync_to_async
#     def create_customer(self, data):
#         full_name = data.get('full_name')
#         phone_number = data.get('phone_number')
#         location = data.get('location')
#         customer = Customer.objects.create(full_name=full_name, phone_number=phone_number, location=location)
#         return customer

#     async def send_customer(self, customer):
#         await self.send(text_data=json.dumps({
#             'command': 'create',
#             'customer': {
#                 'full_name': customer.full_name,
#                 'phone_number': customer.phone_number,
#                 'location': customer.location,
#             },
#         }))



#inafanya kazi kuadd na retrieve but not asyc
# class CustomerConsumer(AsyncWebsocketConsumer):
#     async def connect(self):
#         await self.accept()

#     async def disconnect(self, close_code):
#         pass

#     async def receive(self, text_data):
#         text_data_json = json.loads(text_data)
#         command = text_data_json.get('command')

#         if command == 'create':
#             await self.create_customer(text_data_json)
#         elif command == 'fetch_all':
#             await self.send_all_customers()

#     @database_sync_to_async
#     def create_customer(self, data):
#         full_name = data.get('full_name')
#         phone_number = data.get('phone_number')
#         location = data.get('location')
#         customer = Customer.objects.create(full_name=full_name, phone_number=phone_number, location=location)
#         return customer

#     @database_sync_to_async
#     def fetch_all_customers(self):
#         customers = Customer.objects.all()
#         return [self.serialize_customer(customer) for customer in customers]

#     async def send_all_customers(self):
#         customers = await self.fetch_all_customers()
#         await self.send(text_data=json.dumps({
#             'command': 'fetch_all',
#             'customers': customers,
#         }))

#     def serialize_customer(self, customer):
#         return {
#             'id': customer.id,
#             'full_name': customer.full_name,
#             'phone_number': customer.phone_number,
#             'location': customer.location
#         }





from channels.generic.websocket import AsyncWebsocketConsumer
import json
from .models import Customer
from asgiref.sync import sync_to_async


# import jwt

# class CustomerConsumer(AsyncWebsocketConsumer):
#     async def connect(self):
#         token = self.scope.get('query_string').decode().split('=')[1]  # Extract token from query string
#         try:
#             decoded_token = jwt.decode(token, 'SECRET_KEY', algorithms=['HS256'])  # Verify and decode token
#             user_id = decoded_token['user_id']
#             user = User.objects.get(pk=user_id)
#             self.scope['user'] = user  # Set user in scope
#         except jwt.ExpiredSignatureError:
#             # Handle token expiration
#             await self.close(code=4401)
#         except jwt.InvalidTokenError:
#             # Handle invalid token
#             await self.close(code=4402)
        
#         # Check if user is authenticated
#         if not user.is_authenticated:
#             # Reject the connection
#             await self.close(code=4403)

#         # Join customer group
#         await self.channel_layer.group_add("customer_group", self.channel_name)
#         await self.accept()
        



        
# class CustomerConsumer(AsyncWebsocketConsumer):
#     async def connect(self):
#         # user = self.scope['user']
#         # print(user, user.is_authenticated)
#         # if not user.is_authenticated:
#         #     print('User is not authenticated')
#         #     # Reject the connection
#         #     await self.close()

#         # Join customer group
#         await self.channel_layer.group_add("customer_group", self.channel_name)
#         await self.accept()

#     async def disconnect(self, close_code):
#         # Leave customer group
#         await self.channel_layer.group_discard("customer_group", self.channel_name)

#     async def receive(self, text_data):
#         text_data_json = json.loads(text_data)
#         command = text_data_json.get('command')
        
#         if command == 'create':
#             customer = await self.create_customer(text_data_json)
#             await self.broadcast_new_customer(customer)
#         elif command == 'fetch_all':
#             await self.send_all_customers()

#     @sync_to_async
#     def create_customer(self, data):
#         # Code to create a new customer
#         customer = Customer.objects.create(
#             full_name=data.get('full_name'),
#             phone_number=data.get('phone_number'),
#             location=data.get('location')
#         )
#         return customer

#     async def broadcast_new_customer(self, customer):
#         # Broadcasting new customer to all clients in the group
#         await self.channel_layer.group_send(
#             "customer_group",
#             {
#                 'type': 'new_customer',
#                 'customer': self.serialize_customer(customer),
#             }
#         )

#     async def new_customer(self, event):
#         # Handler for broadcasting customer data
#         await self.send(text_data=json.dumps({
#             'command': 'create',
#             'customer': event['customer'],
#         }))

#     # Additional methods remain unchanged...

#     @database_sync_to_async
#     def fetch_all_customers(self):
#         customers = Customer.objects.all()
#         return [self.serialize_customer(customer) for customer in customers]

#     async def send_all_customers(self):
#         customers = await self.fetch_all_customers()
#         await self.send(text_data=json.dumps({
#             'command': 'fetch_all',
#             'customers': customers,
#         }))

#     def serialize_customer(self, customer):
#         return {
#             'id': customer.id,
#             'full_name': customer.full_name,
#             'phone_number': customer.phone_number,
#             'location': customer.location
#         }





import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from django.contrib.auth.models import User
from rest_framework_simplejwt.tokens import AccessToken
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError
from system_user.models import SystemUser

class CustomerConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        # Extract token from the query string
        query_string = self.scope['query_string'].decode()
        token = query_string.split('token=')[1] if 'token=' in query_string else None
        print(token)

        if not token:
            await self.close(code=4000)  # Close connection if no token is provided
            return

        # Validate token and authenticate user
        user = await self.get_user_from_token(token)
       
        if not user:
            await self.close(code=4001)  # Close connection if token is invalid
            return

        # Set user context to consumer's scope
        self.scope['user'] = user
        print(user, user.is_authenticated)

        # Join the customer group
        await self.channel_layer.group_add("customer_group", self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        # Leave customer group
        await self.channel_layer.group_discard("customer_group", self.channel_name)

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        command = text_data_json.get('command')

        if command == 'create':
            customer = await self.create_customer(text_data_json)
            await self.broadcast_new_customer(customer)
        elif command == 'fetch_all':
            await self.send_all_customers()

    @database_sync_to_async
    def get_user_from_token(self, token):
        try:
            # Decode the token and check if it is valid
            decoded_data = AccessToken(token)
            user = User.objects.get(id=decoded_data['user_id'])
            return user if user.is_authenticated else None
        except (TokenError, User.DoesNotExist, KeyError):
            return None

    @database_sync_to_async
    def create_customer(self, data):
        # Code to create a new customer
        customer = Customer.objects.create(
            full_name=data['full_name'],
            phone_number=data['phone_number'],
            location=data['location'],
            created_by=self.scope['user']
        )
        return customer

    async def broadcast_new_customer(self, customer):
        # Broadcasting new customer to all clients in the group
        await self.channel_layer.group_send(
            "customer_group",
            {
                'type': 'new_customer',
                'customer': self.serialize_customer(customer),
            }
        )

    async def new_customer(self, event):
        # Handler for broadcasting customer data
        await self.send(text_data=json.dumps({
            'command': 'create',
            'customer': event['customer'],
        }))

    @database_sync_to_async
    def fetch_all_customers(self):
        customers = Customer.objects.all()
        return [self.serialize_customer(customer) for customer in customers]

    async def send_all_customers(self):
        customers = await self.fetch_all_customers()
        await self.send(text_data=json.dumps({
            'command': 'fetch_all',
            'customers': customers,
        }))

    def serialize_customer(self, customer):
        return {
            'id': customer.id,
            'full_name': customer.full_name,
            'phone_number': customer.phone_number,
            'location': customer.location
        }






from asgiref.sync import sync_to_async
from complaint.models import Complaint, Question, Answer
import json
from channels.generic.websocket import AsyncWebsocketConsumer

# class ComplaintConsumer(AsyncWebsocketConsumer):
    # async def connect(self):
    #     # Join the complaint group
    #     query_string = self.scope['query_string'].decode()
    #     token = query_string.split('token=')[1] if 'token=' in query_string else None

    #     if not token:
    #         await self.close(code=4000)  # Close connection if no token is provided
    #         return

    #     # Validate token and authenticate user
    #     user = await self.get_user_from_token(token)
    #     if not user:
    #         await self.close(code=4001)  # Close connection if token is invalid
    #         return

    #     # Set user context to consumer's scope
    #     self.scope['user'] = user
    #     print(user, user.is_authenticated)

    #     await self.channel_layer.group_add("complaint_group", self.channel_name)
    #     await self.accept()

    # async def disconnect(self, close_code):
    #     # Leave the complaint group
    #     await self.channel_layer.group_discard("complaint_group", self.channel_name)

    # async def receive(self, text_data):
    #     # Receive message from WebSocket
    #     text_data_json = json.loads(text_data)
    #     command = text_data_json.get('command')

    #     if command == 'fetch_all_complaints':
    #         await self.send_all_complaints()

    # async def send_all_complaints(self):
    #     # Fetch all complaints from the database asynchronously
    #     complaints = await self.fetch_all_complaints()

    #     # Send complaints to the client
    #     await self.send(text_data=json.dumps({
    #         'command': 'fetch_all_complaints',
    #         'complaints': complaints,
    #     }))



    # async def new_complaint(self, event):
    #     # Handler for broadcasting new complaint data
    #     await self.send(text_data=json.dumps({
    #         'command': 'new_complaint',
    #         'complaint': event['complaint'],
    #     }))

    # @sync_to_async
    # def fetch_all_complaints(self):
    #     # Query all complaints from the database
    #     complaints = Complaint.objects.filter(created_by=self.scope['user'])

    #     # Serialize complaints
    #     serialized_complaints = [{
    #         'id': complaint.id,
    #         'message': complaint.message,
    #         'image': complaint.image.url if complaint.image else None,
    #         'created_by': complaint.created_by.full_name if complaint.created_by else None,
    #         'created_time': complaint.created_time.isoformat() if complaint.created_time else None,
    #         'created_date': complaint.created_date.isoformat() if complaint.created_date else None

            
    #     } for complaint in complaints]

    #     return serialized_complaints
    

    # @database_sync_to_async
    # def get_user_from_token(self, token):
    #     try:
    #         # Decode the token and check if it is valid
    #         decoded_data = AccessToken(token)
    #         user = SystemUser.objects.get(id=decoded_data['user_id'])
    #         return user if user.is_authenticated else None
    #     except (TokenError, User.DoesNotExist, KeyError):
    #         return None







from asgiref.sync import sync_to_async
from complaint.models import Complaint
import json
from channels.generic.websocket import AsyncWebsocketConsumer
from django.contrib.humanize.templatetags import humanize
from django.utils.timesince import timesince



class ComplaintConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        # Join the complaint group

        query_string = self.scope['query_string'].decode()
        token = query_string.split('token=')[1] if 'token=' in query_string else None

        if not token:
            await self.close(code=4000)  # Close connection if no token is provided
            return

        # Validate token and authenticate user
        user = await self.get_user_from_token(token)
        if not user:
            await self.close(code=4001)  # Close connection if token is invalid
            return

        # Set user context to consumer's scope
        self.scope['user'] = user
        print(user, user.is_authenticated)

        await self.channel_layer.group_add("complaint_group", self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        # Leave the complaint group
        await self.channel_layer.group_discard("complaint_group", self.channel_name)

    async def receive(self, text_data):
        # Receive message from WebSocket
        text_data_json = json.loads(text_data)
        command = text_data_json.get('command')
        filter_by_user = text_data_json.get('filter_by_user', True)

        print(command, filter_by_user)

        if command == 'fetch_all_complaints':
            # await self.send_all_complaints()
            await self.send_all_complaints(filter_by_user)

    # async def send_all_complaints(self):
    #     # Fetch all complaints from the database asynchronously
    #     complaints = await self.fetch_all_complaints()

    #     # Send complaints to the client
    #     await self.send(text_data=json.dumps({
    #         'command': 'fetch_all_complaints',
    #         'complaints': complaints,
    #     }))


    async def send_all_complaints(self,  filter_by_user=True):
        # Fetch all complaints from the database asynchronously
        # complaints = await self.fetch_all_complaints()
        complaints = await self.fetch_all_complaints(filter_by_user)

        # Send complaints to the client
        await self.send(text_data=json.dumps({
            'command': 'fetch_all_complaints',
            'complaints': complaints,
        }))




    async def new_complaint(self, event):
        # Handler for broadcasting new complaint data
        # await self.send(text_data=json.dumps({
        #     'command': 'new_complaint',
        #     'complaint': event['complaint'],
        # }))

        complaint = event['complaint']
        timestamp_str = complaint['timestamp']  # Assuming timestamp is a string
        timestamp = datetime.fromisoformat(timestamp_str)  # Convert string to datetime object
        complaint['created_time'] = timesince(timestamp)
        # complaint['created_by'] = complaint['created_by'].system_user.full_name
        
        # Broadcast the updated complaint data
        await self.send(text_data=json.dumps({
            'command': 'new_complaint',
            'complaint': complaint,
        }))

    # @sync_to_async
    # def fetch_all_complaints(self):
    #     # Query all complaints from the database
    #     complaints = Complaint.objects.filter(created_by=self.scope['user'])

    #     # Serialize complaints
    #     serialized_complaints = [{
    #         'id': complaint.id,
    #         'message': complaint.message,
    #         'image': complaint.image.url if complaint.image else None,
    #         'created_by': complaint.created_by.full_name if complaint.created_by else None,
    #         'created_time': complaint.created_time.isoformat() if complaint.created_time else None,
    #         'created_date': complaint.created_date.isoformat() if complaint.created_date else None

            
    #     } for complaint in complaints]

    #     return serialized_complaints

    @sync_to_async
    def fetch_all_complaints(self, filter_by_user=True):

        print(filter_by_user)
        if filter_by_user:
            complaints = Complaint.objects.filter(created_by=self.scope['user']).order_by('timestamp')
        else:
            complaints = Complaint.objects.all().order_by('-timestamp')

        # Serialize complaints
        serialized_complaints = [{
            'id': complaint.id,
            'message': complaint.message,
            'image': complaint.image.url if complaint.image else None,
            'created_by': complaint.created_by.full_name if complaint.created_by else None,
            # 'created_time': complaint.created_time.isoformat() if complaint.created_time else None,
            # 'created_time': complaint.created_time.strftime('%H:%M:%S') if complaint.created_time else None,
            'created_time': timesince(complaint.timestamp) if complaint.timestamp else None,
            'created_date': complaint.created_date.isoformat() if complaint.created_date else None
        } for complaint in complaints]

        return serialized_complaints

    @database_sync_to_async
    def get_user_from_token(self, token):
        try:
            # Decode the token and check if it is valid
            decoded_data = AccessToken(token)
            user = SystemUser.objects.get(id=decoded_data['user_id'])
            return user if user.is_authenticated else None
        except (TokenError, User.DoesNotExist, KeyError):
            return None
        







class QuestionConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        # Join the complaint group

        query_string = self.scope['query_string'].decode()
        token = query_string.split('token=')[1] if 'token=' in query_string else None
        print(token)

        if not token:
            await self.close(code=4000)  # Close connection if no token is provided
            return

        # Validate token and authenticate user
        user = await self.get_user_from_token(token)
        if not user:
            await self.close(code=4001)  # Close connection if token is invalid
            return

        # Set user context to consumer's scope
        self.scope['user'] = user
        print(user, user.is_authenticated)

        await self.channel_layer.group_add("question_group", self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        # Leave the complaint group
        await self.channel_layer.group_discard("question_group", self.channel_name)

    async def receive(self, text_data):
        # Receive message from WebSocket
        text_data_json = json.loads(text_data)
        command = text_data_json.get('command')
        filter_by_user = text_data_json.get('filter_by_user', True)

        print(command, filter_by_user)

        if command == 'fetch_all_questions':
            # await self.send_all_complaints()
            await self.send_all_questions(filter_by_user)

 
    async def send_all_questions(self,  filter_by_user=True):
        # Fetch all complaints from the database asynchronously
        # complaints = await self.fetch_all_complaints()
        questions = await self.fetch_all_questions(filter_by_user)

        # Send complaints to the client
        await self.send(text_data=json.dumps({
            'command': 'fetch_all_questions',
            'questions': questions,
        }))


    async def new_question(self, event):
        # Handler for broadcasting new complaint data
        # await self.send(text_data=json.dumps({
        #     'command': 'new_question',
        #     'question': event['question'],
        # }))
        question = event['question']
        timestamp_str = question['timestamp']  # Assuming timestamp is a string
        timestamp = datetime.fromisoformat(timestamp_str)  # Convert string to datetime object
        question['created_time'] = timesince(timestamp)
        # question['created_by'] = question['created_by'].full_name
        
        # Broadcast the updated complaint data
        await self.send(text_data=json.dumps({
            'command': 'new_question',
            'question': question,
        }))

   
    @sync_to_async
    def fetch_all_questions(self, filter_by_user=True):

        print(filter_by_user)
        if filter_by_user:
            questions = Question.objects.filter(created_by=self.scope['user']).order_by('timestamp')
        else:
            questions = Question.objects.all().order_by('-timestamp')

        # Serialize complaints
        serialized_questions = [{
            'id': question.id,
            'message': question.message,
            'image': question.image.url if question.image else None,
            'created_by': question.created_by.full_name if question.created_by else None,
            'created_time': timesince(question.timestamp) if question.timestamp else None,
            'created_date': question.created_date.isoformat() if question.created_date else None,
            'answers': self.get_answers_for_question(question)
        } for question in questions]

        return serialized_questions
    

    def get_answers_for_question(self, question):
        answers = Answer.objects.filter(question=question).select_related('respondent')
        return [
            {
                'id': answer.id,
                'message': answer.message,
                'respondent': answer.respondent.full_name,
                'created_at': answer.created_at.isoformat()
            }
            for answer in answers
        ]

    @database_sync_to_async
    def get_user_from_token(self, token):
        try:
            # Decode the token and check if it is valid
            decoded_data = AccessToken(token)
            user = SystemUser.objects.get(id=decoded_data['user_id'])
            return user if user.is_authenticated else None
        except (TokenError, User.DoesNotExist, KeyError):
            return None
        


    async def new_answer(self, event):
        # Handler for broadcasting new answer data
        print('hhhhhhhhh',event)
        await self.send(text_data=json.dumps({
            'command': 'new_answer',
            'answer': event['answer'],
        }))