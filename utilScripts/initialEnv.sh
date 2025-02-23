cd ../../
mysiteName=laiyff-web-dev
python -m venv ${mysiteName}/env
source ${mysiteName}/env/bin/activate

cd ${mysiteName}
pip install -r requirements.txt
