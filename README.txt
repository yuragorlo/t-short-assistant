python -m venv tshort
source ./tshort/bin/activate
pip3 install -r requirements.txt
cp .env.example .env
nano .env # add your OPENAI_API_KEY
python run.py --verbose # run with tools
python run.py --config examples/t_short_agent_setup.json --verbose # run without tools
chainlit run chainlit_app.py --port 3000 # run with WEB