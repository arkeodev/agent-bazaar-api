#!/bin/bash

# Wait for database to be ready
echo "Waiting for database..."
while ! pg_isready -h db -p 5432 -U postgres; do
    sleep 1
done
echo "Database is ready!"

# Run migrations
echo "Running database migrations..."
cd /code/src && PYTHONPATH=/code/src alembic upgrade head

# Start the application based on service type
if [ "$SERVICE_TYPE" = "web" ]; then
    echo "Starting the web application..."
    uvicorn app.main:app --host 0.0.0.0 --port 8000
elif [ "$SERVICE_TYPE" = "streamlit" ]; then
    echo "Starting the Streamlit application..."
    cd /code/src && streamlit run app/streamlit/main.py --server.port 8501 --server.address 0.0.0.0
elif [ "$SERVICE_TYPE" = "pytest" ]; then
    echo "Running tests..."
    pytest /code/tests/
else
    echo "Unknown service type: $SERVICE_TYPE"
    exit 1
fi
