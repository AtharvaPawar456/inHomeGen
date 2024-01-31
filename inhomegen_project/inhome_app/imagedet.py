
##################################################################################################
# In this section, we set the user authentication, user and app ID, model details, and the URL
# of the image we want as an input. Change these strings to run your own example.
#################################################################################################

# Your PAT (Personal Access Token) can be found in the portal under Authentification
PAT = 'e536ce09a1024c66b7066cdf342be9df'
# Specify the correct user_id/app_id pairings
# Since you're making inferences outside your app's scope
USER_ID = 'clarifai'
APP_ID = 'main'
# Change these to whatever model and image URL you want to use
MODEL_ID = 'general-image-detection'
MODEL_VERSION_ID = '1580bb1932594c93b7e2e04456af7c6f'
IMAGE_URL = 'https://evolveindia.co/wp-content/uploads/2021/07/1_The-Wooden-Rhapsody-Modern-Bedroom-Interior-Design.jpg'
# To use a local file, assign the location variable
IMAGE_FILE_LOCATION = ''

############################################################################
# YOU DO NOT NEED TO CHANGE ANYTHING BELOW THIS LINE TO RUN THIS EXAMPLE
############################################################################

from clarifai_grpc.channel.clarifai_channel import ClarifaiChannel
from clarifai_grpc.grpc.api import resources_pb2, service_pb2, service_pb2_grpc
from clarifai_grpc.grpc.api.status import status_code_pb2

channel = ClarifaiChannel.get_grpc_channel()
stub = service_pb2_grpc.V2Stub(channel)

metadata = (('authorization', 'Key ' + PAT),)

userDataObject = resources_pb2.UserAppIDSet(user_id=USER_ID, app_id=APP_ID)

# To use a local file, uncomment the following lines
# with open(IMAGE_FILE_LOCATION, "rb") as f:
#     file_bytes = f.read()

post_model_outputs_response = stub.PostModelOutputs(
    service_pb2.PostModelOutputsRequest(
        user_app_id=userDataObject,  # The userDataObject is created in the overview and is required when using a PAT
        model_id=MODEL_ID,
        version_id=MODEL_VERSION_ID,  # This is optional. Defaults to the latest model version
        inputs=[
            resources_pb2.Input(
                data=resources_pb2.Data(
                    image=resources_pb2.Image(
                        url=IMAGE_URL
                       # base64=file_bytes
                    )
                )
            )
        ]
    ),
    metadata=metadata
)
if post_model_outputs_response.status.code != status_code_pb2.SUCCESS:
    print(post_model_outputs_response.status)
    raise Exception("Post model outputs failed, status: " + post_model_outputs_response.status.description)
    
regions = post_model_outputs_response.outputs[0].data.regions

for region in regions:
    # Accessing and rounding the bounding box values
    top_row = round(region.region_info.bounding_box.top_row, 3)
    left_col = round(region.region_info.bounding_box.left_col, 3)
    bottom_row = round(region.region_info.bounding_box.bottom_row, 3)
    right_col = round(region.region_info.bounding_box.right_col, 3)
    
    for concept in region.data.concepts:
        # Accessing and rounding the concept value
        name = concept.name
        value = round(concept.value, 4)

        print((f"{name}: {value} BBox: {top_row}, {left_col}, {bottom_row}, {right_col}"))
