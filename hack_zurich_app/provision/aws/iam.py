import sagemaker
import boto3


def get_sagemaker_role():
    sess = sagemaker.Session()
    # sagemaker session bucket -> used for uploading data, models and logs
    # sagemaker will automatically create this bucket if it not exists
    sagemaker_session_bucket = None
    if sagemaker_session_bucket is None and sess is not None:
        # set to default bucket if a bucket name is not given
        sagemaker_session_bucket = sess.default_bucket()

    try:
        role = sagemaker.get_execution_role()
    except ValueError:
        iam = boto3.client("iam")
        role = iam.get_role(RoleName="sagemaker_execution_role")["Role"]["Arn"]

    return role


if __name__ == "__main__":
    print(get_sagemaker_role())
