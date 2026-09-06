import asyncio
import app_core
if __name__ == '__main__':
    app_core.PORT=3000
    try:
        asyncio.run(app_core.main())
    except KeyboardInterrupt:
        pass
