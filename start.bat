@echo off
echo Starting ElasticSearch...
start /B elasticsearch

timeout /T 10

echo Indexing Data...
python backend\elasticsearch_setup.py

echo Generating FAQs...
python backend\nlp_faq_generator.py

echo Starting Flask API...
start /B python backend\app.py

echo Starting React Frontend...
cd frontend && npm start
