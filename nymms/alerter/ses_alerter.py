import logging

logger = logging.getLogger(__name__)

from boto.ses import connect_to_region

from nymms.config import config


class SESAlerter(object):
    def __init__(self, region):
        self.region = region
        self.connection = None
    
    def connect(self):
        self.connection = connect_to_region(self.region)

    def alert(self, task_result):
        if not self.connection:
            logger.debug("Connecting to SES in region %s." % (self.region,))
            self.connect()
        subject_template = config.settings['alerts']['subject']
        sender = config.settings['alerts']['sender']
        body = config.settings['alerts']['body']
        recipients = config.settings['alerts']['recipients']
        result_data = task_result.serialize()
        logger.debug("Sending SES alert to %s as %s for %s" % (
            recipients, sender, task_result.id))
        self.connection.send_email(
            source=sender,
            subject=subject_template.format(**result_data),
            body=body.format(**result_data),
            to_addresses=recipients
        )
