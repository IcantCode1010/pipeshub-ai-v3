from app.utils.logger import create_logger
from app.config.configuration_service import ConfigurationService
import asyncio
import os
import sys
from pathlib import Path

# Add the project root to Python path
project_root = str(Path(__file__).parent.parent)
sys.path.append(project_root)


logger = create_logger('etcd_loader')


async def load_config():
    """Load default configuration into etcd."""
    try:
        logger.info("🚀 Starting configuration loading process")

        # Initialize ConfigurationService with environment
        environment = 'dev'
        logger.info(f"🔧 Using environment: {environment}")

        config_service = ConfigurationService(environment=environment)

        # Check if any configuration exists and get user preference for overwrite
        has_config = await config_service.has_configuration()
        overwrite = False

        if has_config:
            logger.warning("⚠️ Some configuration already exists in etcd")
            user_input = input(
                "Do you want to overwrite existing configuration? (y/N): ")
            if user_input.lower() == 'y':
                overwrite = True
            else:
                logger.info("ℹ️ Will only add new configuration keys")

        # Load default configuration
        logger.info("📝 Loading default configuration...")
        await config_service.load_default_config(overwrite=overwrite)
        logger.info("✅ Default configuration loaded successfully")

    except Exception as e:
        logger.error(f"❌ Failed to load configuration: {str(e)}")
        raise

if __name__ == "__main__":
    try:
        asyncio.run(load_config())
    except KeyboardInterrupt:
        logger.info("⚠️ Process interrupted by user")
    except Exception as e:
        logger.error(f"❌ An error occurred: {str(e)}")
        sys.exit(1)
