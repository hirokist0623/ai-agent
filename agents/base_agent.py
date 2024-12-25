import os
import logging
from datetime import datetime

from utils.git import get_git_root
from utils.color_print import cprint


class BaseAgent:
    def __init__(self, agent_name: str):
        self.agent_name = agent_name
        self._setup_logging()

    def _setup_logging(self):
        git_root = get_git_root()
        log_dir = os.path.join(git_root, ".ai_agents", "logs")
        os.makedirs(log_dir, exist_ok=True)

        today = datetime.now().strftime("%Y-%m-%d")
        log_file = os.path.join(log_dir, f"{today}_log.txt")

        logging.basicConfig(
            filename=log_file,
            level=logging.INFO,
            format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S",
        )
        self.logger = logging.getLogger(self.agent_name)

    def main(self):
        cprint("######################################")
        cprint(f"# Running Agent: {self.agent_name}...")
        cprint("#######################################\n")
        self.logger.info("Agent %s started execution", self.agent_name)
        self.exec()
        self.logger.info("Agent %s finished execution", self.agent_name)

    def exec(self):
        self.logger.debug("exec method called")
        raise NotImplementedError

    # --------------------------------
    # logging methods
    # --------------------------------
    def log_info(self, message: str):
        self.logger.info(message)
        cprint(f"[INFO] {message}")

    def log_debug(self, message: str):
        self.logger.debug(message)
        cprint(f"[DEBUG] {message}", color="cyan")

    def log_error(self, message: str):
        self.logger.error(message)
        cprint(f"[ERROR] {message}", color="red")
