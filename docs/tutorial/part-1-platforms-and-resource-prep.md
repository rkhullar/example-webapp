# FastAPI on AWS with MongoDB Atlas and Okta - Part 1
## Platforms and Resource Preparation

### Amazon Web Services (AWS)
You will need access to an AWS account to follow along and deploy the example api. If you are deploying to your own account
remember to clean up the resources afterward to minimize billing charges. I also suggest setting up cloudwatch billing
alerts and using a service like [privacy.com](https://privacy.com) to prevent overcharging. If you do not have an AWS account
you could try using the lab environment on [A Cloud Guru](https://learn.acloud.guru/labs).

#### AWS User and Lambda Role
For this tutorial we are managing database access to the MongoDB Atlas Cluster through AWS Identity and Access Management
(IAM). During local development you should have your `AWS_PROFILE` configured, which points to the credentials uses for AWS
integrations: `aws_access_key_id` `aws_secret_access_key` and for roles `aws_session_token`. When you create the IAM user
in your AWS account be sure to follow good security practices like adding MFA and using a strong password.

When we create the lambda function later on we will need to specify the role. So let's create the role with the name
`example-backend-dev` and the `AWSLambdaBasicExecutionRole` managed policy. The trust relationship for the role should
define `lambda.amazonaws.com` as the service, which means that the role can be assumed by any lambda function in the account.

### MongoDB Atlas Cluster
If you haven't already, head over to [MongoDB Cloud](https://www.mongodb.com/cloud) to create a free tier Atlas cluster.
Within your organization namespace create a `dev` project. And within that project create a shared cluster called
`default-free-dev` backed by AWS and located in the closest available region to you. For example if you are based in
New York the region would be `us-east-1`.

During the cluster creation process the Atlas UI will ask you to create database user credentials and define the ip address
or cidr blocks that should be allowed to connect. You can go ahead and use the default generated credentials. We don't
actually need static database credentials for our project, since we're using passwordless authentication via AWS IAM.

For the ip address list we need to allow network traffic from `0.0.0.0/0` or "anywhere". For a production environment we can
revisit this network control, but there is significantly more work involved to make an optimal integration. Aside from the
vpc setup, it would require either creating a private link (vpc endpoint) or using vpc peering depending on the type of
Atlas cluster. Those components don't fall under AWS or Atlas free tier.

After creating the cluster delete the default credential based user and replace it with your AWS user arn. When you
add the new database user in the Atlas UI select `AWS IAM` for the authentication method and select `IAM User` for the type.
For the database user privileges choose the built-in role "read and write to any database". And as a good practice you
should explicitly define which cluster the permissions apply to.

This would also be a good time to create another database user that represents the lambda function we'll deploy to later on.
This time select `IAM Role` for the type and enter the lambda role arn. For the permissions we want to follow the principle
of least privilege. So for this example project we'll define a single permission: `readWrite` to the `default` database
`message` collection.

We will need the cluster host value during local development and deployment. On the Atlas UI follow the instructions to
connect to the cluster. We don't need the full connection url, just the host value. It should look similar to this:
`default-free-dev.example.mongodb.net`

### Okta
We want to protect the endpoints in our example application by requiring users to be logged in. You can sign up for a free
okta developer account by heading to their [developer login page](https://developer.okta.com/login). After signing up you
could optionally customize your org by setting a custom domain name and adding social login. That is not the focus of this
tutorial, but the following links should help:

- [Okta: Managed Custom Domain Certificate][okta-managed-cert]
- [Okta: Google Social Login][okta-google-sso]

Within your okta developer org create an app integration and select "OIDC" for the login method and "Single Page Application (SPA)"
for the type. You can rename the client app after creation. I had called mine `Hello World (SPA)`. Under the grant type
settings make sure `Authorization Code` is enabled, and optionally enable `Refresh Token` if you're planning on creating
a frontend or mobile app later on. Clear the logout urls, and for the allowed login urls we need `http://localhost:8000/docs/oauth2-redirect`.
You can also add non-local urls if you know the domain where you want to deploy the api to. For example if you own `company.org`
you could add another allowed login url from `https://api-dev.example.company.org/docs/oauth2-redirect`. Finally under the
assignments settings, select "skip group assignment for now."

We still need to define which users should have access the client app within okta. For this I suggest enabling federation
broker mode under the app's general settings. This way we can define an authentication policy to manage access, and the
same policy can be reused for other client apps. For example, you could have a policy for unreleased applications that allows
access to internal employees and beta testers. And then another policy for applications that are generally available.
For this tutorial, you should be able to use one of the default policies that are created with your developer org like
`Any two factors` or `Password only`. Alternatively, if you keep federation broker mode disabled, you need to assign the app
to users or groups within your okta org in order for them to log in to the client app.

With your okta developer org and client app created, take note of the host and client id. The default host value would be
something like `dev-12345678.okta.com`.

---
- [Continue to Part 2: Project Setup and Local Development][part-2]
- [Overview][overview]

[okta-managed-cert]: https://developer.okta.com/docs/guides/custom-url-domain/main/#use-an-okta-managed-certificate
[okta-google-sso]: https://developer.okta.com/docs/guides/social-login/google/main
