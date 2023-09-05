from google.cloud import aiplatform

aiplatform.init(
    # your Google Cloud Project ID or number
    # environment default used is not set
    project='le-wagon-bootcamp-392422',

    # the Vertex AI region you will use
    # defaults to us-central1
    location='us-central1',

    # Google Cloud Storage bucket in same region as location
    # used to stage artifacts
    staging_bucket='gs://no_sploil_zone',

    # custom google.auth.credentials.Credentials
    # environment default creds used if not set
    # credentials=credentials,

    # customer managed encryption key resource name
    # will be applied to all Vertex AI resources if set
    # encryption_spec_key_name=my_encryption_key_name,

    # the name of the experiment to use to track
    # logged metrics and parameters
    # experiment='my-experiment',

    # description of the experiment above
    # experiment_description='my experiment decsription'
)
