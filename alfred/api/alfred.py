import os
from api.status import status
from api.loggers import init_logging, get_logger
from api.steps import Step
from api.pipeline import Pipeline

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