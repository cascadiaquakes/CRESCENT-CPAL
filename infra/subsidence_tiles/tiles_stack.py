from aws_cdk import CfnOutput, RemovalPolicy, Stack
from aws_cdk import aws_cloudfront as cloudfront
from aws_cdk import aws_cloudfront_origins as origins
from aws_cdk import aws_s3 as s3
from constructs import Construct


class SubsidenceTilesStack(Stack):
    """Private S3 bucket of map tiles, served read-only through CloudFront."""

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        bucket = s3.Bucket(
            self, "TilesBucket",
            block_public_access=s3.BlockPublicAccess.BLOCK_ALL,
            encryption=s3.BucketEncryption.S3_MANAGED,
            enforce_ssl=True,
            removal_policy=RemovalPolicy.RETAIN,
            cors=[s3.CorsRule(allowed_methods=[s3.HttpMethods.GET, s3.HttpMethods.HEAD],
                              allowed_origins=["*"], allowed_headers=["*"], max_age=86400)],
        )

        distribution = cloudfront.Distribution(
            self, "TilesDistribution",
            comment="CPAL map tiles",
            default_behavior=cloudfront.BehaviorOptions(
                origin=origins.S3BucketOrigin.with_origin_access_control(bucket),
                viewer_protocol_policy=cloudfront.ViewerProtocolPolicy.REDIRECT_TO_HTTPS,
                allowed_methods=cloudfront.AllowedMethods.ALLOW_GET_HEAD_OPTIONS,
                cache_policy=cloudfront.CachePolicy.CACHING_OPTIMIZED,
                # Pass the browser's Origin to S3 so its CORS rules answer every request.
                origin_request_policy=cloudfront.OriginRequestPolicy.CORS_S3_ORIGIN,
                # Public, read-only data loaded by the dev and prod viewers.
                response_headers_policy=cloudfront.ResponseHeadersPolicy.CORS_ALLOW_ALL_ORIGINS,
            ),
            price_class=cloudfront.PriceClass.PRICE_CLASS_100,
        )

        CfnOutput(self, "BucketName", value=bucket.bucket_name)
        CfnOutput(self, "TilesUrl", value=f"https://{distribution.distribution_domain_name}")
