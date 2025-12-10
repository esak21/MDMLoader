from constructs import Construct
from aws_cdk import (
    aws_sns as _sns,
    CfnTag
)

from src.infra.my_stack_props import SNSGearprops


class SNSGear(Construct):
    def __init__(self, scope: Construct, id: str, props:SNSGearprops,   **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        sns_topic_tags = CfnTag(
            key="created_by",
            value="App_Infra_Automation"
        )

        created_sns_topic = _sns.CfnTopic(self, "EDM-SNS-Topic",
                                            topic_name=props.topic_name ,
                                            display_name=props.topic_name,
                                             fifo_topic = False,
                                            tags= [sns_topic_tags],
                            )

        created_sns_topic_arn = created_sns_topic.attr_topic_arn
        print(f"we have created the SNS Topic and its ARn is {created_sns_topic_arn}")
        # create the Email Subscription for the topic
        _sns.CfnSubscription(self, "EDM-SNS-Subscription",
                             topic_arn= created_sns_topic_arn,
                             protocol= "email",
                             endpoint= props.email
                            )


