import os
from alfred.api.status import status
from alfred.api.loggers import init_logging, get_logger

def run_pipeline():
    folder = Pipeline.work_dir
    if not os.path.exists(folder):
        os.mkdir(folder)
    init_logging(folder)
    try:
        return Pipeline.execute()
    except KeyboardInterrupt:
        logger = get_logger()
        logger.error("🚨 Pipeline interrupted by user via KeyboardInterrupt (Ctrl+C).")
        print("\nPipeline execution was interrupted. Exiting gracefully...")
        Pipeline.status = status.ABORTED
    except Exception:
        return Exception("Pipeline execution aborted due to error.")
    

import os, inspect
from typing import Any
from alfred.api.loggers import get_logger
from alfred.api.status import status
logger = get_logger()

class Pipeline:

    _instance = None

    def __new__(cls, steps):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        cls.steps = steps
        cls.work_dir = os.path.abspath(os.path.splitext(os.path.basename(
            inspect.currentframe().f_back.f_locals.get('__file__')))[0])
        cls.archive = {}
        cls.status = status.SUCCESS
        return cls._instance

    @classmethod
    def abort(cls) -> None:
        cls.status = status.ABORTED
        logger.info("🚨 Pipeline aborted by user.")
    
    @classmethod
    def execute(cls) -> Any:
        logger.info("🚀 Starting pipeline execution...")
        try:
            data = None
            for i, step in enumerate(cls.steps):
                data = step.run(data)
                if cls.status == status.ABORTED: break
                logger.info(f"Step {i + 1} completed.")
                
            if cls.status == status.SUCCESS:
                logger.info("✅ Pipeline execution completed successfully.")
            return data
        except Exception as e:
            cls.status = status.FAILURE
            logger.error("❌ Uh-oh, something went wrong")
            from alfred.api.steps import OnFailure
            failure_steps = [s for s in cls.steps if isinstance(s, OnFailure)]
            try:
                for s in failure_steps:
                    s.status = cls.status
                    s.run()
            except Exception as e:
                logger.exception(e)
            logger.exception(e)
            raise e
        
from alfred.api.steps import Step