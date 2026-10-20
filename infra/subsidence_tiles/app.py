#!/usr/bin/env python3
import aws_cdk as cdk

from tiles_stack import SubsidenceTilesStack

app = cdk.App()
SubsidenceTilesStack(app, "CpalSubsidenceTiles", env=cdk.Environment(account="818214664804", region="us-east-2"))
app.synth()
