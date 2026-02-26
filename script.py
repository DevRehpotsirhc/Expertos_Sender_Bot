from services import execute_services
from scraper import execute_scraper



# Ejecutables que llamará cron
if __name__ == "__main__":
    execute_services()
    execute_scraper()
