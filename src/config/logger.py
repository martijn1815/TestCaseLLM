import logging

# Create and configure logger
logging.basicConfig(
    filename="../logfiles/policy_agent.log",
    format="{asctime} - {levelname} - {name} - {message}",
    style="{",
    level=logging.INFO
)

logger = logging.getLogger()
