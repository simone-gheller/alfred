import os
import inspect
from typing import Any
from api.status import status
from api.steps import Step
from api.loggers import init_logging

def run_pipeline():
    f = inspect.currentframe().f_back
    PIPELINE = f.f_locals.get('PIPELINE')
    folder = PIPELINE.work_dir
    if not os.path.exists(folder): os.mkdir(folder)
    init_logging(folder)
    if PIPELINE is None:
        raise AttributeError('PIPELINE variable is missing')
    try:
        return PIPELINE.execute()
    except KeyboardInterrupt:
        logger.error("🚨 Pipeline interrupted by user via KeyboardInterrupt (Ctrl+C).")
        print("\nPipeline execution was interrupted. Exiting gracefully...")
        PIPELINE.status = status.ABORTED
    except Exception:
        return Exception("Pipeline execution aborted due to error.")


from api.loggers import get_logger
logger = get_logger()

class Pipeline:

    _instance = None
    archive = {}
    status = status.SUCCESS

    def __new__(cls, steps: list = None):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.steps = steps
            folder = os.path.abspath(os.path.splitext(os.path.basename(
                inspect.currentframe().f_back.f_locals.get('__file__')))[0])
            if not os.path.exists(folder): os.mkdir(folder)
            cls.work_dir = folder
        return cls._instance

    def __init__(self, steps: list = None):
        if not hasattr(self, 'steps'):
            self.steps = steps
            self.status = status.SUCCESS

    @staticmethod
    def abort() -> None:
        Pipeline.status = status.ABORTED
        logger.info("🚨 Pipeline aborted by user.")  # Log dell'abort solo qui

    def execute(self) -> Any:
        logger.info("🚀 Starting pipeline execution...")
        try:
            data = None
            for i, step in enumerate(self.steps):
                data = step.run(data)
                if Pipeline.status == status.ABORTED: break
                logger.info(f"Step {i + 1} completed.")
                
            if Pipeline.status == status.SUCCESS:
                logger.info("✅ Pipeline execution completed successfully.")
            return data

        except Exception as e:
            self.status = status.FAILURE
            logger.error("❌ Uh-oh, something went wrong")
            from api.steps import OnFailure
            failure_steps = [s for s in self.steps if isinstance(s, OnFailure)]
            try:
                for s in failure_steps:
                    s.status = self.status
                    s.run()
            except Exception as e:
                logger.exception(e)
            logger.exception(e)
            raise e
