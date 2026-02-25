BASE_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
LOG_FILE="$BASE_DIR/cron.log"
EXEC="$BASE_DIR/.venv/bin/python $BASE_DIR/script.py"

touch "$LOG_FILE"
chmod 666 "$LOG_FILE"

TAREA="* * * * * $EXEC >> $LOG_FILE 2>&1"

(crontab -l 2>/dev/null | grep -F -q "$TAREA") || \
( crontab -l 2>/dev/null; echo "$TAREA" ) | crontab -
