from clarifai_grpc.channel.clarifai_channel import ClarifaiChannel
from clarifai_grpc.grpc.api import resources_pb2, service_pb2, service_pb2_grpc
from clarifai_grpc.grpc.api.status import status_code_pb2
import constants as const  # Importing constants


def call_clarifai_api(prompt):
    try:
        channel = ClarifaiChannel.get_grpc_channel()
        stub = service_pb2_grpc.V2Stub(channel)
        metadata = (('authorization', 'Key ' + const.PAT),)
        userDataObject = resources_pb2.UserAppIDSet(user_id=const.USER_ID, app_id=const.APP_ID)

        response = stub.PostModelOutputs(
            service_pb2.PostModelOutputsRequest(
                user_app_id=userDataObject,
                model_id=const.MODEL_ID,
                version_id=const.MODEL_VERSION_ID,
                inputs=[resources_pb2.Input(data=resources_pb2.Data(text=resources_pb2.Text(raw=prompt)))]
            ),
            metadata=metadata
        )

        if response.status.code != status_code_pb2.SUCCESS:
            return None, f"Clarifai API error: {response.status.description}"
        else:
            return response.outputs[0].data.text.raw, None
    except Exception as e:
        return None, str(e)

