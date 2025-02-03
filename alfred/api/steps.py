import inspect
from typing import Any, Optional, Callable
from api.status import status
from api.loggers import get_logger
from api.config import CONFIG
from api.pipeline import Pipeline

logger = get_logger()

class Step:
    def __init__(self, function: Callable[[Optional[Any]], Any]):
        self.name = function.__name__
        self.function = function

    def run(self, input_data: Optional[Any] = None) -> Any:
        logger.info(f"Executing step: {self.name} 🏃")
        argv = len(inspect.signature(self.function).parameters)
        return self.function(input_data) if argv > 0 else self.function()

class OnFailure(Step):
    def run(self, input_data: Optional[Any] = None) -> Any:
        if self.status is None or self.status != status.FAILURE:
            return
        return super().run(input_data)
    
    def __getattr__(self, name):
        if name == 'status':
            return None
        return self.__getattr__(name)
    
class SlackNotification(Step):
    def __init__(self, function: Callable[[Optional[Any]], dict], on_status: Optional[None] = None):
        self.on_status = on_status
        self.function = function

    def run(self, input_data: Optional[Any] = None) -> Any:
        if self.status is None or self.status != self.on_status:
            return
        logger.info(f"Sending notifications... 📫")
        argv = len(inspect.signature(self.function).parameters)
        msg = self.function(input_data) if argv > 0 else self.function()
        if not isinstance(msg, dict): raise TypeError(f'{self.function.__name__} must return a dict data type')
        ch_id = msg['channel_id']
        text = msg['text']
        self.__slack_send(ch_id, text)

    def __slack_send(channel_id: str, text: str):
        from slack_sdk import WebClient
        from slack_sdk.errors import SlackApiError

        SLACK_BOT_TOKEN = CONFIG.get('notifications.slack', {}).get('token', None)
        client = WebClient(token=SLACK_BOT_TOKEN)
        try:
            response = client.chat_postMessage(channel=channel_id, text=text)
            print(f"Message sent: {response['message']['text']}")
        except SlackApiError as e:
            print(f"Error: {e.response['error']}")

    def __getattr__(self, name):
        if name == 'status':
            return None
        return self.__getattr__(name)

class MailNotification(Step):
    def __init__(self, function: Callable[[Optional[Any]], dict], on_status: Optional[None] = None):
        self.on_status = on_status
        self.function = function

    def run(self, input_data: Optional[Any] = None) -> Any:
        if self.status is None or self.status != self.on_status:
            return
        logger.info(f"Sending notifications... 📫")
        argv = len(inspect.signature(self.function).parameters)
        msg = self.function(input_data) if argv > 0 else self.function()
        if not isinstance(msg, dict): raise TypeError(f'{self.function.__name__} must return a dict data type')
        to = msg['channel_id']
        subject = msg['text']
        text = msg['text']
        self.__send_mail(to, subject, text)
    
    def __send_mail(to: list[str], subject: str, text: str):
        import smtplib
        from email.mime.text import MIMEText
        from email.mime.multipart import MIMEMultipart

        config = CONFIG.CONFIG.get('notifications.emails', {})
        smtp_server = config.get("smtp_server", None)
        smtp_port = config.get("smtp_port", None)
        sender_email = config.get("smtp_email", None)
        receiver_email = to
        password = config.get("password", None)

        message = MIMEMultipart()
        message['From'] = sender_email
        message['To'] = receiver_email
        message['Subject'] = subject
        message.attach(MIMEText(text, 'plain'))

        try:
            with smtplib.SMTP(smtp_server, smtp_port) as server:
                server.starttls()
                server.login(sender_email, password)
                text = message.as_string()
                server.sendmail(sender_email, receiver_email, text)
                print("Email sent successfully!")
        except Exception as e:
            print(f"Error while sending email: {e}")

    def __getattr__(self, name):
        if name == 'status':
            return None
        return self.__getattr__(name)

class RetryStep(Step):
    def __init__(self, func, retries: int = 3, delay: int = 1000):
        super().__init__(func)
        self.retries = retries
        self.delay = delay

    def run(self, input_data: Optional[Any] = None) -> Any:
        attempt = 0
        while attempt < self.retries:
            try:
                return super().run(input_data)
            except Exception as e:
                attempt += 1
                if attempt < self.retries:
                    import time
                    print(f"Attempt {attempt} failed. Retrying in {self.delay} ms ...")
                    time.sleep(self.delay/1000)
                else:
                    print(f"Attempt {attempt} failed. Giving up.")
                    raise e

class InteractiveStep(Step):

    def run(self, input_data: Optional[Any] = None) -> Any:
        options = {1: 'Continue', 2: 'Abort'}
        print("Available options:")
        for idx, option in options.items():
            print(f"{idx}. {option}")

        choice = input(f"Please select an option (1-{len(options)}): ")

        while not (choice.isdigit() and 1 <= int(choice) <= len(options)):
            print('Invalid choice, please select an actual option (1 or 2).')
            choice = input(f"Please select an option (1-{len(options)}): ")

        choice = int(choice)
        if choice == 1:
            return super().run(input_data)
        elif choice == 2:
            Pipeline.abort()
            return None
