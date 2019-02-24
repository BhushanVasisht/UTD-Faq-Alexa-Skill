# -*- coding: utf-8 -*-

# Comet Guide: A sample Alexa Skill Lambda function
# This function shows how you can pass alexa query and pass to external web service which performs all the NLP part,
# which find matches the query with its existing dataset and answers if match found.,
# handle YES/NO intents with session attributes,
# and return text data on a card.

import logging
import random
import gettext

from ask_sdk_core.skill_builder import SkillBuilder
from ask_sdk_core.handler_input import HandlerInput
from ask_sdk_core.dispatch_components import (
    AbstractRequestHandler, AbstractExceptionHandler,
    AbstractRequestInterceptor)
from ask_sdk_core.utils import is_intent_name, is_request_type

from ask_sdk_model import Response
from ask_sdk_model.ui import SimpleCard

from alexa import data,util

# Skill Builder object
sb = SkillBuilder()

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


# Request Handler classes
class LaunchRequestHandler(AbstractRequestHandler):
    """Handler for skill launch."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return is_request_type("LaunchRequest")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        logger.info("In LaunchRequestHandler")
        _ = handler_input.attributes_manager.request_attributes["_"]

        # logger.info(_("This is an untranslated message"))

        speech = _(data.WELCOME)
        speech += " " + _(data.HELP)
        handler_input.response_builder.speak(speech)
        handler_input.response_builder.ask(_(
            data.GENERIC_REPROMPT))
        return handler_input.response_builder.response


class AboutIntentHandler(AbstractRequestHandler):
    """Handler for about intent."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return is_intent_name("AboutIntent")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        logger.info("In AboutIntentHandler")
        _ = handler_input.attributes_manager.request_attributes["_"]

        handler_input.response_builder.speak(_(data.ABOUT))
        return handler_input.response_builder.response

class FAQIntentIntentHandler(AbstractRequestHandler):
    """Handler for Faq intent."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return is_intent_name("FaqIntent")(handler_input)
        

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        logger.info("In FaqIntent")
        query = util.get_resolved_value(
            handler_input.request_envelope.request, "query")
        attribute_manager = handler_input.attributes_manager
        session_attr = attribute_manager.session_attributes
        _ = attribute_manager.request_attributes["_"]
        try:
            className=session_attr["class"]
        except Exception:
            className="housing"
        answer = util.get_answer(
            {"query":query,"class":className }, data.MY_API)

        speech = answer
        handler_input.response_builder.speak(speech).set_should_end_session(
            True)
        return handler_input.response_builder.response

class OptionIntentIntentHandler(AbstractRequestHandler):
    """Handler for Faq intent."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return is_intent_name("OptionIntent")(handler_input)
        

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        logger.info("In FaqIntent")
        housing = util.get_resolved_value(
            handler_input.request_envelope.request, "housing")
        alumni = util.get_resolved_value(
        handler_input.request_envelope.request, "alumni")
        attribute_manager = handler_input.attributes_manager
        session_attr = attribute_manager.session_attributes
        if(housing is not None):
            session_attr["class"] = "housing"
        elif(alumni is not None):
            session_attr["class"] = "alumni"
        else:
            session_attr["class"] = "counseling"

        speech = "Ok... Thank you for your response... Now you can ask me your queries with hot keyword... 'tell me' "
        handler_input.response_builder.speak(speech).ask(speech)
        return handler_input.response_builder.response

class SessionEndedRequestHandler(AbstractRequestHandler):
    """Handler for skill session end."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return is_request_type("SessionEndedRequest")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        logger.info("In SessionEndedRequestHandler")
        logger.info("Session ended with reason: {}".format(
            handler_input.request_envelope.request.reason))
        return handler_input.response_builder.response


class HelpIntentHandler(AbstractRequestHandler):
    """Handler for help intent."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return is_intent_name("AMAZON.HelpIntent")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        logger.info("In HelpIntentHandler")
        _ = handler_input.attributes_manager.request_attributes["_"]

        handler_input.response_builder.speak(_(
            data.HELP)).ask(_(data.HELP))
        return handler_input.response_builder.response


class ExitIntentHandler(AbstractRequestHandler):
    """Single Handler for Cancel, Stop intents."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return (is_intent_name("AMAZON.CancelIntent")(handler_input) or
                is_intent_name("AMAZON.StopIntent")(handler_input))

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        logger.info("In ExitIntentHandler")
        _ = handler_input.attributes_manager.request_attributes["_"]

        handler_input.response_builder.speak(_(
            data.STOP)).set_should_end_session(True)
        return handler_input.response_builder.response

class FallbackIntentHandler(AbstractRequestHandler):
    """Handler for go out intent."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        # return is_intent_name("AMAZON.FallbackIntent")(handler_input)
        return is_intent_name("FAQ")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        logger.info("In AMAZON.FallbackIntent")
       

        speech = "I am sorry! I am unable to answer your query."

        handler_input.response_builder.speak(speech)
        return handler_input.response_builder.response


# Exception Handler classes
class CatchAllExceptionHandler(AbstractExceptionHandler):
    """Catch All Exception handler.
    This handler catches all kinds of exceptions and prints
    the stack trace on AWS Cloudwatch with the request envelope."""
    def can_handle(self, handler_input, exception):
        # type: (HandlerInput, Exception) -> bool
        return True

    def handle(self, handler_input, exception):
        # type: (HandlerInput, Exception) -> Response
        logger.error(exception, exc_info=True)
        logger.info("Original request was {}".format(
            handler_input.request_envelope.request))

        speech = "Sorry, there was some problem. Please try again!!"
        handler_input.response_builder.speak(speech).ask(speech)

        return handler_input.response_builder.response


class LocalizationInterceptor(AbstractRequestInterceptor):
    """Add function to request attributes, that can load locale specific data."""
    def process(self, handler_input):
        # type: (HandlerInput) -> None
        locale = handler_input.request_envelope.request.locale
        logger.info("Locale is {}".format(locale))
        i18n = gettext.translation(
            'base', localedir='locales', languages=[locale], fallback=True)
        handler_input.attributes_manager.request_attributes[
            "_"] = i18n.gettext


# Add all request handlers to the skill.
sb.add_request_handler(LaunchRequestHandler())
sb.add_request_handler(AboutIntentHandler())
sb.add_request_handler(FAQIntentIntentHandler())
sb.add_request_handler(OptionIntentIntentHandler())
sb.add_request_handler(HelpIntentHandler())
sb.add_request_handler(FallbackIntentHandler())
sb.add_request_handler(ExitIntentHandler())
sb.add_request_handler(SessionEndedRequestHandler())

# Add exception handler to the skill.
sb.add_exception_handler(CatchAllExceptionHandler())

# Add locale interceptor to the skill.
sb.add_global_request_interceptor(LocalizationInterceptor())

# Expose the lambda handler to register in AWS Lambda.
lambda_handler = sb.lambda_handler()