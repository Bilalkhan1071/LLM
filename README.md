# Talk to PDF 
- Python application that uses AWS Lambda to deploy a docker image of the app
- Allows user to ask questions about the given pdf
- PDF covers the topic of fuzzy logic systems and how they can be used to answer the question "What happens next?"

# Instructions
- Clone this repo
- Create and activate conda environment
- Install requirements using `pip install -r requirments.txt`
- Run `python query.py`
- Change `userprompt` on line 6 of query.py as needed



NOTE:
- Initial run can be slow due to lambda needing to warm up.